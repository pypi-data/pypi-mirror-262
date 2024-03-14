"""rTEL module"""

from enum import Enum


class SequenceType(str, Enum):
    PEPTIDE = "peptide"
    NUCLEOTIDE = "nucleotide"
