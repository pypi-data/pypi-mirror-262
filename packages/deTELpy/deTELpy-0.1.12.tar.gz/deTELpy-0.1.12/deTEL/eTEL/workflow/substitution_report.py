import logging
import time

import spectrum_utils.iplot as iplot
import spectrum_utils.spectrum as spectrum

logger = logging.getLogger(__name__)


def replacer(s, newstring, index, nofail=False):
    # raise an error if index is outside of the string
    if not nofail and index not in range(len(s)):
        raise ValueError("index outside given string")
    # if not erroring, but the index is still not in the correct range
    if index < 0:  # add it to the beginning
        return newstring + s
    if index > len(s):  # add it to the end
        return s + newstring
    # insert the new string between "slices" of the original
    return s[:index] + newstring + s[index + 1 :]


def generate_substitution_report(
    extracted_peptides: list,
    output_prefix: str,
    parent_logger=None,
):
    if parent_logger:
        init_logger(
            log_level=parent_logger.level, file_handler=parent_logger.handlers[0]
        )
    logger.info("Generating substitution report...")
    tic = time.perf_counter()
    spectrum.static_modification("C", 57.021464)
    peptides_to_render = []
    for extracted_peptide in extracted_peptides:
        rawfile_name = extracted_peptide["rawfile_name"]

        peak_list = extracted_peptide["peak_list"]
        retention_time = extracted_peptide["retention_time"]
        precursor_mz = extracted_peptide["precursor_mass"]
        precursor_charge = extracted_peptide["precursor_charge"]

        peptide, modifications = extracted_peptide["peptide"], {}
        spectrum_data = spectrum.MsmsSpectrum(
            "Modified",
            precursor_mz,
            precursor_charge,
            [x[0] for x in peak_list],
            [x[1] for x in peak_list],
            peptide=peptide,
            retention_time=retention_time,
            modifications=modifications,
        )

        org = extracted_peptide["origin"]
        dest = extracted_peptide["destination"]
        loc = extracted_peptide["mod_loc"]

        peptide = replacer(peptide, f"[{org}\u279D{dest}]", loc)

        chart = iplot.spectrum(
            spectrum_data.annotate_peptide_fragments(0.5, "Da", ion_types="by")
        ).properties(width=640, height=400, title=peptide)

        jsonSpec = chart.to_json()

        outputFile = (
            output_prefix
            + "_"
            + rawfile_name
            + "_"
            + str(extracted_peptide["scan_number"])
        )
        peptides_to_render.append(
            {
                "rawfile_name": rawfile_name,
                "outputFile": outputFile,
                "scanNo": extracted_peptide["scan_number"],
                "peptide": extracted_peptide["peptide"],
                "jsonSpec": jsonSpec,
            }
        )

    toc = time.perf_counter()
    logger.info(f"Finished substitution report in {toc - tic:0.4f} seconds.")
    return peptides_to_render


def init_logger(log_level, file_handler=None):
    if not file_handler:
        file_handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s: %(message)s")
        file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(log_level)
