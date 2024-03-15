# from dataclasses import dataclass, field
from typing import List

from pydantic import BaseModel, Extra, Field


class Domain(BaseModel):
    domainname: str

    id: str = None
    registered: int = None
    secondary: int = None
    primary: int = None
    group_ids: List[str] = Field(default_factory=list)

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

    def is_same(self, right: "Domain") -> bool:
        """
        This method check the identity (e.g. same id if defined, or same name/name+value)
        """
        if not isinstance(right, Domain):
            return NotImplemented
        return self.domainname == self.right


class Domains:
    def __init__(self, client) -> None:
        self.client = client

    # def create(self, domain: str, record: Record, timeout=None):
    #     url = f"/dns/zone/{domain}/record"
    #     return self.client.post(
    #         url,
    #         data=record.model_dump(),
    #         timeout=timeout,
    #     )

    # def update(self, domain: str, record_id: str, record: Record, timeout=None):
    #     url = f"/dns/zone/{domain}/record/{record_id}"
    #     return self.client.patch(
    #         url,
    #         data=record.model_dump(exclude_unset=True),
    #         timeout=timeout,
    #     )

    # def delete(self, domain: str, record_id: str, timeout=None):
    #     url = f"/dns/zone/{domain}/record/{record_id}"
    #     return self.client.delete(
    #         url,
    #         timeout=timeout,
    #     )

    def list(self, timeout=None):
        url = "/dns/zone"
        res = self.client.get(
            url,
            timeout=timeout,
        )
        return [Domain(**d) for d in res]

    def get(self, domain: str, domain_id, timeout=None):
        res = self.client.list(
            domain,
            timeout=timeout,
        )
        return next((r for r in res if r.id == domain_id), None)

    def get_by_name(self, domain: str, domainname, timeout=None):
        res = self.client.list(
            domain,
            timeout=timeout,
        )
        return next((r for r in res if r.domainname == domainname), None)
