# from dataclasses import dataclass, field
from typing import Literal

from pydantic import BaseModel, Extra

TYPES_VALUES = Literal[
    "A",
    "AAAA",
    "ALIAS" "CNAME",
    "HINFO" "MX",
    "NS",
    "PTR",
    "RP" "SRV",
    "CAA",
    "TXT",
    "REDIRECT://",
    # For comparison, the following are valid on Cloudflare
    # "SOA",
    # "DS",
    # "DNSKEY",
    # "LOC",
    # "NAPTR",
    # "SSHFP",
    # "SVCB",
    # "TSLA",
    # "URI",
    # "SPF",
]

FULL_COMPARISON = {
    "A",
    "AAAA",
    "ALIAS" "CNAME",
}

UNIQUE_BY_NAME = {"HINFO" "MX", "NS", "PTR", "RP" "SRV", "CAA", "TXT", "REDIRECT://"}


class Record(BaseModel):
    name: str
    type: str
    data: str
    id: str = None
    zone: str = None
    aux: str = "0"
    ttl: int = 3600
    active: Literal["Y", "N"] = "Y"
    # isfwd: str = "0"
    # cc: str = None
    # lbType: str = "0"

    class Config:
        populate_by_name = True
        extra = Extra.allow

    # def __eq__(self, __value: Record) -> bool:
    #     if not isinstance(__value, Record):
    #         return NotImplemented
    #     fields1 = self.model_dump(exclude_unset=True)
    #     fields2 = __value.model_dump(exclude_unset=True)
    #     try:
    #         return all(fields2[k] == v for k, v in fields1.items())
    #     except Exception:
    #         return False

    def is_same(self, right: "Record") -> bool:
        """
        This method check the identity (e.g. same id if defined, or same name/name+value)
        """
        if not isinstance(right, Record):
            return NotImplemented
        if self.id and right.id:
            return self.id == right.id
        if (self.name, self.type) != (right.name, right.type):
            return False
        if self.type in FULL_COMPARISON:
            return self.data == right.data
        return True

    @property
    def is_spf(self) -> bool:
        return all((not self.name, self.type == "TXT", "v=spf" in self.data.lower()))

    @property
    def is_dkim(self) -> bool:
        return all(
            (
                "._domainkey" in self.name,
                self.type == "TXT",
                "v=dkim" in self.data.lower(),
            )
        )

    @property
    def is_dmarc(self) -> bool:
        return all(
            ("_dmarc" in self.name, self.type == "TXT", "v=dmarc" in self.data.lower())
        )


class Records:
    def __init__(self, client) -> None:
        self.client = client

    def create(self, domain: str, record: Record, timeout=None):
        url = f"/dns/zone/{domain}/record"
        return self.client.post(
            url,
            data=record.model_dump(),
            timeout=timeout,
        )

    def update(self, domain: str, record_id: str, record: Record, timeout=None):
        url = f"/dns/zone/{domain}/record/{record_id}"
        return self.client.patch(
            url,
            data=record.model_dump(exclude_unset=True),
            timeout=timeout,
        )

    def delete(self, domain: str, record_id: str, timeout=None):
        url = f"/dns/zone/{domain}/record/{record_id}"
        return self.client.delete(
            url,
            timeout=timeout,
        )

    def list(self, domain: str, timeout=None):
        url = f"/dns/zone/{domain}/record"
        res = self.client.get(
            url,
            timeout=timeout,
        )
        return [Record(**d) for d in res]

    def get(self, domain: str, record_id, timeout=None):
        res = self.client.list(
            domain,
            timeout=timeout,
        )
        return next((r for r in res if r.id == record_id), None)
