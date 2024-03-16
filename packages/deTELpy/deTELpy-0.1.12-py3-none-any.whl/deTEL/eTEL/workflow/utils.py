import collections as clt
from pathlib import Path

from Bio import SeqUtils

from deTEL.eTEL.workflow import INV_CODON_TABLE

AMINO_ACIDS_3_LETTER_CODE: list = [
    SeqUtils.seq3(aa) for aa in list("ACDEFGHIKLMNPQRSTVWY")
]


def get_codons() -> list:
    """Return a list of all possible codons."""
    bases = "TCAG"
    return [a + b + c for a in bases for b in bases for c in bases]


def get_amino_acids() -> str:
    """Returns amino acids corresponding to codons."""
    return "FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"


def invert_codon_table(codon_table: dict) -> dict:
    """Invert codon table.

    :param codon_table: Codon table as dictionary with codons as keys and amino acids as values.
    :returns: A dictionary with amino acids as keys and codons as values.
    """
    inv_codon_table = clt.defaultdict(list)
    for k, v in codon_table.items():
        inv_codon_table[v] = inv_codon_table.get(v, [])
        inv_codon_table[v].append(k)
    return inv_codon_table


def get_codons_by_aa() -> list:
    """Returns all possible codons."""
    codons_by_aa = []
    for aa in AMINO_ACIDS_3_LETTER_CODE:
        codons_by_aa = codons_by_aa + INV_CODON_TABLE[aa]

    return codons_by_aa


def codonify(seq):
    """Returns a list of codons for the given nucleotide sequence (not necessarily a string).

    @param seq: a nucleotide sequence (not necessarily a string).
    """
    seq = str(seq).upper()
    return [seq[i : i + 3] for i in range(0, len(seq), 3)]


def list_raw_files(raw_file_folder_path: Path, raw_file_ext=".raw") -> list[str]:
    return [
        item.name
        for item in raw_file_folder_path.iterdir()
        if item.is_file() and raw_file_ext in item.name
    ]


def list_tsv_files(
    open_search_output_path: Path, raw_files: list[str], raw_file_ext=".raw"
) -> list:
    return [
        f"{open_search_output_path / item.replace(raw_file_ext, '.tsv')}"
        for item in raw_files
    ]
