#!/usr/bin/python3
import logging
from argparse import ArgumentParser
from os import environ
from pathlib import Path
from tempfile import TemporaryDirectory
from tomllib import load


VENV_CONFIG = environ.get("BOOTSY")
DEFAULT_CONFIG = "~/.config/.bootsy.toml"
FORMAT = '[BOOTSY] %(message)s'


def read_config() -> dict:
    """Read bootsy TOML config.

    Returns:
        A dict containing bootsy config.
    """

    if not VENV_CONFIG:
        #with open(DEFAULT_CONFIG, "rb") as config:
        with open("bootsy.toml", "rb") as config:
            return load(config)


CONFIG = read_config()


def is_files_and_dirs_key() -> bool:
    """Check if both required keys : files & dirs are specified.

    Returns:
        A boolean indicating if keys are compliants.
    """

    compliant = True

    for env in CONFIG:
        if not "dirs" in CONFIG[env]:  
            logging.error(f"[{env}] - Key 'dirs' is required but missing.")
            compliant = False

        if not "files" in CONFIG[env]:
            logging.error(f"[{env}] - Key 'files' is required but missing.")
            compliant = False

    return compliant


def is_given_path_exists() -> bool:
    """Check if dirs & files could be created based
    on filled paths.

    Returns:
        A boolean indicating if filled paths could exist.
    """

    compliant = True

    for env in CONFIG:
        with TemporaryDirectory() as tmpdir:
            for directory in CONFIG[env]["dirs"]:
                try:
                    _path = Path(tmpdir) / directory
                    _path.mkdir()

                except (
                    FileNotFoundError,
                    FileExistsError
                ) as error:
                    logging.error(f"[{env}] - Directory '{directory}' cannot be created. Path may not exist.")
                    compliant = False

            for file in CONFIG[env]["files"]:
                try:
                    _path = Path(tmpdir) / file
                    _path.touch()

                except (
                    FileNotFoundError, 
                    FileExistsError
                ) as error:
                    logging.error(f"[{env}] - File '{file}' cannot be created. Path may not exist.")
                    compliant = False
            
    return compliant 


def is_config_compliant() -> bool:
    """Check wether or not bootsy TOML config is compliant.

    Returns:
        A boolean indicating the config compliancy.
    """

    return is_files_and_dirs_key() and is_given_path_exists()


def mkdir() -> None:
    """Create directories."""

    for directory in CONFIG[args.env]["dirs"]:
        path_ = path / directory

        try:
            path_.mkdir()

        except FileExistsError:
            logging.error(f"[{env}] - Directory '{directory}' already exists.")


def touch() -> None:
    """Create files."""

    for file in CONFIG[args.env]["files"]:
        path_ = path / file

        try:
            path_.touch()

        except FileNotFoundError:
            logging.error(f"[{env}] - File '{file}' already exists.")


if __name__ == "__main__":
    logging.basicConfig(format=FORMAT)

    parser = ArgumentParser(
        prog="Bootsy",
        description="Setup a programming language environment based on a TOML configuration file.",
    )

    parser.add_argument("env", help="Pick an environment to setup.", choices=CONFIG)
    parser.add_argument("-p", "--path", help="Specify a path to set up the envrionment. Default is working directory.", required=False)

    args = parser.parse_args()


    if not args.path:
        path = Path.cwd()

    else:
        path = Path(args.path)

    if is_config_compliant():
        mkdir()
        touch()
