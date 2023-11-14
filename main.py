#!/usr/bin/python3
import tempfile
import argparse
from pathlib import Path
import tomllib


with open("bootsy.toml", "rb") as file:
    config = tomllib.load(file)

parser = argparse.ArgumentParser(
                    prog="Bootsy",
                    description="Setup a programming language environment based on a TOML configuration file.",
                    epilog="By 0xGuillaume")

parser.add_argument("env", help="Chose an environment to setup.", choices=config)
parser.add_argument("-p", "--path", help="Specify a path to set up the envrionment. Default is working directory.", required=False)

args = parser.parse_args()

if not args.path:
    path = Path.cwd()

else:
    path = Path(args.path)


# ==================================================================

def is_config_compliant() -> bool:
    """Check wether or not the TOML config file is compliant."""

    compliant = True

    for env in config:

        with tempfile.TemporaryDirectory() as tmpdir:
            for dir_ in config[env]["dirs"]:
                _path = Path(tmpdir) / dir_
                _path.mkdir()

            try:
                for file in config[env]["files"]:
                    _path = Path(tmpdir) / file
                    _path.touch()

            except FileNotFoundError as error:
                print("file do not exists :", file)
                compliant = False
            
    return compliant 
        


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
    if not any(vars(args).values()):
        parser.error("Aucun env spécifié")
    
    if is_config_compliant():
        mkdir()
        touch()

