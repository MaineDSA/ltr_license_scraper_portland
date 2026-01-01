"""
Download landlord license data from the City of Portland website and save to CSV.

This script queries the Portland self-service API to retrieve landlord licenses
(Multi-Family, Single-Family, and Two-Family) issued since 2022-01-01.
"""

import logging
from dataclasses import dataclass
from pathlib import Path
from time import sleep
from typing import Any

import pandas as pd
from requests import Session
from tqdm import tqdm

from api_payloads import LicenseType, build_search_payload

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Config:
    """Configuration settings for the scraper."""

    test_mode: bool = False
    page_size: int = 20 if test_mode else 200
    rate_limit_delay: float = 2.5
    output_file: Path = Path("./saved.csv")
    issue_date_from: str = "2022-01-01T05:00:00.000Z"


@dataclass
class APIEndpoints:
    """API endpoint URLs."""

    base_url: str = "https://selfservice.portlandmaine.gov/energov_prod/selfservice/api/energov"

    @property
    def license_details(self) -> str:
        return f"{self.base_url}/customfields/data"

    @property
    def search(self) -> str:
        return f"{self.base_url}/search/search"


REQUEST_HEADERS = {
    "tenantId": "1",
    "tenantName": "EnerGovProd",
    "Referer": "https://selfservice.portlandmaine.gov/energov_prod/selfservice",
    "DNT": "1",
}


class LicenseScraper:
    """Scraper for Portland landlord licenses."""

    def __init__(self, session: Session, config: Config) -> None:
        self.session = session
        self.config = config
        self.endpoints = APIEndpoints()

    def _extract_label(self, data: dict[str, Any]) -> str:
        """Extract the most human-readable field name from license data."""
        return data.get("Label") or data.get("FieldName") or data.get("CustomField") or str(data.get("Id", ""))

    def _extract_value(self, data: dict[str, Any]) -> str | dict[str, dict[str, str]] | None:
        """
        Extract the value from a license data field.

        Returns either a simple string value, a nested dictionary structure
        for table rows, or None if no value exists.
        """
        license_units = data.get("CustomFieldTableRows")
        if license_units:
            return {
                unit["Column0"]["Value"]: {
                    self._extract_label(unit[column]): unit[column]["Value"] for column in unit if column.startswith("Column") and unit[column]
                }
                for unit in license_units
            }

        return data.get("Value")

    def get_license_details(self, license_id: str) -> dict[str, str | dict[str, dict[str, str]] | None]:
        """
        Fetch detailed information for a specific license.

        Args:
        license_id: The unique identifier for the license

        Returns:
        Dictionary mapping field labels to their values

        """
        payload = {
            "EntityId": license_id,
            "ModuleId": 8,
            "LayoutId": "b589c49c-cc17-435d-b2d8-43a1e10e5b6d",
            "OnlineLayoutId": "e7d5dda1-27cb-4d0d-8128-58e979697587",
        }

        response = self.session.post(self.endpoints.license_details, headers=REQUEST_HEADERS, json=payload)
        response.raise_for_status()

        sleep(self.config.rate_limit_delay)

        custom_fields = response.json()["Result"]["CustomGroups"][0]["CustomFields"]

        return {self._extract_label(field): self._extract_value(field) for field in custom_fields}

    def search_licenses(self, license_type: LicenseType, page_number: int) -> tuple[int, list[dict]]:
        """
        Search for licenses of a specific type.

        Args:
        license_type: LicenseType enum member
        page_number: Page number to retrieve

        Returns:
        Tuple of (total_pages, list of license results)

        """
        payload = build_search_payload(
            license_type=license_type, page_number=page_number, page_size=self.config.page_size, issue_date_from=self.config.issue_date_from
        )

        response = self.session.post(self.endpoints.search, headers=REQUEST_HEADERS, json=payload)
        response.raise_for_status()

        sleep(self.config.rate_limit_delay)

        result = response.json().get("Result", {})
        return result.get("TotalPages", 0), result.get("EntityResults", [])

    def fetch_all_licenses(self) -> list[dict]:
        """
        Fetch all licenses across all license types.

        Returns:
        List of all license records

        """
        all_licenses = []

        for license_type in LicenseType:
            logger.info("Fetching %s licenses...", license_type.display_name)

            total_pages, first_page_results = self.search_licenses(license_type, 1)
            all_licenses.extend(first_page_results)

            if self.config.test_mode:
                logger.info("Test mode: Retrieved page 1 of %s for %s", total_pages, license_type.display_name)
                continue

            logger.info("Retrieving all %s pages of %s", total_pages, license_type.display_name)

            for page_num in tqdm(range(2, total_pages + 1), unit="page", initial=1, total=total_pages, desc=license_type.display_name):
                _, page_results = self.search_licenses(license_type, page_num)
                all_licenses.extend(page_results)

        return all_licenses

    def enrich_with_details(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add detailed information to each license record.

        Args:
        df: DataFrame containing basic license information

        Returns:
        DataFrame with added license details

        """
        tqdm.pandas(unit="licenses", desc="Fetching details")
        logger.info("Downloading license details for %s licenses", len(df))

        df["businessLicense"] = df["CaseId"].progress_apply(self.get_license_details)
        return df


def main() -> None:
    """Download license data and save to CSV."""
    config = Config()

    with Session() as session:
        scraper = LicenseScraper(session, config)

        # Fetch all licenses
        licenses = scraper.fetch_all_licenses()
        df = pd.DataFrame(licenses)

        # Enrich with detailed information
        df = scraper.enrich_with_details(df)

        # Save to CSV
        df.to_csv(config.output_file, encoding="utf-8", index=False)
        logger.info("Saved %s licenses to %s", len(df), config.output_file)


if __name__ == "__main__":
    main()
