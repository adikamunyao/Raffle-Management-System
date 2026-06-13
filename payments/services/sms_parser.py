import re
from decimal import Decimal
from datetime import datetime


class SMSParserError(Exception):
    pass


class CoopBankSMSParser:
    """
    Parses the CoopBank/M-Pesa confirmation SMS used by KAG Clay Works.

    Sample:
      Dear EMMANUEL ADIKA, you have sent Ksh. 10.0 to K.A.G CLAYWORKS CHURCH
      for raffleDraw on 06/13/2026 at 13:15:14. MPESA Ref. UFDN77PY5D.
    """

    NAME_PATTERN     = r"Dear\s+([A-Z][A-Z\s]+?),"
    AMOUNT_PATTERN   = r"sent\s+Ksh\.\s*([\d,]+(?:\.\d+)?)"
    DATETIME_PATTERN = r"on\s+(\d{2}/\d{2}/\d{4})\s+at\s+(\d{2}:\d{2}:\d{2})"
    REF_PATTERN      = r"MPESA\s+Ref\.\s*([A-Z0-9]+)"

    @classmethod
    def parse(cls, sms: str) -> dict:
        sms = sms.strip()

        name_m   = re.search(cls.NAME_PATTERN,     sms, re.IGNORECASE)
        amount_m = re.search(cls.AMOUNT_PATTERN,   sms, re.IGNORECASE)
        dt_m     = re.search(cls.DATETIME_PATTERN, sms, re.IGNORECASE)
        ref_m    = re.search(cls.REF_PATTERN,      sms, re.IGNORECASE)

        missing = []
        if not name_m:   missing.append("sender name (Dear ...)")
        if not amount_m: missing.append("amount (sent Ksh. ...)")
        if not ref_m:    missing.append("MPESA Ref.")

        if missing:
            raise SMSParserError(
                f"Could not read {', '.join(missing)} from the SMS. "
                "Please paste the full unedited CoopBank confirmation message."
            )

        amount = Decimal(amount_m.group(1).replace(",", ""))

        transaction_datetime = None
        if dt_m:
            try:
                transaction_datetime = datetime.strptime(
                    f"{dt_m.group(1)} {dt_m.group(2)}", "%m/%d/%Y %H:%M:%S"
                )
            except ValueError:
                pass

        return {
            "name":                 name_m.group(1).strip().title(),
            "amount":               amount,
            "bank_reference":       ref_m.group(1).strip(),
            "transaction_datetime": transaction_datetime,
        }
