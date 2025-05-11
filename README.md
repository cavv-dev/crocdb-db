# Crocdb Database

This codebase includes modules and scripts used for creating the ROMs database utilized by [Crocdb](https://crocdb.net).

## Codebase understanding
The code is built with modularity in mind. The main groups of modules are:
- `scrapers` - Used for scraping the sources URLs responses. Ideally each module represents a different host, like `myrient.py` for Myrient and `internet_archive.py` for Internet Archive.

- `parsers` - Used for parsing entries scraped by the scrapers modules, enriching each entry with appropriate information.

### Main scripts
- `make.py` - Initializes the database and starts processing the sources. Can use cached responses from sources URLs by passing `--use-cached`, useful for testing purposes.

- `workflow.py` - Initiates the workflow needed for updating additional data needed by scrapers/parsers and starting the database creation.

## Available scraping/parsing modules
### Scrapers
- `myrient` - Indexes from Myrient.
- `internet_archive` - Indexes from Internet Archive. Log in credentials have to be specified in `internet_archive_creds.json` to allow for restricted content to be scraped.
- `nopaystation` - TSV files from NoPayStation.
- `mariocube` - Indexes from MarioCube.

### Parsers
- `libretro` - Adds ROM IDs and Box art URLs to entries that are listed in the Libretro DAT files by checking title correspondences.

  Flags: None

- `no_intro` - Performs regions extraction from the ROM's title and refactors it by excluding unnecessary content. Designed to work with entries that have titles following the No-Intro naming convention.

  Flags:
  - **parse_title_regions** *(true, false)*, default is *true*. Perform regions extraction from the ROM's title.
  - **clean_title_contents** *(true, false)*, default is *true*. Refactor the ROM's title by excluding unnecessary content, like regions and languages.
  - **move_title_article** *(true, false)*, default is *true*. If exists, move the article in the ROM's title to the original position. E.g. `Legend of Zelda, The` becomes `The Legend of Zelda`.

- `gametdb` - Adds title and Box art URLs to entries present in GameTDB.

  Flags:
  - **parse_boxart** *(true, false)*, default is *true*. Perform Box art URL parsing from ROM ID.
  - **parse_name** *(true, false)*, default is *false*. Perform title parsing from ROM ID.

- `mame` - Adds full title to entries based on an already set title that has to correspond to the original MAME ROM's name. 

  Flags: None

- `wii_rom_set_by_ghostware` - Parses the ROM ID from the title and refactors it by excluding the ID. Built specifically for the *WiiRomSetByGhostware* source.

  Flags: None

## Sources structure
The sources are contained in the `sources.json` file and are grouped by platform IDs. Each key corresponds to a list of sources for that platform.

Example:
```jsonc
{
    "nes": [
        // sources for NES here
    ],
    "snes": [
        // sources for SNES here
    ],
    // ...
}
```

Each source is a JSON object that must contain the following elements:

- `format` - The file format of the distributed ROMs. It can be:

  - specific, when the files have a specific format/extension. Has to be written in lowercase.
    
    E.g. `nes` for `.nes` files.
  - generic, when the files are not in a specific file format. Has to be written in uppercase.
  
    E.g. `DUMP` for dumped ROMs without file extension.

- `regions` - List of regions that all entries in the source have. Can be empty to let parsers define regions for each entry independently.

- `urls` - List of URLs that return parseable entries.

- `scraper` - The scraper to use for each URL. Check the [scrapers](#scrapers) modules for available options.

- `filter` - Regex pattern used for selecting valid entries in the scraped URL response. It can include a capture group to exclude parts of the name, such as the file extension.

- `parsers` - Parsers to use on scraped entries in order. It's in form of a JSON object where each key is the parser to use and the value is the flag map to use. Check the [parsers](#parsers) modules for available options.

- `type` - The display name for the type of each ROM. E.g. `Game` for games, `DLC` for DLCs.

Example:
```json
{
    "format": "nes",
    "regions": [],
    "urls": [
        "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%20Entertainment%20System%20%28Headered%29/",
        "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%20Entertainment%20System%20%28Headerless%29%20%28Private%29/"
    ],
    "scraper": "myrient",
    "filter": "(.*)\\.zip",
    "parsers": {
        "libretro": {},
        "no_intro": {}
    },
    "type": "Game"
}
```

## Contributing
Contributions are welcome. Whether you have a source to add to Crocdb or a correction to do, feel free to apply your changes through GitHub pull requests.

Refer to the [Sources structure](#sources-structure) section for adding and editing sources.

For any complication or question feel free to [contact me](https://crocdb.net/about/#contact).
