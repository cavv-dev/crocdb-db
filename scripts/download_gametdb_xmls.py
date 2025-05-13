#!/usr/bin/env python
"""
This script downloads and extracts GameTDB XML files from predefined URLs. 
The files are downloaded as ZIP archives, extracted to a specified directory, 
and the ZIP files are removed after extraction.
"""
import os
import sys
import zipfile
import requests

URLS = [
    'https://www.gametdb.com/dstdb.zip?LANG=EN',
    'https://www.gametdb.com/wiitdb.zip?LANG=EN&WIIWARE=1&GAMECUBE=1',
    'https://www.gametdb.com/3dstdb.zip?LANG=EN',
    'https://www.gametdb.com/wiiutdb.zip?LANG=EN',
    'https://www.gametdb.com/ps3tdb.zip?LANG=EN'
]

XML_FILES = [
    'dstdb.xml',
    'wiitdb.xml',
    '3dstdb.xml',
    'wiiutdb.xml',
    'ps3tdb.xml'
]


def download_gametdb_xmls():
    """Download and extract GameTDB XML files from predefined URLs."""
    print("Downloading and extracting GameTDB XML files...")

    # Destination directory for downloaded and extracted files
    destination = 'data/gametdb'
    os.makedirs(destination, exist_ok=True)

    for url, xml_file in zip(URLS, XML_FILES):
        try:
            # Download the file
            r = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36'
            }, timeout=5)

            if r.ok:
                # Extract the ZIP file name from the URL
                zip_file_name = url.split('/')[-1].split('?')[0]
                zip_file_path = os.path.join(destination, zip_file_name)

                # Save the downloaded content to a file
                with open(zip_file_path, 'wb') as f:
                    f.write(r.content)
                print(f"Downloaded: {zip_file_path}")

                # Extract the contents of the ZIP file
                with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                    zip_ref.extractall(destination)
                print(f"Extracted: {zip_file_path}")

                # Remove the ZIP file after extraction
                os.remove(zip_file_path)
            else:
                raise Exception(
                    f"Failed to download {url} with status code {r.status_code}")

        except Exception as e:
            xml_file_path = os.path.join(destination, xml_file)
            if os.path.exists(xml_file_path):
                print(
                    f"Download failed for {url}, but {xml_file} already exists.")
            else:
                print(f"Download failed for {url}. Error: {e}")
                sys.exit(1)


if __name__ == '__main__':
    # Change the working directory to main db repository location
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    os.chdir('../')

    download_gametdb_xmls()
