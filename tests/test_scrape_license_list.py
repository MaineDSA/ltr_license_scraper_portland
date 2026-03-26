from pathlib import Path

import pytest
from requests import Session

from src.license_downloader import Config, LicenseScraper


@pytest.fixture
def session() -> Session:
    return Session()


@pytest.fixture
def scraper(session: Session) -> LicenseScraper:
    config = Config(
        test_mode=True,
        output_file=Path("output.csv"),
        issue_date_from="2025-01-01",
        rate_limit_delay=0.1,
    )
    return LicenseScraper(session, config)


@pytest.fixture
def licenses(scraper: LicenseScraper) -> list[dict]:
    return scraper.fetch_all_licenses()


@pytest.mark.vcr
@pytest.mark.default_cassette("license_list.yaml")
def test_list_length(licenses: list[dict]) -> None:
    assert len(licenses) == 60


@pytest.mark.vcr
@pytest.mark.default_cassette("license_list.yaml")
def test_list_first_item_keys(licenses: list[dict]) -> None:
    assert set(licenses[0].keys()) == {
        "CaseId",
        "CaseNumber",
        "CaseTypeId",
        "CaseType",
        "CaseWorkclassId",
        "CaseWorkclass",
        "CaseStatusId",
        "CaseStatus",
        "ProjectName",
        "IssueDate",
        "ApplyDate",
        "ExpireDate",
        "CompleteDate",
        "FinalDate",
        "RequestDate",
        "ScheduleDate",
        "StartDate",
        "ExpectedEndDate",
        "Address",
        "ModuleName",
        "AddressDisplay",
        "MainParcel",
        "Description",
        "DBA",
        "LicenseYear",
        "CompanyName",
        "CompanyTypeName",
        "BusinessTypeName",
        "TaxID",
        "OpenedDate",
        "ClosedDate",
        "LastAuditDate",
        "HolderCompanyName",
        "HolderFirstName",
        "HolderLastName",
        "HolderMiddleName",
        "BusinessId",
        "BusinessStatus",
        "Highlights",
    }
