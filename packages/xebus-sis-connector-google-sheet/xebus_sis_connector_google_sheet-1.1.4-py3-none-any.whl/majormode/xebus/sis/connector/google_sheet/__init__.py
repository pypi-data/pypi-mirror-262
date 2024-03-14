# Copyright (C) 2024 Majormode.  All rights reserved.
#
# This software is the confidential and proprietary information of
# Majormode or one of its subsidiaries.  You shall not disclose this
# confidential information and shall use it only in accordance with the
# terms of the license agreement or other applicable agreement you
# entered into with Majormode.
#
# MAJORMODE MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY
# OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE, OR NON-INFRINGEMENT.  MAJORMODE SHALL NOT BE LIABLE FOR ANY
# LOSSES OR DAMAGES SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING
# OR DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.

from __future__ import annotations

import logging
import os
from os import PathLike
from pathlib import Path

import gspread
from majormode.perseus.model.country import Country
from majormode.perseus.model.date import ISO8601DateTime
from majormode.perseus.model.locale import Locale
from majormode.perseus.utils import cast
from majormode.perseus.utils import module_utils
from majormode.xebus.constant.family_sheet import DEFAULT_COUNTRIES_NAMES_MAPPING_SHEET_NAME
from majormode.xebus.constant.family_sheet import DEFAULT_FAMILIES_SHEET_NAME
from majormode.xebus.constant.family_sheet import DEFAULT_GRADES_NAMES_MAPPING_SHEET_NAME
from majormode.xebus.constant.family_sheet import DEFAULT_LANGUAGES_NAMES_MAPPING_SHEET_NAME
from majormode.xebus.model.family import FamilyData
from majormode.xebus.model.family_sheet import FamilyDataSectionedSheet

from majormode.xebus.sis.connector.constant.vendor import SisVendor
from majormode.xebus.sis.connector.sis_connector import SisConnector
from majormode.xebus.utils import normalization_utils

# Define the absolute path to the data of this Python library.
#
# The data of this Python library are located in a folder ``data`` located
# at the root path of this Python library.
#
# We have organized our Python modules in a source folder ``src`` located
# at the root path of this Python library, therefore the source depth is
# ``1`` (not ``0``).
LIBRARY_DATA_PATH = os.path.join(
    module_utils.get_project_root_path(__file__, __name__, 1),
    'data'
)


class GoogleSheetConnector(SisConnector):
    """
    Connector to a Google Sheets spreadsheet containing an organization's
    family data.
    """
    @classmethod
    def __fetch_google_sheet_rows(
            cls,
            google_client: gspread.client.Client,
            spreadsheet_url: str,
            sheet_name: str
    ) -> list[list[str]]:
        """
        Fetch the families data from the specified Google Sheet.


        :param google_client: The client instance to communicate with Google
            API.

        :param spreadsheet_url: The Uniform Resource Locator (URL) of the
            Google spreadsheet.

        :param sheet_name: The name of the sheet to returns the rows.


        :return: A list of rows containing each the information about a child
            and their legal guardians.
        """
        spreadsheet = google_client.open_by_url(spreadsheet_url)
        worksheet = spreadsheet.worksheet(sheet_name)

        # Read the whole content of the sheet in one go.
        #
        # @note: This code is faster than the simpler following version that
        #     does multiple API network calls:
        #
        # ```python
        # rows = [
        #     worksheet.row_values(i)
        #     for i in range(1, worksheet.row_count + 1)
        # ]
        # ```
        cells = worksheet.range(1, 1, worksheet.row_count, worksheet.col_count)
        rows = [
            [
                cell.value
                for cell in cells[row_index * worksheet.col_count: (row_index + 1) * worksheet.col_count]
            ]
            for row_index in range(worksheet.row_count)
        ]

        return rows

    @classmethod
    def __fetch_grades_names_mapping_from_google_sheet(
            cls,
            google_client: gspread.client.Client,
            spreadsheet_url: str,
            sheet_name: str
    ) -> dict[str, int]:
        """
        Fetch the list of education grades of the school organization.


        :param google_client: The client instance to communicate with Google
            API.

        :param spreadsheet_url: The Uniform Resource Locator (URL) of the
            Google spreadsheet.

        :param sheet_name: The name of the sheet that contains the school's
            organization's education grades.


        :return: A dictionary of education grades where the key corresponds to
            the name of an education grades and the value corresponds to the
            number of the year a pupil has reached in this given educational
            stage for this grade.
        """
        rows = cls.__fetch_google_sheet_rows(google_client, spreadsheet_url, sheet_name)

        education_grades_names_mapping = {
            grade_name: int(grade_level)
            for grade_name, grade_level in rows
            if grade_name
        }

        return education_grades_names_mapping

    @classmethod
    def __fetch_languages_names_mapping_from_google_sheet(
            cls,
            google_client: gspread.client.Client,
            spreadsheet_url: str,
            sheet_name: str
    ) -> dict[str, Locale]:
        """
        Return the mapping between the names of languages and their respective
        ISO 639-3:2007 codes.


        :param google_client: The client instance to communicate with Google
            API.

        :param spreadsheet_url: The Uniform Resource Locator (URL) of the
            Google spreadsheet.

        :param sheet_name: The name of the sheet that contains the mapping
            between languages names and their respective ISO 639-3:2007 codes.


        :return: A dictionary representing a mapping between the names of
            languages (the keys), localized in the specified language, and
            their corresponding ISO 639-3:2007 codes (the values).
        """
        rows = cls.__fetch_google_sheet_rows(google_client, spreadsheet_url, sheet_name)

        languages_names_iso_codes_mapping = {
            name: Locale(iso_639_3_code)
            for name, iso_639_3_code in rows
            if name  # Ignore empty rows at the end of the sheet
        }

        return languages_names_iso_codes_mapping

    @classmethod
    def __fetch_nationalities_names_mapping_from_google_sheet(
            cls,
            google_client: gspread.client.Client,
            spreadsheet_url: str,
            sheet_name: str
    ) -> dict[str, Country]:
        """
        Return the mapping between the names of nationalities and their
        respective ISO 3166-1 alpha-2 codes.


        :param google_client: The client instance to communicate with Google
            API.

        :param spreadsheet_url: The Uniform Resource Locator (URL) of the
            Google spreadsheet.

        :param sheet_name: The name of the sheet that contains the mapping
            between languages names and their respective ISO 639-3:2007 codes.


        :return: A dictionary representing a mapping between the names of
            nationalities (the keys), localized in the specified langauge, and
            their corresponding ISO 3166-1 alpha-2 codes (the values).
        """
        rows = cls.__fetch_google_sheet_rows(google_client, spreadsheet_url, sheet_name)

        nationalities_names_iso_codes_mapping = {
            name: Country(iso_3166_alpha2_code)
            for name, iso_3166_alpha2_code in rows
            if name  # Ignore empty rows at the end of the sheet
        }

        return nationalities_names_iso_codes_mapping

    def __init__(
            self,
            google_service_account_file_path_name: PathLike,
            spreadsheet_url: str,
            families_sheet_name: str = None
    ):
        """
        Build a new connector to access a Google Sheet spreadsheet.


        :param google_service_account_file_path_name:

        :param spreadsheet_url: The Uniform Resource Locator (URL) of the
            Google spreadsheet.

        :param families_sheet_name: The name of the sheet that contains the
            families data of a school organization.
        """
        super().__init__(SisVendor.google_sheet)

        self.__google_client = gspread.service_account(filename=str(google_service_account_file_path_name))
        self.__spreadsheet_url = spreadsheet_url
        self.__families_sheet_name = families_sheet_name or DEFAULT_FAMILIES_SHEET_NAME

        # The mappings between entities names and their corresponding codes
        # are lazily loaded when the family list is fetched from the school
        # organization's Google Sheets.
        self.__grades_names_mapping: dict[str, int] | None = None
        self.__languages_names_mapping: dict[str, Locale] | None = None
        self.__nationalities_names_mapping: dict[str, Country] | None = None

    def fetch_family_data(self) -> FamilyData:
        """
        Returns the data of the families to synchronize.


        :return: The data of the families to synchronize.
        """
        # Fetch rows from the Google Sheets and create a family data sectioned
        # sheet.
        logging.debug(
            f"Fetching rows from the Google Sheets \"{self.__spreadsheet_url}\" "
            f"sheet \"{self.__families_sheet_name}\"..."
        )

        google_sheet_rows = self.__fetch_google_sheet_rows(
            self.__google_client,
            self.__spreadsheet_url,
            self.__families_sheet_name
        )

        # Fetch the education grades of the school organization.
        if self.__grades_names_mapping is None:
            logging.debug(
                "Fetching the school education's grades names mapping from the sheet "
                f"\"{DEFAULT_GRADES_NAMES_MAPPING_SHEET_NAME}\"..."
            )

            self.__grades_names_mapping = normalization_utils.normalize_names_codes_mapping(
                self.__fetch_grades_names_mapping_from_google_sheet(
                    self.__google_client,
                    self.__spreadsheet_url,
                    DEFAULT_GRADES_NAMES_MAPPING_SHEET_NAME
                )
            )

        # Fetch the languages names mapping.
        if self.__languages_names_mapping is None:
            logging.debug(
                "Fetching the languages names mapping from the sheet "
                f"\"{DEFAULT_LANGUAGES_NAMES_MAPPING_SHEET_NAME}\"..."
            )

            self.__languages_names_mapping = normalization_utils.normalize_names_codes_mapping(
                self.__fetch_languages_names_mapping_from_google_sheet(
                    self.__google_client,
                    self.__spreadsheet_url,
                    DEFAULT_LANGUAGES_NAMES_MAPPING_SHEET_NAME
                )
            )

        # Fetch the nationalities (alias, the countries) names mapping.
        if self.__nationalities_names_mapping is None:
            logging.debug(
                "Fetching the nationalities names mapping from the sheet "
                f"\"{DEFAULT_COUNTRIES_NAMES_MAPPING_SHEET_NAME}\"..."
            )

            self.__nationalities_names_mapping = normalization_utils.normalize_names_codes_mapping(
                self.__fetch_nationalities_names_mapping_from_google_sheet(
                    self.__google_client,
                    self.__spreadsheet_url,
                    DEFAULT_COUNTRIES_NAMES_MAPPING_SHEET_NAME
                )
            )

        # Convert the Google Sheet rows into a Xebus data structure.
        family_data_sectioned_sheet = FamilyDataSectionedSheet(
            google_sheet_rows,
            self.__grades_names_mapping,
            languages_names_mapping=self.__languages_names_mapping,
            nationalities_names_mapping=self.__nationalities_names_mapping
        )

        xebus_rows = family_data_sectioned_sheet.rows

        # Build the families entities.
        family_data = FamilyData(xebus_rows)

        return family_data

    def fetch_update_time(self) -> ISO8601DateTime:
        """
        Return the time of the most recent update of the family list.


        :return: The time the family list was last updated.
        """
        spreadsheet = self.__google_client.open_by_url(self.__spreadsheet_url)
        last_update_time = cast.string_to_timestamp(spreadsheet.lastUpdateTime)
        return last_update_time
