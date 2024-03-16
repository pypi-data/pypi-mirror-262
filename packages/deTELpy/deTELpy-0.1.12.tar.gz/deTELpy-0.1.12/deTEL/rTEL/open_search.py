"""Implementation of the open search workflow using Python core functionality."""
import argparse
import copy
import fileinput
import functools
import glob
import logging
import os.path
import platform
import subprocess
import sys
from inspect import getsourcefile
from os.path import abspath
from pathlib import Path
from typing import List

from Bio import SeqIO

from deTEL.exceptions import WrongSequenceTypeError
from deTEL.rTEL import SequenceType
from deTEL.utils import is_valid_file

EXITING_MSG = "Exiting program now."

EXPECTED_TOOL_VERSIONS: dict = {
    "msfragger-jar": "4.0",
    "philosopher": "5.1.0",
    "ptmshepherd": "2.0.6",
    "ionquant": "1.10.12",
    "crystalc": "1.5.2",
    "batmass-io": "1.30.0",
    "grppr": "0.3.23",
    "commons-math3": "3.6.1",
    "jfreechart": "1.5.3",
    "hipparchus-core": "1.8",
    "hipparchus-stat": "1.8",
}

CLASSPATH_SEPARATOR: str = ";" if platform.system() == "Windows" else ":"


def parse_args(args):
    """Parse and retrieve input arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        dest="fasta",
        nargs="?",
        type=lambda x: is_valid_file(parser, x),
        help="Search database as codon fasta file",
    )
    parser.add_argument(
        dest="raw_file_location",
        nargs="?",
        help="Mass spec RAW file location",
    )
    parser.add_argument(
        "-c",
        "--num_threads",
        required=False,
        default=1,
        help="The number of threads used for processing by MSFragger and Crystal-C (default=1)",
        type=int,
    )
    parser.add_argument(
        "-p",
        "--output_dir_name",
        required=False,
        default="output",
        help="Name of the output folder created within the given RAW file directory.",
        type=str,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Turns on verbosity.",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "-iq",
        "--ionquant",
        help="Turns on MS1 precursor intensity-based quantification.",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "-cd",
        "--config_dir",
        required=False,
        help="Absolute path to the folder, which contains the configuration files for MSFragger, Crystal-C and Shepherd "
        "(open_search_params, crystal-c.params and shepherd.config).",
        type=str,
    )
    parser.add_argument(
        "-fp",
        "--fragpipe_bin_dir",
        required=False,
        help="Absolute path to the folder containing the FragPipe binary.",
        type=str,
    )
    parser.add_argument(
        "-gc",
        "--generate-config",
        required=False,
        help="Configuration directory output path. To be auto created by the software.",
        action="store_true",
    )
    return parser.parse_args(args), parser


def check_args_logic(args, parser):
    if (not args.fasta and not args.raw_file_location) and (
        not args.generate_config and not args.config_dir
    ):
        parser.error(
            "The following arguments are required: (FILE, DIR) | (--generate-config, --config_dir)"
        )

    if (args.fasta and not args.raw_file_location) or (
        not args.fasta and args.raw_file_location
    ):
        parser.error("The following positional arguments are required: (FILE, DIR)")
    elif args.generate_config and not args.config_dir:
        parser.error(
            "The following argument is required in addition to generate-config: --config_dir"
        )


def determine_sequence_type(fasta_input_file: Path) -> SequenceType:
    """
    Approach: Iterate over all sequence entries of the FASTA file. Convert each sequence record string into a
    set of unique letters. If this set is below a certain threshold, then all sequences are classified
    as a nucleotide sequences.
    :return: Sequence type, e.g. peptide or nucleotide sequence.
    """
    result = SequenceType.PEPTIDE
    with open(fasta_input_file) as handle:
        union_letters = set()
        for record in SeqIO.parse(handle, "fasta"):
            union_letters.update(set(str(record.seq)))
            if len(union_letters) <= 6:
                result = SequenceType.NUCLEOTIDE
                break
    return result


def touch_flag_files(step_name: str, item: int):
    def decorator_touch_flag_files(func):
        @functools.wraps(func)
        def wrapper_touch_file(*args, **kwargs):
            output_folder = (
                kwargs["output_folder"] if "output_folder" in kwargs else None
            )
            lock_flag_file = None
            if output_folder:
                lock_flag_file: Path = output_folder / f"step-{item}-{step_name}-lock"
                lock_flag_file.touch()

            return_value = func(*args, **kwargs)
            if output_folder:
                if lock_flag_file:
                    os.remove(lock_flag_file)
                success_flag_file: Path = (
                    output_folder / f"step-{item}-{step_name}-success"
                )
                success_flag_file.touch()
            return return_value

        return wrapper_touch_file

    return decorator_touch_flag_files


class OpenSearchRunner(object):
    def __init__(self):
        self.logger = logging.getLogger("detelpy.open_search")
        file_handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s: %(message)s")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        # take a snapshot of the current working directory (cwd)
        # due to Philosopher we need to change directory later on in the workflow
        # we'll use the cwd to build the absolute paths to the input sequence file and RAW file directory
        self.cwd = Path.cwd()

    def run(self, args):
        """Main function."""
        args, parser = parse_args(args)
        check_args_logic(args, parser)
        if args.verbose:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

        config_dir: str = args.config_dir
        script_file_path: str = abspath(getsourcefile(lambda: 0))
        root_folder = Path(Path(script_file_path).resolve().parent)
        default_config_folder: Path = root_folder / "configs"
        if args.generate_config:
            self.create_config_templates(default_config_folder, config_dir)
        else:
            self.logger.info("Running rTEL workflow...")
            fasta_input_file: Path = self.prepare_path(
                args.fasta
            )  # input sequence database (FASTA formatted)
            raw_file_location_folder: Path = self.prepare_path(args.raw_file_location)
            working_directory = copy.copy(raw_file_location_folder)
            num_threads: int = args.num_threads
            output_dir_name: str = args.output_dir_name
            is_ionquant: bool = args.ionquant
            fragpipe_bin: str = args.fragpipe_bin_dir
            output_folder = raw_file_location_folder / output_dir_name
            seq_type: SequenceType = determine_sequence_type(fasta_input_file)
            try:
                config_dir_path: Path = (
                    Path(config_dir) if config_dir else default_config_folder
                )
                #
                fragpipe_install_folder: Path = (
                    self.get_fragpipe_install_root_path(fragpipe_bin)
                    if fragpipe_bin
                    else self.read_system_paths(os.environ["PATH"])
                )
                tool_paths: dict = self.determine_tool_paths(fragpipe_install_folder)
                self.initial_checks(
                    fasta_input_file,
                    raw_file_location_folder,
                    tool_paths,
                    config_dir_path,
                )
                self.step_prepare_output_folder(output_folder=output_folder)
                #
                open_search_config_file_path = config_dir_path / "open_search.params"
                crystalc_config_file_path = config_dir_path / "crystal-c.params"
                shepherd_config_file_path = config_dir_path / "shepherd.config"
                #
                self.step_prepare_opensearch_config_file(
                    open_search_config_file_path,
                    fasta_input_file,
                    num_threads,
                    output_folder=output_folder,
                )
                os.chdir(f"{working_directory}")  # Change current working directory

                philosopher_exec: Path = tool_paths.get("philosopher") / "philosopher"
                self.step_clean_up_workspace(philosopher_exec)
                self.step_init_workspace(philosopher_exec, output_folder=output_folder)

                raw_files = self.step_find_raw_files(
                    raw_file_location_folder, output_folder=output_folder
                )
                msfragger_exec: Path = tool_paths["msfragger-jar"]
                self.step_run_msfragger(
                    config_file_path=open_search_config_file_path,
                    raw_files=raw_files,
                    tool_path=msfragger_exec,
                    output_folder=output_folder,
                )

                (
                    msfragger_tsv_files,
                    msfragger_pep_xml_files,
                ) = self.step_find_msfragger_output_files(
                    raw_file_location_folder, output_folder=output_folder
                )

                self.step_prepare_crystalc_config_file(
                    config_file=crystalc_config_file_path,
                    fasta_input_file=fasta_input_file,
                    num_threads=num_threads,
                    raw_file_location=raw_file_location_folder,
                    output_location=working_directory,
                    output_folder=output_folder,
                )
                self.step_run_crystalc(
                    config_file_path=crystalc_config_file_path,
                    pep_xml_files=msfragger_pep_xml_files,
                    tool_paths=tool_paths,
                    output_folder=output_folder,
                )

                crystalc_output_files = self.step_run_find_command(
                    folder=working_directory, file_suffix="_c.pepXML"
                )
                #
                self.step_run_peptideprophet(
                    philosopher_exec,
                    crystalc_output_files,
                    fasta_input_file,
                    output_folder=output_folder,
                )
                #
                interact_path = working_directory / "interact.pep.xml"
                uncalibrated_mzml_files: List[Path] = self.step_run_find_command(
                    folder=working_directory, file_suffix="_uncalibrated.mzML"
                )
                self.step_rewrite_pepxml(
                    interact_path,
                    fragpipe_install_folder,
                    uncalibrated_mzml_files,
                    output_folder=output_folder,
                )

                self.step_run_protein_prophet(
                    philosopher_exec, interact_path, output_folder=output_folder
                )

                self.step_run_db_annotate(
                    philosopher_exec, fasta_input_file, output_folder=output_folder
                )

                combined_path = working_directory / "combined.prot.xml"
                self.step_run_filtering(
                    philosopher_exec,
                    working_directory,
                    combined_path,
                    output_folder=output_folder,
                )

                self.step_run_report(philosopher_exec, output_folder=output_folder)

                psm_file_path = working_directory / "psm.tsv"
                self.step_prepare_shepherd_config_file(
                    config_file=shepherd_config_file_path,
                    fasta_input_file=fasta_input_file,
                    raw_file_location=raw_file_location_folder,
                    psm_file_path=psm_file_path,
                    output_folder=output_folder,
                )
                self.step_run_ptm_shepherd(
                    shepherd_config_file_path, tool_paths, output_folder=output_folder
                )

                self.step_clean_up_workspace(philosopher_exec)

                if is_ionquant:
                    self.step_run_ionquant(
                        raw_file_location_folder=raw_file_location_folder,
                        psm_file_path=psm_file_path,
                        num_threads=num_threads,
                        tool_paths=tool_paths,
                        output_folder=output_folder,
                    )
            except Exception as err:
                self.logger.error("An unexpected error occurred.")
                if seq_type != SequenceType.PEPTIDE:
                    raise WrongSequenceTypeError(args.fasta)
                raise err
            finally:
                self.step_move_all_but_raw_files(
                    source=raw_file_location_folder, dst=output_folder
                )

    @touch_flag_files(step_name="prep-opensearch-config", item=1)
    def step_prepare_opensearch_config_file(
        self,
        config_file: Path,
        fasta_input_file: Path,
        num_threads: int,
        output_folder=None,
    ) -> None:
        """Prepare open search configuration file. Set path to input database and number of threads.

        :param config_file: Path to the pre-existing configuration to edit
        :param fasta_input_file: Database input file FASTA formatted.
        :param num_threads: Number of threads to be used for MSFragger.
        :param output_folder: This parameter is used within the touch_flag_files decorator.
        """
        self.logger.info("Step: Preparing open search config file...")
        with fileinput.input(files=(config_file,), inplace=True) as f:
            for line in f:
                if line.startswith("database_name"):
                    new_line = f"database_name = {fasta_input_file}\n"
                elif line.startswith("num_threads"):
                    new_line = f"num_threads = {num_threads}\n"
                else:
                    new_line = line
                print(new_line, end="")  # noqa: T201

    @touch_flag_files(step_name="prepare_shepherd_config_file", item=14)
    def step_prepare_shepherd_config_file(
        self,
        config_file: Path,
        fasta_input_file: Path,
        raw_file_location: Path,
        psm_file_path: Path,
        output_folder=None,
    ) -> None:
        """Prepare shepherd configuration file. Set path to input database, PSM formatted file and
        RAW file location.

        :param config_file: Path to the pre-existing configuration to edit
        :param fasta_input_file: Database input file FASTA formatted.
        :param raw_file_location: Folder containing the RAW files downloaded from PRIDE.
        :param psm_file_path: PSM input file path.
        :param output_folder: This parameter is used within the touch_flag_files decorator.
        """
        self.logger.info("Step: Preparing Shepherd config file...")
        with fileinput.input(files=(config_file,), inplace=True) as f:
            for line in f:
                if line.startswith("database"):
                    new_line = f"database = {fasta_input_file}\n"
                elif line.startswith("dataset"):
                    new_line = (
                        f"dataset = dataset01 {psm_file_path} {raw_file_location}\n"
                    )
                else:
                    new_line = line
                print(new_line, end="")  # noqa: T201

    @touch_flag_files(step_name="prep-crystalc-config-file", item=6)
    def step_prepare_crystalc_config_file(
        self,
        config_file: Path,
        fasta_input_file: Path,
        num_threads: int,
        raw_file_location: Path,
        output_location: Path,
        output_folder=None,
    ) -> None:
        """Prepare CrystalC configuration file.

        :param config_file: Path to the pre-existing configuration to edit
        :param fasta_input_file: Database input file, FASTA formatted.
        :param num_threads: Number of threads used for the processing.
        :param raw_file_location: Folder containing the RAW files downloaded from PRIDE.
        :param output_location: Path to the output folder.
        :param output_folder: This parameter is used within the touch_flag_files decorator.
        """
        self.logger.info("Step: Preparing CrystalC config file...")
        with fileinput.input(files=(config_file,), inplace=True) as f:
            for line in f:
                if line.startswith("fasta"):
                    new_line = f"fasta = {fasta_input_file}\n"
                elif line.startswith("thread"):
                    new_line = f"thread = {num_threads}\n"
                elif line.startswith("raw_file_location"):
                    new_line = f"raw_file_location = {raw_file_location}\n"
                elif line.startswith("output_location"):
                    new_line = f"output_location = {output_location}\n"
                else:
                    new_line = line
                print(new_line, end="")  # noqa: T201

    def step_prepare_output_folder(self, output_folder: Path) -> None:
        """Make sure that the provided output folder does exist and create it if needed."""
        self.logger.info("Step: Preparing output folder...")
        if not output_folder.exists():
            output_folder.mkdir(exist_ok=True)
        self.logger.info(
            f"Writing output file to the following folder: {output_folder}"
        )

    def run_subprocess(self, args: List[str]):
        """Generic function for running command line tools using Python's subprocess module.

        :param args: Provided tool command.
        """
        command = " ".join(args)
        self.logger.debug(f"Running: {command}")
        try:
            subprocess.run(
                args=args,
                timeout=3600,
                check=True,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
        except subprocess.CalledProcessError as err:
            self.logger.error(f"RETURN CODE: {err.returncode}")
            self.logger.error(f"{err.stderr}")
            self.logger.error(f"{EXITING_MSG}")
            sys.exit(err.returncode)

    def step_clean_up_workspace(self, tool_path: Path):
        """Clean up the Philosopher workspace.
        Command: philosopher workspace --clean --nocheck

        :param tool_path: Path to the Philosopher binary.
        """
        self.logger.info("Step: Cleaning up workspace ...")
        self.run_subprocess([f"{tool_path}", "workspace", "--clean", "--nocheck"])

    @touch_flag_files(step_name="init-workspace", item=2)
    def step_init_workspace(self, tool_path: Path, output_folder=None):
        """Initialise the Philosopher workspace.
        Command: philosopher workspace --init --nocheck

        :param tool_path: Path to the Philosopher binary.
        :param output_folder: This parameter is used within the touch_flag_files decorator.
        """
        self.logger.info("Step: Initialising workspace...")
        self.run_subprocess([f"{tool_path}", "workspace", "--init", "--nocheck"])

    @touch_flag_files(step_name="run-msfragger", item=4)
    def step_run_msfragger(
        self,
        config_file_path: Path,
        raw_files: List[str],
        tool_path: Path,
        output_folder=None,
    ):
        """
        Command:
            java -jar -Dfile.encoding=UTF-8 -Xmx217G ${MSFRAGGER} ${configs_dir}open_search.params ${raw_files[@]}

        :param config_file_path: Relative path to config file
        :param raw_files: List of raw files
        :param tool_path: Path to the MSFragger binary.
        :param output_folder: This parameter is used within the touch_flag_files decorator.
        """
        self.logger.info("Step: Running MSFragger...")
        self.run_subprocess(
            [
                "java",
                "-jar",
                "-Dfile.encoding=UTF-8",
                "-Xms512M",
                "-Xmx217G",
                "-XX:+UseG1GC",
                "-XX:MaxGCPauseMillis=200",
                "-XX:ParallelGCThreads=20",
                "-XX:ConcGCThreads=5",
                "-XX:InitiatingHeapOccupancyPercent=70",
                f"{tool_path}",
                f"{config_file_path}",
            ]
            + raw_files
        )

    @touch_flag_files(step_name="find-raw-files", item=3)
    def step_find_raw_files(
        self, raw_file_location_folder: Path, output_folder=None
    ) -> List[str]:
        """Please note that Path like objects will be converted into strings.

        :param raw_file_location_folder: Folder containing the RAW files downloaded from PRIDE.
        :param output_folder: This parameter is used within the touch_flag_files decorator.
        :return: List of identified file paths - string formatted.
        """
        self.logger.info("Step: Identifying RAW files...")
        result = [
            f"{item}"
            for item in raw_file_location_folder.iterdir()
            if item.is_file() and item.name.endswith(".raw")
        ]
        self.logger.debug(f"Found the following RAW files: {result}")
        return result

    def create_config_templates(self, source: Path, config_dir: str):
        self.logger.info("Creating configuration folder...")
        try:
            destination: Path = Path(config_dir)
            destination.mkdir(exist_ok=True)
            for source_file in source.iterdir():
                destination_file = destination / source_file.name
                destination_file.write_text(source_file.read_text())
        except FileNotFoundError or OSError as err:
            self.logger.error("Could NOT create new configuration folder!")
            raise err
        self.logger.info("Configuration folder successfully created.")

    def step_move_all_but_raw_files(self, source: Path, dst: Path):
        """Move all result files expect the RAW files to the provided destination.

        :param source: Source directory to look at for output files.
        :param dst: Destination, source files will be moved to
        """
        if not source.exists():
            self.logger.warning(
                f"Source file does not exist ({source}). Skipping moving of result files."
            )
            return
        if not dst.exists():
            self.logger.warning(
                f"Destination directory does not exist ({dst}). Skipping moving of result files."
            )
            return
        source_files: List[Path] = [
            item
            for item in source.iterdir()
            if item.is_file() and not item.name.endswith(".raw")
        ]
        num_result_files = len(source_files)
        if num_result_files > 0:
            self.logger.info(
                f"Step: Moving all {len(source_files)} result file(s) into folder {dst}"
            )
            for source_file in source_files:
                destination = dst / source_file.name
                if not destination.exists():
                    source_file.replace(destination)

    @touch_flag_files(step_name="run-crystalc", item=7)
    def step_run_crystalc(
        self,
        config_file_path: Path,
        pep_xml_files: List[Path],
        tool_paths: dict,
        output_folder=None,
    ):
        """
        Command:
            for raw_file in "${raw_files[@]}"
                $dry || java -Dlibs.thermo.dir=${MSFRAGGER_DIR}ext/thermo -Xmx217G -cp ${CRYSTALC}:${BATMASS_IO}:${GRPPR} crystalc.Run $crystalc_in $crystalc_out
            done

        :param config_file_path: Relative path to config file.
        :param pep_xml_files: List of pep_xml formatted files.
        :param tool_paths: Tool path dictionary.
        :param output_folder: This parameter is used within the touch_flag_files decorator.
        """
        self.logger.info("Step: Running CrystalC...")
        msfragger_dir: Path = tool_paths["msfragger-dir"]
        thermo_dir: Path = msfragger_dir / "ext" / "thermo"
        crystalc_jar: Path = tool_paths["crystalc"]
        batmass_io_jar: Path = tool_paths["batmass-io"]
        grppr_jar: Path = tool_paths["grppr"]
        for pep_xml_file in pep_xml_files:
            cmd = [
                "java",
                f"-Dlibs.thermo.dir={thermo_dir}",
                "-Dfile.encoding=UTF-8",
                "-Xms512M",
                "-Xmx6G",
                "-XX:+UseG1GC",
                "-XX:MaxGCPauseMillis=200",
                "-XX:ParallelGCThreads=20",
                "-XX:ConcGCThreads=5",
                "-XX:InitiatingHeapOccupancyPercent=70",
                "-cp",
                CLASSPATH_SEPARATOR.join(
                    [f"{batmass_io_jar}", f"{grppr_jar}", f"{crystalc_jar}"]
                ),
                "crystalc.Run",
                f"{config_file_path}",
                f"{pep_xml_file}",
            ]
            self.run_subprocess(cmd)

    @staticmethod
    def step_run_find_command(folder: Path, file_suffix: str) -> List[Path]:
        """Generic function for finding files with a specific suffix within the provided folder."""
        return [
            item
            for item in folder.iterdir()
            if item.is_file() and item.name.endswith(file_suffix)
        ]

    def step_run_find_by_pattern(self, folder: Path, pattern: str) -> List[Path]:
        """Find files by pattern in the provided folder.
        Here is an example: glob.glob('/app/test_data/PXD018591/*[0-9].pepXML')

        Please note that the glob() function expects a string and not a Path object.

        :return: List of files found with the specific pattern.
        :rtype: Path
        """
        result_files = glob.glob(str(folder / pattern))
        return [Path(item) for item in result_files]

    @touch_flag_files(step_name="find-msfragger-output", item=5)
    def step_find_msfragger_output_files(
        self, raw_file_location_folder: Path, output_folder=None
    ):
        """Find MSFragger output files.

        :param output_folder: This parameter is used within the touch_flag_files decorator.
        :return: 2 lists of files (TSV and pepXML formatted).
        :rtype: List, List
        """
        msfragger_tsv_files = self.step_run_find_command(
            folder=raw_file_location_folder, file_suffix=".tsv"
        )
        msfragger_pep_xml_files = self.step_run_find_by_pattern(
            folder=raw_file_location_folder, pattern="*[0-9].pepXML"
        )
        return msfragger_tsv_files, msfragger_pep_xml_files

    @touch_flag_files(step_name="run-peptideprophet", item=8)
    def step_run_peptideprophet(
        self,
        tool_path: Path,
        input_files: List[Path],
        fasta_input_file: Path,
        output_folder=None,
    ):
        """
        Command: philosopher peptideprophet --nonparam --expectscore --decoyprobs --masswidth 1000.0 --clevel -2 --decoy rev_ --database $database_name --combine

        :param tool_path: Path to the Philosopher binary file.
        :param input_files: List of CrystalC output files.
        :param fasta_input_file: Database input file, FASTA formatted.
        :param output_folder: This parameter is used within the touch_flag_files decorator.
        """
        self.logger.info("Step: Running PeptideProphet...")
        self.run_subprocess(
            [
                f"{tool_path}",
                "peptideprophet",
                "--nonparam",
                "--expectscore",
                "--decoyprobs",
                "--masswidth",
                "1000.0",
                "--clevel",
                "2",
                "--decoy",
                "rev_",
                "--database",
                f"{fasta_input_file}",
                "--combine",
            ]
            + [f"{item}" for item in input_files]
        )

    @touch_flag_files(step_name="rewrite_pepxml", item=9)
    def step_rewrite_pepxml(
        self,
        interact_path: Path,
        fragpipe_dir: Path,
        uncalibrated_mzml_files: List[Path],
        output_folder=None,
    ):
        """
        Command: java -cp ${fragpipe_dir}lib/* com.dmtavt.fragpipe.util.RewritePepxml $interact_path $uncalibrated_mzml_files

        :param interact_path: Interact file path.
        :param fragpipe_dir: fragpipe installation folder.
        :param tool_paths: Tool paths dictionary for looking up individual binary paths.
        :param output_folder: This parameter is used within the touch_flag_files decorator.
        """
        self.logger.info("Step: Running RewritePepxml...")
        self.run_subprocess(
            [
                "java",
                "-cp",
                f"{fragpipe_dir}/lib/*",
                "com.dmtavt.fragpipe.util.RewritePepxml",
                f"{interact_path}",
            ]
            + [f"{item}" for item in uncalibrated_mzml_files]
        )

    @touch_flag_files(step_name="run-protein-prophet", item=10)
    def step_run_protein_prophet(
        self, tool_path: Path, interact_path: Path, output_folder=None
    ):
        """
        Command: philosopher proteinprophet --maxppmdiff 2000000 --output combined $interact_path filelist_proteinprophet.txt

        :param tool_path: Path to the Philosopher binary file.
        :param interact_path: Interact file path.
        :param output_folder: This parameter is used within the touch_flag_files decorator.
        """
        self.logger.info("Step: Running ProteinProphet...")
        self.run_subprocess(
            [
                f"{tool_path}",
                "proteinprophet",
                "--maxppmdiff",
                "2000000",
                "--output",
                "combined",
                f"{interact_path}",
            ]
        )

    @touch_flag_files(step_name="run-db-annotate", item=11)
    def step_run_db_annotate(
        self, tool_path: Path, fasta_input_file: Path, output_folder=None
    ):
        """
        Command: philosopher database --annotate $database_name --prefix rev_

        :param tool_path: Path to the Philosopher binary file.
        :param fasta_input_file: Database input file, FASTA formatted.
        :param output_folder: This parameter is used within the touch_flag_files decorator.
        """
        self.logger.info("Step: Running DBannotate...")
        self.run_subprocess(
            [
                f"{tool_path}",
                "database",
                "--annotate",
                f"{fasta_input_file}",
                "--prefix",
                "rev_",
            ]
        )

    @touch_flag_files(step_name="run-filtering", item=12)
    def step_run_filtering(
        self,
        tool_path: Path,
        working_dir: Path,
        combined_path: Path,
        output_folder=None,
    ):
        """
        Command: philosopher filter --sequential --razor --prot 0.01 --mapmods --tag rev_ --pepxml $output_dir --protxml $combined_path

        :param tool_path: Path to the Philosopher binary file.
        :param working_dir: Path to the output folder.
        :param combined_path: Path to the combined file path (XML file).
        :param output_folder: This parameter is used within the touch_flag_files decorator.
        """
        self.logger.info("Step: Running PhilosopherFilter...")
        cmd = [
            f"{tool_path}",
            "filter",
            "--sequential",
            "--razor",
            "--prot",
            "0.01",
            "--mapmods",
            "--tag",
            "rev_",
            "--pepxml",
            f"{working_dir}",
            "--protxml",
            f"{combined_path}",
        ]
        self.run_subprocess(cmd)

    @touch_flag_files(step_name="run-report", item=13)
    def step_run_report(self, tool_path: Path, output_folder=None):
        """
        Command: philosopher report --decoys
        Please note that PhilosopherReport does not require any file specification.

        :param tool_path: Path to the Philosopher binary file.
        :param output_folder: This parameter is used within the touch_flag_files decorator.
        """
        self.logger.info("Step: Generating report...")
        self.run_subprocess([f"{tool_path}", "report", "--decoys"])

    def get_fragpipe_install_root_path(self, install_path: str) -> Path:
        """Determine the fragpipe root directory,
        e.g. if the given install_path is...
        deTEL/rTEL/tests/resources/binaries/fragpipe/bin
        then the install_path_root will be...
        deTEL/rTEL/tests/resources/binaries/fragpipe

        Please note, that this method should cater for Posix and Windows Paths.
        """
        self.logger.info("Step: Validating provided FragPipe installation folder...")
        install_path_p: Path = Path(install_path)
        if not install_path_p.exists():
            self.logger.error(
                f"Provided or configured FragPipe binary folder does not exist: {install_path_p}! {EXITING_MSG}"
            )
            sys.exit(1)
        fragpipe_binary_p: Path = install_path_p / "fragpipe"
        if not fragpipe_binary_p.exists():
            self.logger.error(
                f"Cannot find FragPipe executable file: {fragpipe_binary_p}! {EXITING_MSG}"
            )
            sys.exit(1)
        install_path_root: Path = install_path_p.parent
        child_dirs: list = [
            f"{child_dir.name}" for child_dir in install_path_root.iterdir()
        ]
        for expected_dir in ["bin", "lib", "tools"]:
            if f"{expected_dir}" not in child_dirs:
                self.logger.error(
                    f"Found invalid fragpipe installation folder! Could not find {expected_dir} subdirectory. {EXITING_MSG}"
                )
                sys.exit(1)
        self.logger.debug(
            f"Identified the following fragpipe installation root path: {install_path_root}"
        )
        return install_path_root

    def read_system_paths(
        self, system_paths_raw: str, keyword: str = "fragpipe"
    ) -> Path:
        """Parse fragpipe install path from system PATHS and return root install folder as a string.

        :param system_paths_raw: System PATH to parse.
        :param keyword: Defines the binary folder name to find in the system PATH.
        :return: fragpipe installation path
        """
        separated_system_paths: list[str] = system_paths_raw.split(sep=":")
        fragpipe_install_paths: list[str] = [
            item
            for item in separated_system_paths
            if keyword in item
            and Path(item).name == "bin"
            and keyword in f"{Path(item).parent}"
        ]
        if len(fragpipe_install_paths) == 0:
            self.logger.error(
                f"Could not find any fragpipe installation in your system PATH. Please make sure you have "
                f"fragpipe installed correctly! {EXITING_MSG}"
            )
            sys.exit(1)
        install_path: str = fragpipe_install_paths[0]
        install_path_root: Path = self.get_fragpipe_install_root_path(install_path)
        return install_path_root

    def determine_tool_paths(self, fragpipe_install_folder: Path) -> dict:
        """Determine all required tool paths, relative to the fragpipe install folder.

        :param fragpipe_install_folder: Fragpipe install folder.
        :return: A dictionary of tool names mapped to their absolute binary paths.
        """
        tools: dict = {}
        try:
            tools_folder: Path = fragpipe_install_folder / "tools"
            for item in tools_folder.iterdir():
                item_name: str = item.name.lower()
                if item.is_dir():
                    if "msfragger" in item_name:
                        tools["msfragger-dir"] = item
                        tools["msfragger-jar"] = item / f"{item.name}.jar"
                    elif "philosopher" in item_name:
                        tools["philosopher"] = item
                    elif "hipparchus" in item_name:
                        tools["hipparchus-core"] = item / f"{item.name}.jar".replace(
                            "-", "-core-"
                        )
                        tools["hipparchus-stat"] = item / f"{item.name}.jar".replace(
                            "-", "-stat-"
                        )
                    elif "ionquant" in item_name:
                        tools["ionquant"] = item / f"{item.name}.jar"
                    else:
                        pass
                elif item.is_file():
                    if "crystalc" in item_name:
                        tools["crystalc"] = item
                    elif "batmass-io" in item_name:
                        tools["batmass-io"] = item
                    elif "grppr" in item_name:
                        tools["grppr"] = item
                    elif "ptmshepherd" in item_name:
                        tools["ptmshepherd"] = item
                    elif "commons-math3" in item_name:
                        tools["commons-math3"] = item
                    elif "jfreechart" in item_name:
                        tools["jfreechart"] = item
                    else:
                        pass
        except FileNotFoundError:
            self.logger.error("Could not find FragPipe's tool directory.")
            raise

        return tools

    def tool_version_updated(self, tool_paths: dict) -> bool:
        """Check if tool versions have been updated."""
        if len(tool_paths) == 0:
            self.logger.error(
                f"Could not determine any tools paths in the fragpipe installation folder! {EXITING_MSG}"
            )
            sys.exit(1)
        is_version_updated: bool = False
        for tool_name, expected_ver in EXPECTED_TOOL_VERSIONS.items():
            tool_path = tool_paths.get(tool_name)
            if not tool_path:
                self.logger.error(
                    f"Could not determine a valid tool path for tool {tool_name}!"
                )
                if any(
                    name == tool_name
                    for name in [
                        "msfragger-jar",
                        "philosopher",
                        "ptmshepherd",
                        "ionquant",
                        "crystalc",
                    ]
                ):
                    logging.error(f"{EXITING_MSG}")
                    sys.exit(1)
                else:
                    pass
            if expected_ver not in f"{tool_path}":
                self.logger.warning(
                    f"The version of the {tool_name} tool has been updated from {expected_ver} to {tool_path}!"
                )
                is_version_updated = True
        return is_version_updated

    def initial_checks(
        self,
        fasta_input_file_path: Path,
        raw_file_location_folder: Path,
        tool_paths: dict,
        config_dir: Path,
    ):
        """Perform some initial checks of the provided input parameters. Exit the program if any of the
        essential checks fail.
        E.g. check the existence of the input database and the RAW file folder and
        the expected tool versions.

        :param fasta_input_file_path: Database input file, FASTA formatted.
        :param raw_file_location_folder: Folder containing the RAW files downloaded from PRIDE.
        :param tool_paths: Dictionary holding all fragpipe tool paths.
        :param config_dir: Configuration directory containing config files for various tools.
        """
        self.logger.info("Step: Running initial checks...")
        if not fasta_input_file_path.exists():
            self.logger.error(
                f"Provided input database file does not exist! Please provide correct path. {EXITING_MSG}"
            )
            sys.exit(1)
        elif not fasta_input_file_path.is_file():
            self.logger.error(
                f"Provided input database file is NOT a file object! {EXITING_MSG}"
            )
            sys.exit(1)
        elif not raw_file_location_folder.exists():
            self.logger.error(
                f"Provided RAW file location folder does not exist! Please provide correct path. {EXITING_MSG}"
            )
            sys.exit(1)
        elif not raw_file_location_folder.is_dir():
            self.logger.error(
                f"Provided RAW file location folder is NOT a directory object! {EXITING_MSG}"
            )
            sys.exit(1)
        elif not config_dir.exists():
            self.logger.error(
                f"Provided config folder does not exist! Please provide correct path. {EXITING_MSG}"
            )
            sys.exit(1)
        elif not config_dir.is_dir():
            self.logger.error(
                f"Provided config folder is NOT a directory object! {EXITING_MSG}"
            )
            sys.exit(1)
        elif self.tool_version_updated(tool_paths):
            self.logger.warning(
                "Your fragpipe installation contains upgraded tool versions, which have NOT been tested by us!"
            )
            self.logger.warning(
                "The program will still continue with the analysis, but without any warranty."
            )
        else:
            self.logger.info("All initial checks passed successfully!")

    @touch_flag_files(step_name="run-ptm-shepherd", item=15)
    def step_run_ptm_shepherd(
        self, config_file_path, tool_paths: dict, output_folder=None
    ):
        """
        Command: java -Dlibs.thermo.dir=${MSFRAGGER_DIR}ext/thermo -cp ${PTMSHEPHERD}:${BATMASS_IO}:${COMMONS_MATH}:${HIPPARCHUS} edu.umich.andykong.ptmshepherd.PTMShepherd ${configs_dir}shepherd.config

        :param config_file_path: Relative path to config file.
        :param tool_paths: Tool path dictionary.
        :param output_folder: This parameter is used within the touch_flag_files decorator.
        """
        self.logger.info("Step: Running PTMShepherd...")
        msfragger_dir: Path = tool_paths["msfragger-dir"]
        thermo_dir: Path = msfragger_dir / "ext" / "thermo"
        ptmshepherd_jar: Path = tool_paths["ptmshepherd"]
        batmass_io_jar: Path = tool_paths["batmass-io"]
        commons_math3_jar: Path = tool_paths["commons-math3"]
        hipparchus_core_jar: Path = tool_paths["hipparchus-core"]
        hipparchus_stat_jar: Path = tool_paths["hipparchus-stat"]
        self.run_subprocess(
            [
                "java",
                "-Xmx3G",
                f"-Dlibs.thermo.dir={thermo_dir}",
                "-cp",
                CLASSPATH_SEPARATOR.join(
                    [
                        f"{ptmshepherd_jar}",
                        f"{batmass_io_jar}",
                        f"{commons_math3_jar}",
                        f"{hipparchus_core_jar}",
                        f"{hipparchus_stat_jar}",
                    ]
                ),
                "edu.umich.andykong.ptmshepherd.PTMShepherd",
                f"{config_file_path}",
            ]
        )

    @touch_flag_files(step_name="run-ionquant", item=16)
    def step_run_ionquant(
        self,
        raw_file_location_folder: Path,
        psm_file_path: Path,
        num_threads: int,
        tool_paths: dict,
        output_folder=None,
    ):
        """
        Command: java -Xmx217G -Dlibs.bruker.dir=${MSFRAGGER_DIR}ext/bruker
        -Dlibs.thermo.dir=${MSFRAGGER_DIR}ext/thermo -cp ${IONQUANT}:${SMILE_CORE}:
        {SMILE_MATH}:${JAVACPP}:${BATMASS_IO} ionquant.IonQuant --threads $cores --ionmobility 0 --mbr 0
        --maxlfq 1 --requantify 1 --mztol 10 --imtol 0.05 --rttol 0.4 --mbrmincorr 0 --mbrrttol 1 --mbrimtol 0.05
        --mbrtoprun 100000 --ionfdr 0.01 --proteinfdr 1 --peptidefdr 1 --normalization 1 --minisotopes 2
        --minscans 3 --writeindex 0 --tp 3 --minfreq 0.5 --minions 2 --minexps 1 --locprob 0.75
        --psm $output_dir/psm.tsv --specdir $raw_folder

        :param raw_file_location_folder: Folder containing the RAW files downloaded from PRIDE.
        :param psm_file_path: PSM input file path.
        :param num_threads: Number of threads.
        :param tool_paths: Dictionary holding all fragpipe tool paths.
        :param output_folder: This parameter is used within the touch_flag_files decorator.
        """
        self.logger.info("Step: Running IonQuant...")
        msfragger_dir: Path = tool_paths["msfragger-dir"]
        thermo_dir: Path = msfragger_dir / "ext" / "thermo"
        bruker_dir: Path = msfragger_dir / "ext" / "bruker"
        ionquant_jar: Path = tool_paths["ionquant"]
        batmass_io_jar: Path = tool_paths["batmass-io"]
        required_jars: List[str] = [f"{ionquant_jar}", f"{batmass_io_jar}"]
        #
        jfreechart_jar: Path = tool_paths.get("jfreechart", None)
        if not jfreechart_jar:
            self.logger.error(
                f"Could not find jfreechart library. Java library jfreechart is required to run "
                f"this version of IonQuant: {ionquant_jar}. Skipping IonQuant step now."
            )
            return
        class_path: str = CLASSPATH_SEPARATOR.join(
            required_jars + [f"{jfreechart_jar}"]
        )
        cmd = [
            "java",
            "-Xms512M",
            "-Xmx217G",
            "-XX:+UseG1GC",
            "-XX:MaxGCPauseMillis=200",
            "-XX:ParallelGCThreads=20",
            "-XX:ConcGCThreads=5",
            "-XX:InitiatingHeapOccupancyPercent=70",
            f"-Dlibs.bruker.dir={bruker_dir}",
            f"-Dlibs.thermo.dir={thermo_dir}",
            "-cp",
            class_path,
            "ionquant.IonQuant",
            "--threads",
            f"{num_threads}",
            "--ionmobility",
            "0",
            "--mbr",
            "0",
            "--maxlfq",
            "1",
            "--requantify",
            "1",
            "--mztol",
            "10",
            "--imtol",
            "0.05",
            "--rttol",
            "0.4",
            "--mbrmincorr",
            "0",
            "--mbrrttol",
            "1",
            "--mbrimtol",
            "0.05",
            "--mbrtoprun",
            "100000",
            "--ionfdr",
            "0.01",
            "--proteinfdr",
            "1",
            "--peptidefdr",
            "1",
            "--normalization",
            "1",
            "--minisotopes",
            "2",
            "--minscans",
            "3",
            "--writeindex",
            "0",
            "--tp",
            "3",
            "--minfreq",
            "0.5",
            "--minions",
            "2",
            "--minexps",
            "1",
            "--locprob",
            "0.75",
            "--psm",
            f"{psm_file_path}",
            "--specdir",
            f"{raw_file_location_folder}",
        ]
        self.run_subprocess(cmd)

    def prepare_path(self, input_path: str):
        """Turns relative paths into absolute paths using the current working directory"""
        if not os.path.isabs(input_path):
            return self.cwd / input_path
        return Path(input_path)


if __name__ == "__main__":
    instance = OpenSearchRunner()
    instance.run(sys.argv[1:])
