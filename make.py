#!/usr/bin/env python
"""
This script is responsible for initializing a database, processing sources for scraping and parsing,
and moving generated static files to a specified directory. It integrates various scrapers and parsers
to handle data from multiple platforms and formats.
"""
import json
import sys
import os
import shutil
from parsers import no_intro
from scrapers import myrient, internet_archive, nopaystation, mariocube
from parsers import libretro, gametdb, mame, wii_rom_set_by_ghostware
from database import db_manager

SCRAPERS = {
    'myrient': myrient,
    'internet_archive': internet_archive,
    'nopaystation': nopaystation,
    'mariocube': mariocube
}

PARSERS = {
    'no_intro': no_intro,
    'libretro': libretro,
    'gametdb': gametdb,
    'mame': mame,
    'wii_rom_set_by_ghostware': wii_rom_set_by_ghostware
}


def load_sources(file_path='sources.json'):
    """Load sources from a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)


def load_config(file_path='config.json'):
    """Load configuration from a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)


def get_scraper(name):
    """Retrieve a scraper by its name."""
    return SCRAPERS.get(name)


def get_parser(name):
    """Retrieve a parser by its name."""
    return PARSERS.get(name)


def process_sources(sources, use_cached):
    """Process the sources to scrape, parse, and insert data into the database."""
    for platform, source_list in sources.items():
        print(f"\n{platform}:")
        for i, source in enumerate(source_list, start=1):
            print(f"  {i}) ", end='')
            print(f"[{source['format']}] ", end='')
            if source['regions']:
                print(f"[{', '.join(source['regions'])}] ", end='')
            print(f"[{source['scraper']}] ", end='')
            print(f"[{source['type']}]")

            scraper = get_scraper(source['scraper'])
            if not scraper:
                print(f"Scraper '{source['scraper']}' not found.")
                sys.exit(1)

            entries = scraper.scrape(source, platform, use_cached)

            for parser_name, parser_flags in source['parsers'].items():
                parser = get_parser(parser_name)
                if not parser:
                    print(f"Parser '{parser_name}' not found.")
                    sys.exit(1)

                entries = parser.parse(entries, parser_flags)

            for entry in entries:
                db_manager.insert_entry(entry)


def move_static_files(destination_dir, static_dir='static'):
    """Move the contents of the static directory to the destination directory, overwriting if necessary."""
    if not os.path.exists(static_dir):
        return

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    for item in os.listdir(static_dir):
        source_path = os.path.join(static_dir, item)
        destination_path = os.path.join(destination_dir, item)

        if os.path.exists(destination_path):
            # Remove existing file or directory
            if os.path.isdir(destination_path):
                shutil.rmtree(destination_path)
            else:
                os.remove(destination_path)

        # Move the source to the destination
        shutil.move(source_path, destination_dir)


def make(use_cached=False):
    """Main function to initialize the database, process sources, and close the database."""
    config = load_config()
    sources = load_sources()
    db_manager.init_database()

    process_sources(sources, use_cached)

    db_manager.close_database()
    print("Database created successfully.")

    static_files_dir_path = config.get('static_files_dir_path')
    if static_files_dir_path:
        move_static_files(static_files_dir_path)
        print(f"Static files moved to '{static_files_dir_path}'.")


if __name__ == '__main__':
    # Change directory to script location
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    args = sys.argv[1:] if len(sys.argv) > 1 else []
    use_cached = '--use-cached' in args

    make(use_cached)
