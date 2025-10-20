#!/usr/bin/env python3

# Copyright 2014 Brett Slatkin, Pearson Education Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Preamble to mimick book environment
import logging
from pprint import pprint
from sys import stdout as STDOUT


# Example 1
import sys
print(sys.version_info)
print(sys.version)

###
#! /opt/local/bin/python3

# ----- System Imports -----
import requests

# ----- Constants -----
C_PROXIES = {
    "http": "wwwproxy.frb.gov:8080",
    "https": "wwwproxy.frb.gov:8080",
    "NO_PROXY": "*.frb.gov"}
""" Proxy server values. """

def get_collection_uids_for_start_end_dates(collection, start_date,end_date=None):
    """ Get All metadata for a Collection

    Args:
        i_collection (str): The name of the collection.
    """

    try:
        v_result = requests.get(
            "https://udr-test-api.frb.gov/getCollectionMetadata/?collectionName="
            f"{collection}&startDate={start_date}&endDate={end_date}",
            verify=True,
            timeout=10)

        if v_result.status_code != 200:
            raise Exception("Could not return collection metadata.")

        return [uid["uniqueIdentifier"] for uid in v_result.json()["results"]]

    except Exception as v_error:
        logging.error(v_error)
        raise

def get_collection_text_for_uid(i_collection, i_unique_identifier, i_concatenated=False):
    """ Get Text for a document

    Args:
        i_collectoin (str): The name of the collection.
        i_unique_identifier (str): The unique identifier.
        i_concatenated (bool): True = Return in string format, False = Return in list format.

    Returns:
        str | list: The document text.
    """

    try:
        v_result = requests.get(
            "https://udr-test-api.frb.gov/getDocumentText/?collectionName="
            f"{i_collection}&uniqueIdentifier={i_unique_identifier}",
            verify=True,
            timeout=10)

        if v_result.status_code != 200:
            raise Exception("Could not return document text.")

        if i_concatenated is True:
            return re.sub(r'\s+', ' ', "".join([v_page["pageText"] for v_page in v_result.json()]))

        return v_result.json()

    except Exception as v_error:
        logging.error(v_error)
        raise

def write_collection_text_for_uid(collection, unique_id, collection_pages_for_uid):
    with open(f"{collection}_{unique_id}", "a", encoding="utf-8") as f:
        f.write(f"collection:{collection}, unique_identifier:{unique_id}\n")
        for rec in collection_pages_for_uid:
            f.write(f"page_no:{rec['pageNum']}\npage_text:{rec['pageText']}\n")

class Args:
    def __init__(self,collectionName,firstPublicationDate,lastPublicationDate):
        self.collectionName=collectionName
        self.firstPublicationDate=firstPublicationDate
        self.lastPublicationDate=lastPublicationDate
        
def main():
    
    
    args=[
        Args("fomc_historical_meeting_minutes", "1936-03-18","1967-05-23"),
        Args("fomc_meeting_minutes", "2007-10-31", "2024-12-18" )
        ]
    

    for arg in args:
        v_collection_unique_ids = get_collection_uids_for_start_end_dates(collection=arg.collectionName, start_date=arg.firstPublicationDate, end_date=arg.lastPublicationDate)

        for uid in v_collection_unique_ids:

            # ---------- Part 4: Get Document Text ----------
            # ----- Document Text -----
            collection_pages_for_uid = get_collection_text_for_uid(
                i_collection=arg.collectionName,
                i_unique_identifier=uid,
                i_concatenated=False)

            write_collection_text_for_uid(arg.collectionName, uid, collection_pages_for_uid)
if __name__ == "__main__":
    main()

###
