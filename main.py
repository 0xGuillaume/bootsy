#!/usr/bin/python3
import sys
import logging
import tempfile
import argparse
from pathlib import Path
import tomllib


FORMAT = '[BOOTSY] %(message)s'
logging.basicConfig(format=FORMAT)


with open("bootsy.toml", "rb") as file:
    config = tomllib.load(file)


parser = argparse.ArgumentParser(
    prog="Bootsy",
    description="Setup a programming language environment based on a TOML configuration file.",
    epilog="By 0xGuillaume"
)

parser.add_argument("env", help="Chose an environment to setup.", choices=config)
parser.add_argument("-p", "--path", help="Specify a path to set up the envrionment. Default is working directory.", required=False)

args = parser.parse_args()


if not args.path:
    path = Path.cwd()

else:
    path = Path(args.path)


def is_files_and_dirs_key() -> bool:
    """Check if both required keys : files & dirs are specified.

    Returns:
        A boolean indicating if keys are compliants.
    """

    compliant = True

    for env in config:
        if not "dirs" in config[env]:  
            logging.error(f"[{env}] - Key 'dirs' is required but missing.")
            compliant = False

        if not "files" in config[env]:
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

    for env in config:
        with tempfile.TemporaryDirectory() as tmpdir:
            for directory in config[env]["dirs"]:
                try:
                    _path = Path(tmpdir) / directory
                    _path.mkdir()

                except (
                    FileNotFoundError,
                    FileExistsError
                ) as error:
                    logging.error(f"[{env}] - Directory '{directory}' cannot be created. Path may not exist.")
                    compliant = False

            for file in config[env]["files"]:
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

    for directory in config[args.env]["dirs"]:
        path_ = path / directory

        try:
            path_.mkdir()

        except FileExistsError:
            logging.error(f"[{env}] - Directory '{directory}' already exists.")


def touch() -> None:
    """Create files."""

    for file in config[args.env]["files"]:
        path_ = path / file

        try:
            path_.touch()

        except FileNotFoundError:
            logging.error(f"[{env}] - File '{file}' already exists.")


if __name__ == "__main__":

    if is_config_compliant():
        mkdir()
        touch()
