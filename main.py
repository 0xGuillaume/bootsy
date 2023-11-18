#!/usr/bin/python3
import sys
import logging
import tempfile
import argparse
from pathlib import Path
import tomllib


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

# ==================================================================


def is_files_and_dirs_key() -> bool:
    """."""

    compliant = True

    for env in config:
        if not "dirs" in config[env]:  
            logging.error(f"No dirs key in env : {config[env]}")
            compliant = False

        if not "files" in config[env]:
            logging.error(f"No files key in env : {config[env]}")
            compliant = False

    return compliant


def is_given_path_exists() -> bool:
    """Check wether or not the TOML config file is compliant."""

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
                    logging.error(f"directory do not exists : {directory}")
                    compliant = False

            for file in config[env]["files"]:
                try:
                    _path = Path(tmpdir) / file
                    _path.touch()

                except (
                    FileNotFoundError, 
                    FileExistsError
                ) as error:
                    logging.error(f"file do not exists : {file}")
                    compliant = False
            
    return compliant 


def is_config_compliant() -> bool:
    return is_files_and_dirs_key() and is_given_path_exists()


def mkdir() -> None:
    """Create new directories."""

    for directory in config[args.env]["dirs"]:
        path_ = path / directory

        try:
            path_.mkdir()

        except FileExistsError:
            print(f"Directory {directory} already exists.")


def touch() -> None:
    """Create new files."""

    for file in config[args.env]["files"]:
        path_ = path / file

        try:
            path_.touch()

        except FileNotFoundError:
            print(f"File {file} can't be created. Wrong path.")


if __name__ == "__main__":


    if not is_files_and_dirs_key():
        sys.exit()

    if not is_given_path_exists(): 
        sys.exit()

    if not any(vars(args).values()):
        parser.error("Aucun env spécifié")
    
    #if is_config_compliant():
    #    mkdir()
    #    touch()
