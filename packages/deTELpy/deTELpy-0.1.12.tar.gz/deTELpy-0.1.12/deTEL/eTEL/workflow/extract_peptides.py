import logging
import time
from pathlib import Path

import matplotlib
import pandas as pd

from deTEL.eTEL import CsvFileOutputColumnNames

matplotlib.use("Agg")


logger = logging.getLogger(__name__)


def extract_peptides(
    raw_file_folder_path: Path, psm_subs: pd.DataFrame, parent_logger=None
) -> list:
    tic = time.perf_counter()
    if parent_logger:
        init_logger(
            log_level=parent_logger.level, file_handler=parent_logger.handlers[0]
        )
    logger.info("Extracting peptides...")
    logger.debug(f"RAW file folder: {raw_file_folder_path}")
    peptides = []

    raw_file_paths: list[Path] = [
        item
        for item in raw_file_folder_path.iterdir()
        if item.is_file() and ".raw" in item.name
    ]
    raw_file_paths_d: dict = {
        raw_file_path.name: raw_file_path for raw_file_path in raw_file_paths
    }
    grouped_by_raw_file = psm_subs.groupby(CsvFileOutputColumnNames.RAW_FILE)
    import ms_deisotope
    for name, group in grouped_by_raw_file:
        raw_file_name: str = f"{name}.raw"
        raw_file_path: str = raw_file_paths_d.get(raw_file_name)
        logger.info(f"Reading RAW file {raw_file_path}...")
        reader = ms_deisotope.MSFileLoader(f"{raw_file_path}")
        logger.info(f"Finished raw file reading.")

        for index, row in group.iterrows():
            spectrum: str = str(index)
            scan_num: str = spectrum.split(".")[1]
            pep = {
                "rawfile_name": f"{name}",
                "scan_number": int(scan_num),
                "precursor_mass": row.calculated_peptide_mass,
                "precursor_charge": row.charge,
                "retention_time": row.retention,
                "origin": row.origin,
                "destination": row.destination,
                "peptide": row.modified_peptide,
                "mod_loc": int(row.localization_in_protein) - int(row.protein_start),
            }
            scan = reader.get_scan_by_id(scan_num)
            scan.pick_peaks()
            peak_list = []
            for peak in scan.peak_set.peaks:
                peak_list.append([peak.mz, peak.intensity])
            pep["peak_list"] = peak_list
            peptides.append(pep)
    toc = time.perf_counter()
    logger.info(f"Finished peptides extraction in {toc - tic:0.4f} seconds.")
    return peptides


def init_logger(log_level, file_handler=None):
    if not file_handler:
        file_handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s: %(message)s")
        file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(log_level)
