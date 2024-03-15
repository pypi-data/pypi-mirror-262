import logging

from cloudfloordns.record import Record

DEFAULT_SPF = Record(name="", type="TXT", data="""v=spf1 -all""")
DEFAULT_DKIM = Record(name="*._domainkey", type="TXT", data="""v=DKIM1; p=""")
DEFAULT_DMARC = Record(
    name="_dmarc",
    type="TXT",
    data="""v=DMARC1; p=reject; sp=reject; adkim=s; aspf=s;""",
)
DEFAULT_MX = Record(name="", type="MX", data="")


def create_default_mail_records(client, domain, override=False, logger=None):
    if logger is None:
        logger = logging
    records = client.records.list(domain)
    spf_records = [r for r in records if r.is_spf]
    dkim_records = [r for r in records if r.is_dkim]
    dmarc_records = [r for r in records if r.is_dmarc]
    mx_records = [r for r in records if r.type == "MX"]

    if not spf_records or override:
        logger.info("Creating default SPF record for 'domain'")
        client.records.create(domain, DEFAULT_SPF)
    if not dkim_records or override:
        logger.info("Creating default DKIM record for 'domain'")
        client.records.create(domain, DEFAULT_DKIM)
    if not dmarc_records or override:
        logger.info("Creating default DMARC record for 'domain'")
        client.records.create(domain, DEFAULT_DMARC)
    if not mx_records or override:
        logger.info("Creating default MX record for 'domain'")
        client.records.create(domain, DEFAULT_MX)
