from pathlib import Path

import pandas as pd
import pytest
from pandas.core.frame import DataFrame
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


@pytest.fixture
def licenses_df(licenses: list[dict]) -> DataFrame:
    return pd.DataFrame(licenses)


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


@pytest.mark.vcr("license_list.yaml")
@pytest.mark.default_cassette("license_details.yaml")
def test_license_details(scraper: LicenseScraper, licenses_df: DataFrame) -> None:
    first_five_licenses_df = licenses_df.head(n=5)
    assert len(first_five_licenses_df.columns) == 39

    licenses_with_details_df = scraper.enrich_with_details(first_five_licenses_df)
    first_license_with_details_df = licenses_with_details_df.head(n=1)
    assert len(first_license_with_details_df.columns) == 40

    first_license_supplimental_info = first_license_with_details_df["businessLicense"].iloc[0]["BL Supplimental Information"]
    assert len(first_license_supplimental_info) == 12

    first_unit_df = first_license_supplimental_info["1"]
    assert len(first_unit_df) == 17
    assert first_unit_df["Base Rent @ Row 1"] == 1450.0
    assert first_unit_df["Current Rent (as of Nov 1) @ Row 1"] == 1530.0
