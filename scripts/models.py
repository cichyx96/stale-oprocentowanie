from enum import Enum


class FixedRateDataEntry:
    def __init__(self, bank, offer_name, fixed_interest_rate, apr, offer_collection_date):
        self.bank = bank
        self.offer_name = offer_name
        self.fixed_interest_rate = fixed_interest_rate
        self.apr = apr
        self.offer_collection_date = offer_collection_date

    @classmethod
    def from_dict(cls, data):
        """
        Create a FixedRateDataEntry object from a dictionary.
        """
        return cls(
            bank=data.get("bank"),
            offer_name=data.get("offer_name"),
            fixed_interest_rate=data.get("fixed_interest_rate"),
            apr=data.get("apr"),
            offer_collection_date=data.get("offer_collection_date"),
        )
    def __repr__(self):
        return (
            f"FixedRateDataEntry(bank={self.bank}, "
            f"offer_name={self.offer_name}, "
            f"fixed_interest_rate={self.fixed_interest_rate}, "
            f"apr={self.apr}, "
            f"offer_collection_date={self.offer_collection_date})"
        )
    
    def to_dict(self):
        """
        Convert the FixedRateDataEntry object to a dictionary.
        """
        return {
            "bank": self.bank,
            "offer_name": self.offer_name,
            "fixed_interest_rate": self.fixed_interest_rate,
            "apr": self.apr,
            "offer_collection_date": self.offer_collection_date,
        }