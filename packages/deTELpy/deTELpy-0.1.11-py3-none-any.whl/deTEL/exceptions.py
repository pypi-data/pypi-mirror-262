"""Custom exceptions for detelpy."""


class WrongSequenceTypeError(Exception):
    """Exception for cases when no GO annotation could be fetched from UniProt."""

    def __init__(self, fasta_file):
        self.fasta_file = fasta_file
        self.message = (
            f"It seems that you have provided the wrong FASTA sequence file: {fasta_file}\n"
            " The FASTA file appears to contain nucleotide sequences.\n"
            "Please provide a FASTA file containing protein sequences only."
        )
        super(Exception, self).__init__(self.message)
