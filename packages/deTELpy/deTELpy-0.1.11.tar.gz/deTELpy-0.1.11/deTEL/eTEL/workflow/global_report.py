import argparse
import collections as clt
import logging
import os
import re
import sys
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from Bio import SeqIO, SeqUtils
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from scipy import stats

from deTEL.eTEL import CsvFileOutputColumnNames
from deTEL.eTEL.workflow import (
    AMINO_ACIDS_ONE_TO_THREE,
    CODON_TABLE,
    SUBSTITUTION_ERROR_FILE_NAME_SUFFIX,
)
from deTEL.eTEL.workflow.utils import (
    AMINO_ACIDS_3_LETTER_CODE,
    INV_CODON_TABLE,
    get_codons_by_aa,
)

matplotlib.use("Agg")

logger = logging.getLogger(__name__)


def unique(sequence):
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]


def aa_limits(codon_list, ct):
    aas = []
    for c in codon_list:
        aas.append(ct[c])
    cc = dict(clt.Counter(aas))
    cc["Ala"] = 3.5
    cumsum = [0]
    for key, value in cc.items():
        cumsum.append(cumsum[-1] + value)
    cumsum.pop(0)
    del cumsum[-1]
    return cumsum


def read_codon_proteome(filename: str) -> dict:
    logger.info("Reading codon proteome...")
    proteome = list(SeqIO.parse(filename, "fasta"))
    codonified_proteome: dict = clt.defaultdict(list)

    for protein in proteome:
        sequence = str(protein.seq).upper()
        codon_seq = [sequence[i : i + 3] for i in range(0, len(sequence), 3)]
        codonified_proteome[protein.id] = codon_seq

    logger.info("Finished reading codon proteome")
    return codonified_proteome


def read_all_substitutions(folder: Path, codon_proteome) -> pd.DataFrame:
    logger.info("Reading substitutions...")
    sub_error_files: list[str] = [
        f"{error_file}"
        for error_file in folder.iterdir()
        if error_file.is_file()
        and SUBSTITUTION_ERROR_FILE_NAME_SUFFIX in error_file.name
    ]
    substitution = pd.DataFrame(
        None,
        columns=[
            CsvFileOutputColumnNames.PROTEIN,
            "destination",
            "origin",
            "codon",
            CsvFileOutputColumnNames.LOCALIZATION_IN_PROTEIN,
            "intensity_based_error_rate",
            "dataset",
        ],
    )
    for sf in sub_error_files:
        tmp = pd.read_csv(
            sf,
            sep=",",
            header=0,
            usecols=[
                CsvFileOutputColumnNames.PROTEIN,
                "destination",
                "origin",
                "codon",
                CsvFileOutputColumnNames.LOCALIZATION_IN_PROTEIN,
                "intensity_based_error_rate",
            ],
        )
        tmp["dataset"] = os.path.basename(sf).split("_")[0]
        substitution = pd.concat([substitution, tmp])

    substitution.dropna(axis=0, inplace=True)
    substitution["length"] = substitution[CsvFileOutputColumnNames.PROTEIN].map(
        lambda x: len(codon_proteome[x])
    )
    substitution.query("length > 0", inplace=True)
    substitution["fractional_pos_in_prot"] = (
        substitution[CsvFileOutputColumnNames.LOCALIZATION_IN_PROTEIN] / substitution["length"]
    ) * 100
    substitution["log_intensity_based_error_rate"] = substitution[
        "intensity_based_error_rate"
    ].map(np.log10)
    substitution.replace([np.inf, -np.inf], np.nan, inplace=True)

    logger.info("Finished reading substitutions.")
    return substitution


def get_substitution_counts(subs_df):
    aa_substitution_count = pd.DataFrame(
        0, index=AMINO_ACIDS_3_LETTER_CODE, columns=AMINO_ACIDS_3_LETTER_CODE, dtype=int
    )

    codons = []
    for aa in AMINO_ACIDS_3_LETTER_CODE:
        codons = codons + INV_CODON_TABLE[aa]

    codon_substitution_count = pd.DataFrame(
        0, index=codons, columns=AMINO_ACIDS_3_LETTER_CODE, dtype=int
    )

    for row in subs_df.iterrows():
        r = row[1]
        o = SeqUtils.seq3(r["origin"])
        d_one = r["destination"]
        if d_one == "I/L":
            d_one = "L"
        d = SeqUtils.seq3(d_one)
        aa_substitution_count.at[o, d] += 1
        codon_substitution_count.at[r["codon"], d] += 1

    return aa_substitution_count, codon_substitution_count


def read_substitutions_as_dict(folder: Path, codon_proteome) -> dict:
    logger.info("Converting substitutions to dictionary...")
    sub_error_files: list[str] = sorted(
        [
            f"{error_file}"
            for error_file in folder.iterdir()
            if error_file.is_file()
            and SUBSTITUTION_ERROR_FILE_NAME_SUFFIX in error_file.name
        ]
    )
    substitution = {}

    for sf in sub_error_files:
        pxd_id = list(filter(lambda x: re.search(r"PXD", x), re.split("_|/", sf)))[0]
        tmp = pd.read_csv(
            sf,
            sep=",",
            header=0,
            usecols=[
                CsvFileOutputColumnNames.PROTEIN,
                "destination",
                "origin",
                "codon",
                CsvFileOutputColumnNames.LOCALIZATION_IN_PROTEIN,
            ],
        )
        tmp.dropna(axis=0, inplace=True)
        tmp["length"] = tmp[CsvFileOutputColumnNames.PROTEIN].map(lambda x: len(codon_proteome[x]))
        tmp.query("length > 0", inplace=True)
        tmp["fractional_pos_in_prot"] = (
            tmp[CsvFileOutputColumnNames.LOCALIZATION_IN_PROTEIN] / tmp["length"]
        ) * 100
        substitution[pxd_id] = tmp

    logger.info("Dictionary conversation completed.")
    return substitution


def read_codon_counts_as_dict(folder: Path) -> dict:
    logger.info("Converting codon counts to dictionary...")
    count_files: list[str] = [
        f"{count_file}"
        for count_file in folder.iterdir()
        if count_file.is_file() and "codon_counts.csv" in count_file.name
    ]
    codon_counts = {}
    for cf in count_files:
        pxd_id = list(filter(lambda x: re.search(r"PXD", x), re.split("_|/", cf)))[0]
        tmp = pd.read_csv(
            cf,
            sep=",",
            header=0,
            index_col=0,
            usecols=[
                CsvFileOutputColumnNames.CODON,
                CsvFileOutputColumnNames.BASE_COUNT,
                CsvFileOutputColumnNames.ERROR_COUNT,
                CsvFileOutputColumnNames.DETECTION_RATE
            ],
        )
        codon_counts[pxd_id] = tmp

    logger.info("Finished dictionary conversation.")
    return codon_counts


def get_all_codon_count(cc_dict: dict, subs_dict: dict) -> pd.DataFrame:
    all_codon_counts = pd.DataFrame(
        None, columns=["total_count", "error_count", "detection_rate"]
    )
    for key in cc_dict.keys():
        cc = cc_dict[key]
        sub = subs_dict[key].groupby("codon").count()
        cc["subs"] = sub[CsvFileOutputColumnNames.PROTEIN]
        all_codon_counts = pd.concat([all_codon_counts, cc], axis=0)

    all_codon_counts[CsvFileOutputColumnNames.CODON] = all_codon_counts.index
    all_codon_counts[CsvFileOutputColumnNames.AA] = all_codon_counts[CsvFileOutputColumnNames.CODON].map(lambda x: CODON_TABLE[x])
    all_codon_counts["log_detection_rate"] = all_codon_counts[CsvFileOutputColumnNames.DETECTION_RATE].map(
        np.log10
    )
    all_codon_counts.replace([np.inf, -np.inf], np.nan, inplace=True)
    all_codon_counts.dropna(subset=["log_detection_rate"], inplace=True)

    return all_codon_counts


def plot_substitution_identified(
    all_substitutions,
    peptide_count,
    cutoff=0.5,
    substitution_folder=None,
    filtered_folder=None,
    out_folder=None,
):

    n_subs = all_substitutions.groupby("dataset").count().loc[:, "protein"]
    n_peptides = peptide_count.groupby("dataset").sum().loc[:, "total_peptide"]

    x = np.array(np.log10(n_peptides))
    y = np.array(np.log10(n_subs))
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    keep = np.where(
        ((slope * x + intercept + cutoff) > y)
        & ((slope * x + intercept - cutoff) < y)
        & (y > 1)
    )
    fig, axs = plt.subplots(1, 1, figsize=(6, 5))
    axs.scatter(x, y, color="0.25", alpha=0.3)
    axs.scatter(x[keep], y[keep], color="b", alpha=0.3)
    axs.set_xlabel(r"log$_{10}$[Identified peptides]", fontweight="bold")
    axs.set_ylabel(r"log$_{10}$[Identified substitutions]", fontweight="bold")
    axs.annotate(text=r"R$^2$ = {0:0.2f}".format(r_value), xy=(2, 3.2))
    axs.annotate(text=r"y = {0:.1f}x + {1:.1f}".format(slope, intercept), xy=(2, 3))
    axs.annotate(text=r"$\rho$ = {0:.4f}".format(p_value), xy=(2, 2.8))
    axs.axline(
        xy1=(min(x), slope * min(x) + intercept),
        slope=slope,
        color="0.25",
        linestyle="--",
    )
    axs.axline(
        xy1=(min(x), slope * min(x) + intercept + cutoff),
        slope=slope,
        color="b",
        linestyle="--",
        alpha=0.3,
    )
    axs.axline(
        xy1=(min(x), slope * min(x) + intercept - cutoff),
        slope=slope,
        color="b",
        linestyle="--",
        alpha=0.3,
    )
    axs.axline(xy1=(min(x), 1), slope=0, color="b", linestyle="--", alpha=0.3)
    fig.tight_layout()
    plt.savefig(out_folder + "/global-1.png", format="png")

    # For HongKee: This part is tricky, of course the function should only plot. I took this whole routine from my
    # filtering function which I use to filter my datasets, only keeping what I deem useful.
    # Maybe it should be done separately which requires that we can ensure that the cutoff parameter is not changed
    # between the plot and the copying of files.
    if substitution_folder is not None and filtered_folder is not None:
        # keep only these datasets for fitting
        datasets = np.array(n_subs.index)[keep]
        for d in datasets:
            os.system(f"cp {substitution_folder}/{d}* filtered_folder")


def plot_substitution_pos_hist(all_substitutions: pd.DataFrame, output_file_p: Path):
    logger.info("Generating position histogram...")
    fig, axs = plt.subplots(1, 1, figsize=(6, 5))
    # Ref: https://github.com/mwaskom/seaborn/issues/2652#issuecomment-916114304
    all_substitutions = all_substitutions.reset_index(drop=True)
    g = sns.histplot(
        data=all_substitutions,
        x="fractional_pos_in_prot",
        ax=axs,
        bins=100,
        color="0.25",
    )
    g.set_xlim(0, 100)
    g.set_xlabel("Percent Protein Length", fontweight="bold")
    g.set_ylabel("Detected Substitutions", fontweight="bold")
    fig.tight_layout()
    plt.savefig(f"{output_file_p}", format="png")
    logger.info("Finished position histogram generation.")


def plot_heatmap(
    count_array,
    output_file_p,
    aabounds=None,
    colmap: str = "bwr",
    log: bool = False,
    include_total=False,
):
    logger.info("Generating heat map...")
    if include_total:
        columns = list(count_array.columns) + ["Total"]
    else:
        columns = list(count_array.columns)

    max_val = count_array.max().max()

    total = count_array.sum(axis=1)
    if log:
        total = np.log(total)
        count_array = np.log10(count_array)
        max_val = np.log10(max_val)
        count_array[np.isinf(count_array)] = float("NaN")

    img_data = pd.DataFrame(float("NaN"), index=count_array.index, columns=columns)
    img_data.loc[count_array.index, count_array.columns] = count_array

    fig, ax = plt.subplots(figsize=(6.5, 10))
    plt.subplots_adjust(left=0.11, right=0.74, top=0.99, bottom=0.1)
    ima = ax.imshow(img_data, cmap=colmap, aspect="auto", vmax=max_val)  #

    if include_total:
        img_data = pd.DataFrame(float("NaN"), index=count_array.index, columns=columns)
        img_data["Total"] = total
        imb = ax.imshow(
            img_data, cmap="Blues", aspect="auto", vmax=img_data.max().max()
        )

    # Create color bar
    if include_total:
        axins = inset_axes(
            ax,
            width="5%",
            height="45%",
            loc="lower left",
            bbox_to_anchor=(1.13, 0.0, 1, 1),
            bbox_transform=ax.transAxes,
            borderpad=0,
        )
        axins1 = inset_axes(
            ax,
            width="5%",
            height="45%",
            loc="upper left",
            bbox_to_anchor=(1.13, 0.0, 1, 1),
            bbox_transform=ax.transAxes,
            borderpad=0,
        )
    else:
        axins1 = inset_axes(
            ax,
            width="5%",
            height="45%",
            loc="center left",
            bbox_to_anchor=(1.13, 0.0, 1, 1),
            bbox_transform=ax.transAxes,
            borderpad=0,
        )

    if include_total:
        cbar = ax.figure.colorbar(imb, cax=axins, extend="both")
        plt.setp(cbar.ax.yaxis.get_ticklabels(), weight="bold")

    # ticks = np.linspace(0, np.ceil((10**max_val)/100), 5, endpoint=True)*100
    cbar2 = ax.figure.colorbar(ima, cax=axins1, extend="both")
    plt.setp(cbar2.ax.yaxis.get_ticklabels(), weight="bold")

    xlab = columns
    codons = count_array.index
    ylab = [c.replace("T", "U") for c in count_array.index]

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(xlab)))
    ax.set_yticks(np.arange(len(ylab)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(xlab, weight="bold")
    ax.set_yticklabels(ylab, weight="bold")

    # put x label on top
    ax.tick_params(top=False, bottom=True, labeltop=False, labelbottom=True)

    ax.set_xlabel("Destination Amino Acid", weight="bold")
    ax.set_ylabel("Original Codon", weight="bold")

    if aabounds is not None:
        ax.hlines(aabounds, *ax.get_xlim(), color="k")
        # second y-axis with AA labels
        ax1 = ax.twinx()
        ax1.set_ylim(ax.get_ylim())

        y2_tick_pos = [ax.get_ylim()[1]] + aabounds + [ax.get_ylim()[0]]
        y2_tick_pos = [
            sum(y2_tick_pos[i : i + 2]) / 2 for i in range(len(y2_tick_pos) - 2 + 1)
        ]

        y2lab = unique([CODON_TABLE[c] for c in codons])
        ax1.set_yticks(y2_tick_pos)
        ax1.set_yticklabels(y2lab, weight="bold", rotation=0)
        ax1.tick_params(top=False, bottom=True, labeltop=False, labelbottom=True)
        ax1.autoscale(False)

    ax.autoscale(False)

    # Rotate the tick labels and set their alignment.
    plt.setp(
        ax.get_xticklabels(),
        rotation=90,
        ha="center",
        va="top",
        rotation_mode="default",
    )
    plt.savefig(f"{output_file_p}", format="png")
    logger.info("Finished heat map generation.")


def plot_detection_rate(
    output_file_p: Path,
    all_codon_counts: pd.DataFrame,
    all_substitutions: pd.DataFrame,
    aabounds,
):
    """This is the boxplot"""
    logger.info("Plotting detection rate...")
    codons_by_aa = get_codons_by_aa()
    fig, ax = plt.subplots(1, 1, figsize=(6.5, 12))

    col1 = "#a6cee3"
    col2 = "#b2df8a"
    palette = {
        "Ala": col1,
        "Cys": col2,
        "Asp": col1,
        "Glu": col2,
        "Phe": col1,
        "Gly": col2,
        "His": col1,
        "Ile": col2,
        "Lys": col1,
        "Leu": col2,
        "Met": col1,
        "Asn": col2,
        "Pro": col1,
        "Gln": col2,
        "Arg": col1,
        "Ser": col2,
        "Thr": col1,
        "Val": col2,
        "Trp": col1,
        "Tyr": col2,
    }
    all_substitutions[CsvFileOutputColumnNames.AA] = all_substitutions.origin.map(
        lambda x: AMINO_ACIDS_ONE_TO_THREE[x]
    )
    slim_substitutions = all_substitutions.dropna(
        subset=["log_intensity_based_error_rate"], how="all"
    )
    slim_substitutions.codon = slim_substitutions.codon.map(
        lambda x: x.replace("T", "U")
    )
    all_codon_counts.codon = all_codon_counts.codon.map(lambda x: x.replace("T", "U"))
    codons = codons_by_aa
    codons_by_aa = [c.replace("T", "U") for c in codons_by_aa]
    g = sns.boxplot(
        ax=ax,
        y="codon",
        x="log_intensity_based_error_rate",
        data=slim_substitutions,
        saturation=1,
        order=codons_by_aa,
        hue=CsvFileOutputColumnNames.AA,
        dodge=False,
        fliersize=0,
        palette=palette,
    )
    g = sns.stripplot(
        ax=ax,
        y="codon",
        x="log_intensity_based_error_rate",
        data=slim_substitutions,
        color="0.25",
        order=codons_by_aa,
        alpha=0.7,
    )
    g = sns.stripplot(
        ax=ax,
        y=CsvFileOutputColumnNames.CODON,
        x="log_detection_rate",
        data=all_codon_counts,
        color="r",
        order=codons_by_aa,
        alpha=0.5,
    )
    g.set_xlabel("log$_{10}$[Error Detection Rate]", fontweight="bold")
    g.set_ylabel("Codon", fontweight="bold")
    plt.legend([], [], frameon=False)

    if aabounds is not None:
        ax.hlines(aabounds, *ax.get_xlim(), color="k")
        # second y-axis with AA labels
        ax1 = ax.twinx()
        ax1.set_ylim(ax.get_ylim())

        y2_tick_pos = [ax.get_ylim()[1]] + aabounds + [ax.get_ylim()[0]]
        y2_tick_pos = [
            sum(y2_tick_pos[i : i + 2]) / 2 for i in range(len(y2_tick_pos) - 2 + 1)
        ]

        y2lab = unique([CODON_TABLE[c] for c in codons])
        ax1.set_yticks(y2_tick_pos)
        ax1.set_yticklabels(y2lab, weight="bold", rotation=0)

        ax1.tick_params(top=False, bottom=True, labeltop=False, labelbottom=True)
        ax1.autoscale(False)
    ax.autoscale(False)

    fig.tight_layout()
    plt.savefig(f"{output_file_p}", format="png")
    logger.info("Finished plotting detection rate.")


def plot_substitutions_detected(subs_dict, out_folder=None):
    fig, ax = plt.subplots(1, 1, figsize=(6.5, 5))
    n_subs_detected = [len(df.index) for df in subs_dict.values()]
    g = sns.histplot(n_subs_detected, log_scale=True, color="0.25")
    g.set_ylabel("Datasets", fontweight="bold")
    g.set_xlabel("Detected Substitutions", fontweight="bold")
    fig.tight_layout()
    plt.savefig(out_folder + "/global-5.png", format="png")


def parse_args(args):
    """Parse and retrieve input arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        dest="fasta",
        required=True,
        help="Search database as codon fasta file (CDS FASTA formatted file)",
        metavar="FILE",
    )
    parser.add_argument(
        "-s",
        dest="substitution_folder",
        required=True,
        help="substitution folder",
        metavar="FILE",
    )
    parser.add_argument(
        "-b",
        dest="base_folder",
        required=True,
        help="Base folder name, which is used as file name prefix e.g. PXD018591",
    )
    parser.add_argument(
        "-o",
        dest="output_folder",
        required=True,
        help="Output folder",
        metavar="FILE",
    )
    return parser.parse_args(args), parser


def init_logger(log_level, file_handler=None):
    if not file_handler:
        file_handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s: %(message)s")
        file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(log_level)


def generate_global_report(
    substitution_input_folder_p: Path,
    report_output_folder_p: Path,
    cds_file_path: str,
    dataset_id: str,
    parent_logger=None,
):
    if parent_logger:
        init_logger(
            log_level=parent_logger.level, file_handler=parent_logger.handlers[0]
        )
    logger.info("Generating global report...")
    logger.info(f"cds_file: {cds_file_path}")
    logger.info(f"substitution_folder: {substitution_input_folder_p}")
    report_output_folder_p.mkdir(exist_ok=True)

    codon_prot: dict = read_codon_proteome(cds_file_path)
    all_substitutions: pd.DataFrame = read_all_substitutions(
        substitution_input_folder_p, codon_prot
    )
    codon_count_dict: dict = read_codon_counts_as_dict(substitution_input_folder_p)
    substitution_dict: dict = read_substitutions_as_dict(
        substitution_input_folder_p, codon_prot
    )

    substitution_pos_hist_output_file_p: Path = (
        report_output_folder_p / f"{dataset_id}_position_hist.png"
    )
    plot_substitution_pos_hist(all_substitutions, substitution_pos_hist_output_file_p)

    aa_sub_matrix, codon_sub_matrix = get_substitution_counts(all_substitutions)
    aabounds = aa_limits(list(codon_sub_matrix.index), CODON_TABLE)

    heatmap_plot_output_file_p: Path = (
        report_output_folder_p / f"{dataset_id}_heatmap.png"
    )
    plot_heatmap(
        codon_sub_matrix,
        heatmap_plot_output_file_p,
        aabounds=aabounds,
        colmap="Reds",
        log=True,
    )

    all_cc: pd.DataFrame = get_all_codon_count(codon_count_dict, substitution_dict)
    output_file_p: Path = (
        report_output_folder_p / f"{dataset_id}_detection_rate_plot.png"
    )
    plot_detection_rate(output_file_p, all_cc, all_substitutions, aabounds)
    logger.info("Finished global report generation successfully.")


def main(args):
    init_logger(logging.INFO)
    args, parser = parse_args(args)
    cds_filename = args.fasta
    base_folder: str = args.base_folder
    substitution_folder_p: Path = Path(args.substitution_folder)
    report_output_folder_p: Path = Path(args.output_folder)
    generate_global_report(
        substitution_folder_p,
        report_output_folder_p,
        cds_filename,
        dataset_id=f"{base_folder}",
    )


if __name__ == "__main__":
    main(sys.argv[1:])
