import argparse
import collections as clt
import logging
import os
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from Bio import SeqIO
from jinja2 import Environment, FileSystemLoader

from deTEL.eTEL import CsvFileOutputColumnNames
from deTEL.eTEL.workflow import (
    CODON_COUNTS_TABLE_COLUMN_NAMES_DICT,
    CODON_COUNTS_TABLE_COLUMN_NAMES_LIST,
)
from deTEL.eTEL.workflow.dataset_report import (
    plot_codon_counts,
    plot_hyperscore_distribution,
    plot_peptide_hist,
)
from deTEL.eTEL.workflow.extract_peptides import extract_peptides
from deTEL.eTEL.workflow.global_report import generate_global_report
from deTEL.eTEL.workflow.substitution_report import generate_substitution_report
from deTEL.eTEL.workflow.utils import (
    codonify,
    get_amino_acids,
    get_codons,
    invert_codon_table,
    list_raw_files,
    list_tsv_files,
)
from deTEL.utils import is_valid_file, prep_folder

ABSOLUTE_SCRIPT_PATH = Path(os.path.dirname(os.path.realpath(__file__)))

logger = logging.getLogger(__name__)


def count_observed_codons(dp: pd.DataFrame, cds_dict: dict):
    codon_counts = clt.Counter()
    proteinID = np.array(dp["Protein"], dtype=str)
    peptideStartPos = np.array(dp["Protein Start"], dtype=int) - 1
    peptideEndPos = np.array(dp["Protein End"], dtype=int)
    for i in range(0, len(proteinID)):
        sequence = cds_dict[proteinID[i]]
        codon_seq = codonify(sequence.seq)

        codon_peptide = codon_seq[peptideStartPos[i] : peptideEndPos[i]]
        codon_counts.update(clt.Counter(codon_peptide))

    return codon_counts


def get_mass_substitution_dict():
    """
    output: Dictionary of amino acid (key) mass differences (value)
    """
    aa_mass = {
        "G": 57.02147,
        "A": 71.03712,
        "S": 87.03203,
        "P": 97.05277,
        "V": 99.06842,
        "T": 101.04768,
        "I": 113.08407,
        "L": 113.08407,
        "N": 114.04293,
        "D": 115.02695,
        "Q": 128.05858,
        "K": 128.09497,
        "E": 129.0426,
        "M": 131.04049,
        "H": 137.05891,
        "F": 147.06842,
        "R": 156.10112,
        "C": 160.030654,  # CamCys
        "Y": 163.0633,
        "W": 186.07932,
        "*": 71.03712,
    }

    subs_dict_complete = {
        i + " to " + j: aa_mass[j] - aa_mass[i]
        for i in aa_mass
        for j in aa_mass
        if i != j
    }
    del subs_dict_complete["L to I"]
    del subs_dict_complete["I to L"]

    subs_dict_complete = {k: v for k, v in subs_dict_complete.items() if k[-1] != "L"}
    subs_dict = clt.defaultdict(int)
    for k, v in subs_dict_complete.items():  # unifies I and L
        if k[-1] == "I":
            subs_dict[k + "/L"] = v
        else:
            subs_dict[k] = v

    return subs_dict


def mark_danger_mods(dp, dm, mass_tol=0.005):
    aas = list("ACDEFGHIKLMNPQRSTVWY")

    dp["danger"] = False
    for mod in dm.iterrows():
        mod = mod[1]
        position = mod["position"]
        site = mod["site"]
        delta_m = mod["delta_m"]

        mass_filter = (delta_m - (2 * mass_tol) < dp["Delta Mass"]) & (
            dp["Delta Mass"] < delta_m + (2 * mass_tol)
        )

        site_filter = True
        if site in aas:
            site_filter = dp.modAA.str.contains(site)

        term_filter = True
        if position == "Protein N-term":
            term_filter = dp.is_prot_nterm
        elif position == "Protein C-term":
            term_filter = dp.is_prot_cterm
        elif position == "Any N-term":
            term_filter = dp.is_peptide_nterm
        elif position == "Any C-term":
            term_filter = dp.is_peptide_cterm

        dp.loc[site_filter & term_filter & mass_filter, "danger"] = True

    return dp


def define_near_cognate_mask(codons, aas, i_codon_table):
    """
    Create mask for mis-pairing. A binary dataframe indicating for each codon the AAs encoded by near-cognate codons.
    """

    def hamming(s1, s2):
        return sum(a != b for a, b in zip(s1, s2))

    AMINO_ACIDS = "ACDEFGHKLMNPQRSTVWY*"
    mask = pd.DataFrame(
        data=False, index=codons, columns=list(AMINO_ACIDS), dtype=float
    )
    for label in codons:
        near_cognates = np.array([hamming(i, label) == 1 for i in codons])
        reachable_aa = set(np.array(list(aas))[near_cognates])
        mask.loc[label] = [i in reachable_aa for i in AMINO_ACIDS]

    for label in mask.index:  # removes "near-cognates" that encodes the same AA
        for col in mask.columns:
            if label in i_codon_table[col]:
                mask.loc[label, col] = float("NaN")

    return mask.rename(columns={"L": "I/L"})


def mark_substitutions(peptide_df, mass_diff_dict, tolerance):
    peptide_df["substitution"] = False
    for i in sorted(mass_diff_dict.keys()):
        delta_m = mass_diff_dict[i]
        original_aa = i[0]
        peptide_df.loc[
            (peptide_df["Delta Mass"] > (delta_m - tolerance))
            & (peptide_df["Delta Mass"] < (delta_m + tolerance))
            & (peptide_df["modAA"] == original_aa)
            & ~peptide_df["danger"],
            "substitution",
        ] = i
    return peptide_df


def peptide_in_proteome(peptide, proteome):
    return any([id for id, seq in proteome.items() if peptide in str(seq.seq)])


def prepare(psm, dm_mass_tol, decoy, cds_names):
    psm = psm.loc[psm["Is Unique"], :].copy()
    psm["is_decoy"] = psm["Protein"].map(lambda p: re.search(decoy, p) is not None)
    psm["is_contaminant"] = psm["Protein"].map(lambda p: p not in cds_names)
    psm.query("not is_decoy and not is_contaminant", inplace=True)
    psm["Delta Mass"] = psm["Delta Mass"].astype(float)
    psm["zero_shift_peptide"] = psm["Delta Mass"].map(
        lambda dm: (dm < dm_mass_tol) and (dm > -dm_mass_tol)
    )
    psm["is_prot_nterm"] = psm["Prev AA"].map(lambda x: x == "-")
    psm["is_prot_cterm"] = psm["Next AA"].map(lambda x: x == "-")

    psm.loc[psm["MSFragger Localization"].isna(), "MSFragger Localization"] = ""
    psm["MSFragger Localization"] = psm["MSFragger Localization"].astype(str)

    psm["n_matched_pos"] = psm["MSFragger Localization"].map(
        lambda loc: len(re.findall("[a-z]", loc))
    )
    psm.query("n_matched_pos <= 1", inplace=True)
    psm = psm.loc[
        ~(
            (psm["n_matched_pos"] == 1)
            & (psm["Delta Mass"] < dm_mass_tol)
            & (psm["Delta Mass"] > -dm_mass_tol)
        ),
        :,
    ]

    def localize_mod(loc):
        x = re.search("[a-z]", loc)
        return x.span()[0] if x is not None else -1

    psm["mod_loc_in_peptide"] = psm["MSFragger Localization"].map(localize_mod)

    def get_mod_aa(loc):
        x = re.findall("[a-z]", loc)
        return x[0].upper() if len(x) > 0 else ""

    psm["modAA"] = psm["MSFragger Localization"].map(get_mod_aa)
    psm["Protein Start"] = psm["Protein Start"].astype(int)
    psm["mod_loc_in_protein"] = psm["mod_loc_in_peptide"] + psm["Protein Start"]
    psm["is_peptide_nterm"] = psm["mod_loc_in_peptide"] == 0
    psm["is_peptide_cterm"] = (psm["mod_loc_in_peptide"] + 1) == psm["Peptide Length"]
    psm["raw_file"] = [
        s[0 : re.search("\.\d+\.\d+\.\d\Z", s).span()[0]] for s in psm.index
    ]

    return psm


def fetch_substituted_codon(row, cds_dict):
    mod_loc = row.mod_loc_in_protein
    prot = row.Protein

    codon = "NaN"
    if (not row.is_decoy) & (prot in cds_dict.keys()):
        sequence = cds_dict[prot]
        codon_seq = codonify(sequence.seq)
        codon = codon_seq[mod_loc - 1]

    return codon


def parse_args(args):
    """Parse and retrieve input arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        dest="fasta",
        required=True,
        help="search database as codon fasta file",
        metavar="FILE",
        type=lambda x: is_valid_file(parser, x),
    )
    parser.add_argument(
        "-psm",
        dest="psm",
        required=True,
        help="psm.tsv produced by philosopher",
        metavar="FILE",
    )
    parser.add_argument(
        "-s",
        dest="open_search_output",
        required=True,
        help="Absolute path to the open_search/rTEL output folder.",
        metavar="DIR",
    )
    parser.add_argument(
        "-o",
        dest="output_folder",
        required=True,
        help="Output folder",
        metavar="FILE",
        type=lambda x: prep_folder(x),
    )
    parser.add_argument(
        "-decoy",
        dest="decoy",
        required=False,
        help="decoy prefix (default: rev_)",
        default="rev_",
    )
    parser.add_argument(
        "-p",
        dest="prefix",
        required=False,
        help="prefix for experiment naming",
        default="substitutions",
    )
    parser.add_argument(
        "-tol",
        dest="tol",
        required=False,
        help="m/z tolerance, used to filter DP–BP couples that resemble substitutions "
        "and exclude pairs that resemble known PTM (default: 0.005)",
        default=0.005,
        type=float,
    )
    parser.add_argument(
        "-gr",
        "--generate-report",
        default=False,
        help="Option to generate a full dataset report.",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Turns on verbosity.",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "-r",
        dest="raw_file_location",
        help="Mass spec RAW file location (optional). Please note that, by default eTEL expects the RAW files to "
             "be present in the parent folder of the given open search output folder (-s option).",
        metavar="DIR",
    )
    return parser.parse_args(args), parser


class ETelRunner(object):
    def __init__(self):
        file_handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s: %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    def run(self, args):
        """Main function."""
        args, parser = parse_args(args)
        if args.verbose:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        logger.info("Running eTEL workflow...")

        tic_total = time.perf_counter()
        logger.info(
            "----Setup-----------------------------------------------------------"
        )
        logger.info(f"FASTA database file: {args.fasta}")
        logger.info(f"PSM file: {args.psm}")
        logger.info(f"decoy prefix: {args.decoy}")
        logger.info(f"Output folder: {args.output_folder}")
        logger.info(f"Output file prefix: {args.prefix}")
        logger.info(f"M/Z tolerance: {args.tol}")
        # Please note: The assumption made is that the open_search output folder will always be written into the RAW file folder by open_search
        raw_file_folder_path: Path = (
            Path(args.raw_file_location)
            if args.raw_file_location
            else Path(args.open_search_output).parent
        )
        logger.info(f"Raw file location: {raw_file_folder_path}")
        logger.info(
            "--------------------------------------------------------------------"
        )

        # to be set via command line arguments
        delta_mass_tolerance = args.tol  # 0.005
        cds_file: str = args.fasta  #
        psm_file = args.psm  # 'input/PXD025934_fragpipe/pepXML'
        output_folder = args.output_folder  # 'output/PXD025934_fragpipe/'
        decoy_prefix = args.decoy
        output_prefix = args.prefix
        open_search_output_path = Path(args.open_search_output)

        ms_diff_dict = get_mass_substitution_dict()
        codons = get_codons()
        amino_acids = get_amino_acids()
        codon_table = dict(zip(codons, amino_acids))
        inverted_codon_table = invert_codon_table(codon_table)
        inverted_codon_table["L"] = (
            inverted_codon_table["L"] + inverted_codon_table["I"]
        )

        logger.info("Reading sequences...")
        tic = time.perf_counter()
        cds_dict = SeqIO.to_dict(SeqIO.parse(cds_file, "fasta"))
        logger.info(f"Number of sequence(s) in database: {len(cds_dict)}")
        toc = time.perf_counter()
        logger.info(f"Sequences reading finished in {toc - tic:0.4f} seconds.")

        logger.info("Reading and preparing PSM file...")
        tic = time.perf_counter()
        psm_df = pd.read_csv(psm_file, sep="\t", index_col=0)
        psm_df = prepare(
            psm_df,
            dm_mass_tol=delta_mass_tolerance,
            decoy=decoy_prefix,
            cds_names=cds_dict.keys(),
        )
        toc = time.perf_counter()
        logger.info(f"PSM file preparation finished in {toc - tic:0.4f} seconds.")

        logger.info("Running substitution detection...")
        tic = time.perf_counter()
        p = Path(__file__).with_name("danger_mods.csv")
        danger_mods = pd.read_csv(p)

        logger.info("Marking dangerous PTMs...")
        psm_df = mark_danger_mods(psm_df, danger_mods, mass_tol=delta_mass_tolerance)
        psm_df = mark_substitutions(psm_df, ms_diff_dict, delta_mass_tolerance)
        psm_subs = self.retain_subs_with_basepeptide(psm_df)

        near_cognate_mask = define_near_cognate_mask(
            codons, amino_acids, inverted_codon_table
        )

        psm_subs["codon"] = psm_subs.apply(
            lambda row: fetch_substituted_codon(row, cds_dict), axis=1
        )
        psm_subs["origin"] = psm_subs["substitution"].map(lambda x: x.split(" ")[0])
        psm_subs["destination"] = psm_subs["substitution"].map(
            lambda x: x.split(" ")[2]
        )
        psm_subs["near_cognate"] = psm_subs.apply(
            lambda row: near_cognate_mask.loc[row["codon"], row["destination"]], axis=1
        )

        psm_subs = psm_subs[
            [
                "Protein",
                "Peptide",
                "raw_file",
                "MSFragger Localization",
                "Prev AA",
                "Next AA",
                "Charge",
                "Retention",
                "Calculated Peptide Mass",
                "PeptideProphet Probability",
                "Delta Mass",
                "Protein Start",
                "Protein End",
                "mod_loc_in_protein",
                "codon",
                "origin",
                "destination",
                "substitution",
                "near_cognate",
                "Intensity",
                "avg_base_intensity",
            ]
        ]

        psm_subs.rename(
            columns={
                "Protein": CsvFileOutputColumnNames.PROTEIN,
                "Peptide": "peptide",
                "raw_file": CsvFileOutputColumnNames.RAW_FILE,
                "MSFragger Localization": "modified_peptide",
                "Prev AA": "prev_aa",
                "Next AA": "next_aa",
                "Charge": "charge",
                "Retention": "retention",
                "Calculated Peptide Mass": "calculated_peptide_mass",
                "PeptideProphet Probability": "peptide_prophet_probability",
                "Delta Mass": "delta_mass",
                "Protein Start": "protein_start",
                "Protein End": "protein_end",
                "mod_loc_in_protein": CsvFileOutputColumnNames.LOCALIZATION_IN_PROTEIN,
                "Intensity": CsvFileOutputColumnNames.INTENSITY,
                "avg_base_intensity": "avg_base_intensity",
            },
            inplace=True,
        )
        psm_subs.index.name = "spectrum"

        psm_subs = psm_subs.astype(
            {
                CsvFileOutputColumnNames.PROTEIN: str,
                "peptide": str,
                CsvFileOutputColumnNames.RAW_FILE: str,
                "modified_peptide": str,
                "prev_aa": str,
                "next_aa": str,
                "charge": int,
                "retention": float,
                "calculated_peptide_mass": float,
                "peptide_prophet_probability": float,
                "delta_mass": float,
                "protein_start": int,
                "protein_end": int,
                CsvFileOutputColumnNames.LOCALIZATION_IN_PROTEIN: int,
                "codon": str,
                "origin": str,
                "destination": str,
                "substitution": str,
                "near_cognate": bool,
                CsvFileOutputColumnNames.INTENSITY: float,
                "avg_base_intensity": float,
            }
        )

        toc = time.perf_counter()
        logger.info(f"Detected {psm_subs.shape[0]} substitutions.")
        logger.info(f"Substitution detection finished in {toc - tic:0.4f} seconds.")

        logger.info("Calculating protein and peptide error rates...")
        tic = time.perf_counter()
        psm_subs["intensity_based_error_rate"] = psm_subs[
            CsvFileOutputColumnNames.INTENSITY
        ] / (
            psm_subs[CsvFileOutputColumnNames.INTENSITY]
            + psm_subs["avg_base_intensity"]
        )
        # peptide count
        psm_pc = pd.DataFrame.from_dict(clt.Counter(psm_df["Protein"]), orient="index")
        psm_zs_pc = pd.DataFrame.from_dict(
            clt.Counter(psm_df.loc[psm_df["zero_shift_peptide"], "Protein"]),
            orient="index",
        )
        psm_subs_pc = pd.DataFrame.from_dict(
            clt.Counter(psm_subs[CsvFileOutputColumnNames.PROTEIN]), orient="index"
        )
        psm_pc = psm_pc.join(psm_zs_pc, lsuffix="Total", rsuffix="zero_shift")
        psm_pc = psm_pc.join(psm_subs_pc, lsuffix="Total", rsuffix="subs")
        psm_pc["Error_rate"] = psm_pc[0] / psm_pc["0Total"]
        psm_pc["ZS_Error_rate"] = psm_pc[0] / psm_pc["0zero_shift"]
        psm_pc = psm_pc.reset_index()
        psm_pc.fillna(0, inplace=True)
        psm_pc.columns = [
            CsvFileOutputColumnNames.PROTEIN,
            CsvFileOutputColumnNames.TOTAL,
            "no_mass_shift",
            CsvFileOutputColumnNames.ERRONEOUS,
            "total_error_rate",
            "no_mass_shift_error_rate",
        ]
        psm_pc.drop(["no_mass_shift", "no_mass_shift_error_rate"], axis=1, inplace=True)

        # codon counting
        base_codon_count = count_observed_codons(psm_df, cds_dict)
        basepeptide_codon_count = pd.DataFrame.from_dict(
            base_codon_count, orient="index"
        )
        subs_codon_count = pd.DataFrame.from_dict(
            clt.Counter(psm_subs["codon"]), orient="index"
        )
        total_codon_count = basepeptide_codon_count.join(
            subs_codon_count, lsuffix="base", rsuffix="substitution"
        )
        total_codon_count["error_rate"] = (
            total_codon_count["0substitution"] / total_codon_count["0base"]
        )
        total_codon_count = total_codon_count.reset_index()
        total_codon_count.fillna(0, inplace=True)
        total_codon_count.columns = CODON_COUNTS_TABLE_COLUMN_NAMES_LIST
        psm_cc = total_codon_count.astype(CODON_COUNTS_TABLE_COLUMN_NAMES_DICT)
        toc = time.perf_counter()
        logger.info(
            f"The calculation of protein and peptide error rates finished in {toc - tic:0.4f} seconds."
        )

        substitution_errors_file_name = f"{output_prefix}_substitution_errors"
        codon_counts_file_name = f"{output_prefix}_codon_counts"
        peptide_counts_file_name = f"{output_prefix}_peptide_counts"
        csv_ext = ".csv"
        psm_subs.to_csv(
            os.path.join(output_folder, f"{substitution_errors_file_name}{csv_ext}")
        )
        psm_cc.to_csv(os.path.join(output_folder, f"{codon_counts_file_name}{csv_ext}"))
        psm_pc.to_csv(
            os.path.join(output_folder, f"{peptide_counts_file_name}{csv_ext}")
        )

        if args.generate_report:
            logger.info("Report generation activated.")
            list_of_raw_files: list[str] = list_raw_files(raw_file_folder_path)
            if len(list_of_raw_files) == 0:
                raise FileNotFoundError(
                    f"Could not find any RAW input files under: {raw_file_folder_path}"
                )
            tsv_files = list_tsv_files(open_search_output_path, list_of_raw_files)
            if len(tsv_files) == 0:
                raise FileNotFoundError(
                    f"Could not find any TSV RAW output files under: {raw_file_folder_path}"
                )
            psm_data = pd.DataFrame()
            for tsv_file in tsv_files:
                tmp_base = pd.read_csv(
                    tsv_file, sep="\t", header=0, usecols=["protein", "hyperscore"]
                )
                psm_data = pd.concat([psm_data, tmp_base])
            self.generate_report(
                output_folder,
                output_prefix,
                psm_cc,
                codon_counts_file_name,
                psm_pc,
                peptide_counts_file_name,
                psm_data,
                raw_file_folder_path,
                psm_subs,
                cds_file,
            )

        toc_total = time.perf_counter()
        logger.info(f"eTEL finished in {toc_total - tic_total:0.4f} seconds.")

    @staticmethod
    def generate_report(
        etel_output_path,
        dataset_id,
        psm_codon_counts,
        codon_counts_file_name,
        psm_peptide_counts,
        peptide_counts_file_name,
        psm_data,
        raw_file_folder_path: Path,
        psm_subs: pd.DataFrame,
        cds_file_path: str,
    ):
        logger.info("Generating report...")
        report_output_path: Path = Path(etel_output_path) / "report"
        report_output_path.mkdir(parents=True, exist_ok=True)
        #
        png_ext = ".png"
        plot_codon_counts(
            codon_counts=psm_codon_counts,
            output_file_path=report_output_path / f"{codon_counts_file_name}{png_ext}",
        )
        plot_peptide_hist(
            psm_peptide_counts,
            output_file_path=report_output_path
            / f"{peptide_counts_file_name}{png_ext}",
        )

        plot_hyperscore_distribution(
            psm_data=psm_data,
            output_file_path=report_output_path
            / f"{dataset_id}_hyperscore_distribution{png_ext}",
        )

        peptides: list = extract_peptides(raw_file_folder_path, psm_subs, logger)
        peptides_to_render = generate_substitution_report(peptides, dataset_id, logger)
        generate_global_report(
            Path(etel_output_path),
            report_output_path,
            cds_file_path,
            dataset_id=dataset_id,
            parent_logger=logger,
        )

        # HTML Template creation
        file_loader = FileSystemLoader(ABSOLUTE_SCRIPT_PATH / "templates")
        env = Environment(loader=file_loader)
        template = env.get_template("substitution_report.html")
        output = template.render(
            raw_folder=dataset_id,
            peptides=peptides_to_render,
            pxds=[{"name": dataset_id.rstrip("\n")}],
        )

        html_file_path: Path = Path(report_output_path) / f"{dataset_id}.html"
        with open(f"{html_file_path}", "w") as html_file:
            html_file.write(output)

        logger.info("Report generation finished.")

    @staticmethod
    def retain_subs_with_basepeptide(psm):
        subs = psm.query("substitution != False and danger == False").copy()
        base_peptide_df = psm.query(
            "substitution == False and danger == False and zero_shift_peptide"
        )
        logger.info(f"Identified {base_peptide_df.shape[0]} base peptides.")

        def is_in(x, base_df) -> bool:
            return (
                base_df.loc[
                    (base_df["Protein"] == x.Protein)
                    & (base_df["raw_file"] == x.raw_file)
                    & (base_df["Protein Start"] < x.mod_loc_in_protein)
                    & (base_df["Protein End"] > x.mod_loc_in_protein),
                    :,
                ].shape[0]
                > 0
            )

        def get_avg_base_intensity(x, base_df) -> float:
            """Calculates average base intensity over all peptides matching substitutions provided as x"""
            return base_df.loc[
                (base_df["Protein"] == x.Protein)
                & (base_df["raw_file"] == x.raw_file)
                & (base_df["Protein Start"] < x.mod_loc_in_protein)
                & (base_df["Protein End"] > x.mod_loc_in_protein),
                "Intensity",
            ].mean()

        subs["base_peptide_exists"] = subs.apply(
            lambda row: is_in(row, base_peptide_df), axis=1
        )
        subs["avg_base_intensity"] = subs.apply(
            lambda row: get_avg_base_intensity(row, base_peptide_df), axis=1
        )
        return subs.query("base_peptide_exists")


if __name__ == "__main__":
    instance = ETelRunner()
    instance.run(sys.argv[1:])
