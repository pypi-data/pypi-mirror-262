import argparse
import re
import sys
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame

from deTEL.eTEL import CsvFileOutputColumnNames
from deTEL.eTEL.workflow import CODON_COUNTS_TABLE_COLUMN_NAMES_LIST
from deTEL.eTEL.workflow.utils import list_raw_files, list_tsv_files


matplotlib.use("Agg")


FDR = 0.01


def plot_codon_counts(codon_counts: DataFrame, output_file_path: Path):
    """Plots codon counts"""
    fig, ax1 = plt.subplots(1, 1, figsize=(10, 6))
    ax1.bar(codon_counts.index, codon_counts[CODON_COUNTS_TABLE_COLUMN_NAMES_LIST[1]])
    ax1.set_ylabel("Codon count", fontweight="bold")
    ax1.set_xlabel("Codons", fontweight="bold")
    ax1.set_xticks(codon_counts.index)
    ax1.set_xticklabels(codon_counts[CODON_COUNTS_TABLE_COLUMN_NAMES_LIST[0]], rotation=90)
    ax2 = ax1.twinx()
    ax2.plot(
        codon_counts.index,
        codon_counts[CODON_COUNTS_TABLE_COLUMN_NAMES_LIST[2]]
        / codon_counts[CODON_COUNTS_TABLE_COLUMN_NAMES_LIST[1]],
        color="k",
        linestyle="dashed",
    )
    ax2.plot(
        codon_counts.index,
        codon_counts[CODON_COUNTS_TABLE_COLUMN_NAMES_LIST[2]]
        / codon_counts[CODON_COUNTS_TABLE_COLUMN_NAMES_LIST[1]],
        color="k",
        marker="o",
    )
    ax2.set_ylabel("Error rate", fontweight="bold")
    plt.tight_layout()
    plt.savefig(f"{output_file_path}", format="png")


def plot_peptide_hist(peptide_counts: DataFrame, output_file_path: Path):
    fig, ax1 = plt.subplots(1, 1, figsize=(7, 5))
    ax1.hist(
        (peptide_counts[CsvFileOutputColumnNames.TOTAL] - peptide_counts[CsvFileOutputColumnNames.ERRONEOUS]),
        bins=100,
        histtype="stepfilled",
        alpha=0.8,
    )
    ax1.set_xlabel("Error free peptides per protein", fontweight="bold")
    ax1.set_ylabel("Frequency", fontweight="bold")
    plt.tight_layout()
    plt.savefig(f"{output_file_path}", format="png")


def plot_hyperscore_distribution(psm_data: DataFrame, output_file_path: Path):
    psm_data.sort_values("hyperscore", ascending=False, inplace=True)
    psm_data = psm_data.assign(
        is_decoy=psm_data["protein"].map(lambda x: re.search(r"rev_", x) is not None)
    )
    ratio = np.array(
        [
            i / float(j)
            for i, j in zip(
                psm_data["is_decoy"].cumsum(), range(1, len(psm_data.index) + 1)
            )
        ]
    )

    if np.min(ratio) < FDR:
        cut_off = np.max(np.where(ratio < FDR))
        hyperscore_th = np.array(psm_data["hyperscore"])[cut_off]

    psm_real = psm_data.query("is_decoy == False")
    psm_decoy = psm_data.query("is_decoy == True")

    fig, ax1 = plt.subplots(1, 1, figsize=(7, 5))
    x = ax1.hist(
        psm_real["hyperscore"],
        bins=100,
        histtype="stepfilled",
        alpha=0.8,
        density=False,
        label="Identified",
    )
    ax1.hist(
        psm_decoy["hyperscore"],
        bins=x[1],
        histtype="stepfilled",
        alpha=0.8,
        density=False,
        label="Decoys",
    )
    ax1.set_xlabel("Hyperscore", fontweight="bold")
    ax1.set_ylabel("Density", fontweight="bold")
    if np.min(ratio) < FDR:
        ax1.axvline(hyperscore_th, color="k", linestyle="dashed")
    ax1.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(f"{output_file_path}", format="png")


def parse_args(args):
    """Parse and retrieve input arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        dest="raw_file_folder_path",
        required=True,
        help="RAW file folder path",
        metavar="FILE",
    )
    parser.add_argument(
        "-b",
        dest="base_folder",
        required=True,
        help="Base folder name, which is used as file name prefix e.g. PXD018591",
    )
    parser.add_argument(
        "-e",
        dest="etel_output_path",
        required=True,
        help="eTEL output path",
        metavar="FILE",
    )
    parser.add_argument(
        "-s",
        dest="open_search_output_path",
        required=True,
        help="open search output path",
        metavar="FILE",
    )
    parser.add_argument(
        "-o", dest="output_folder", required=True, help="Output folder", metavar="FILE"
    )

    return parser.parse_args(args), parser


def main(args):
    args, parser = parse_args(args)
    raw_file_folder_path: Path = Path(args.raw_file_folder_path)
    open_search_output_path: Path = Path(args.open_search_output_path)
    etel_output_path: Path = Path(args.etel_output_path)
    base_folder: str = args.base_folder
    output_folder_p: Path = Path(args.output_folder)
    cf = etel_output_path / f"{base_folder}_codon_counts.csv"
    pf = etel_output_path / f"{base_folder}_peptide_counts.csv"
    print("Generating dataset report...")
    print(f"base_folder: {base_folder}")
    print(f"raw_file_folder_path: {raw_file_folder_path}")
    print(f"etel_output_path: {etel_output_path}")
    print(f"open_search_output_path: {open_search_output_path}")
    print(f"output_folder_p: {output_folder_p}")

    # after detection of substitution
    codon_counts = pd.read_csv(cf, sep=",", header=0, index_col=0)
    plot_codon_counts(
        codon_counts=codon_counts,
        output_file_path=output_folder_p / f"{base_folder}_codon_counts.png",
    )

    peptide_counts = pd.read_csv(pf, sep=",", header=0, index_col=0)
    plot_peptide_hist(
        peptide_counts=peptide_counts,
        output_file_path=output_folder_p / f"{base_folder}_peptide_counts.png",
    )

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
    plot_hyperscore_distribution(
        psm_data=psm_data,
        output_file_path=output_folder_p / f"{base_folder}_hyperscore_distribution.png",
    )
    print("Finished dataset report generation successfully.")


if __name__ == "__main__":
    main(sys.argv[1:])
