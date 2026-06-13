import re
from decimal import Decimal
from datetime import datetime


class MpesaSMSParserError(Exception):
    pass


class MpesaSMSParser:

    NAME_PATTERN = r"Dear\s+(.*?),"
    AMOUNT_PATTERN = r"sent\s+Ksh\.\s*([\d,]+(?:\.\d+)?)"
    RECIPIENT_PATTERN = r"to\s+(.*?)\s+for"
    ACCOUNT_PATTERN = r"for\s+(.*?)\s+on"
    DATETIME_PATTERN = r"on\s+(\d{2}/\d{2}/\d{4})\s+at\s+(\d{2}:\d{2}:\d{2})"
    REFERENCE_PATTERN = r"MPESA\s+Ref\.\s*([A-Z0-9]+)"

    @classmethod
    def parse(cls, sms):

        try:

            name = re.search(
                cls.NAME_PATTERN,
                sms
            ).group(1)

            amount = Decimal(
                re.search(
                    cls.AMOUNT_PATTERN,
                    sms
                ).group(1)
            )

            recipient = re.search(
                cls.RECIPIENT_PATTERN,
                sms
            ).group(1)

            account_reference = re.search(
                cls.ACCOUNT_PATTERN,
                sms
            ).group(1)

            date_str, time_str = re.search(
                cls.DATETIME_PATTERN,
                sms
            ).groups()

            mpesa_reference = re.search(
                cls.REFERENCE_PATTERN,
                sms
            ).group(1)

            transaction_datetime = datetime.strptime(
                f"{date_str} {time_str}",
                "%m/%d/%Y %H:%M:%S"
            )

            return {
                "name": name.strip(),
                "amount": amount,
                "recipient": recipient.strip(),
                "account_reference": account_reference.strip(),
                "transaction_datetime": transaction_datetime,
                "mpesa_reference": mpesa_reference.strip(),
            }

        except Exception as e:
            raise MpesaSMSParserError(
                str(e)
            )