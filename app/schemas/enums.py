from enum import Enum


class TriggerEnum(Enum):
    """
    Enum for Trigger
    """

    GOOGLE_SHEETS = "google_sheets"
    RECEIPT_SMS = "receipt_sms"
