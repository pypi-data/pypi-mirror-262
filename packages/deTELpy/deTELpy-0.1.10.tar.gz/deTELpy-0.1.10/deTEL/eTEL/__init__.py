from enum import Enum


class CsvFileOutputColumnNames(str, Enum):
    TOTAL_COUNT = "total_count"
    ERROR_COUNT = "error_count"
    DETECTION_RATE = "detection_rate"
    BASE_COUNT = "base_count"
    LOCALIZATION_IN_PROTEIN = "localization_in_protein"
    PROTEIN = "protein"
    CODON = "codon"
    AA = "aa"
    RAW_FILE = "raw_file"
    TOTAL = "total"
    ERRONEOUS = "erroneous"
    TOTAL_ERROR_RATE = "total_error_rate"
    INTENSITY = "intensity"
