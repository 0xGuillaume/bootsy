# Bootsy

**Bootsy** is a lightweight tool I am using to bootstrap a new programming environnment with required files and directories I need.
The tool is made in _Python_ with only built-in packages to avoid installing additional packages.


## Configuraiton

**Bootsy** configuration is based on a [TOML](https://toml.io/en/) config file.

By default the `.bootsy.toml` config file is attend to be stored in the `~/.config` directory.

If `~/.config` directory doesn't exist or you want to place the configuration somewhere else please use an environment variable named `BOOTSY` with config file location as value.

```bash 
$ export BOOTSY="/etc/.bootsy.toml"
```

---

The configuration must follow the bellow pattern.

```toml
[python]
dirs = []
files = ["main.py", "requirements.txt"]

[terraform]
dirs = ["environment"]
files = ["main.tf", "variables.tf", "environment/dev.tfvars"]
```

1. `[env]` : The [table](https://toml.io/en/v1.0.0#table) represents the environment you would like to setup.
2. `dirs = []` : An [array](https://toml.io/en/v1.0.0#array) indicating directories to create (must be an array).
2. `files = []` : An [array](https://toml.io/en/v1.0.0#array) indicating files to create (must be an array).

Feel free to add an additional environment in your **Bootsy** configuration respecting the pattern above!


## Command Line Interface

### Environments

**Bootsy** is designed to provide positional arguments based on the **config file tables** representing environments you would like to setup.

```bash
$ bootsy <environment>

# Bootsy's help output
positional arguments:
  {python,terraform}    Pick an environment to setup.
```

### Custom path

By default **Bootsy** will setup the environment in the current working directory.

If you want to setup your environment in another directory, use the `-p` or `--path` option.

```bash
$ bootsy <environment> -p ~/projects/foo
```

### Git

Additionnaly you can setup an environment and then initialiaze a [Git](https://git-scm.com/) repository with the `-g` or `--git` option.

```bash
$ bootsy <environment> --git
```

---

For additionnal help please run the `bootsy` command with the `-h` or `--help` option.

## Install

In order to install **Bootsy** and run it from anywhere you can run the `install.sh` file to easily configure **Bootsy**.

```bash
$ bash install.sh
```

It will first create a symbolic link of the `bootsy` python file in `/usr/local/bin` and make it executable with `chmod +x`. 
Then the `.bootsy.toml` config file will also be linked into the `~/.config` directory.

