#!/bin/bash
if [ -d $HOME/.config/ ]; then
	ln -s $PWD/.bootsy.toml $HOME/.config/.bootsy.toml

	sudo ln -s $PWD/bootsy /usr/local/bin
	sudo chmod +x /usr/local/bin/bootsy

	echo "[BOOTSY] [INFO] Successfully installed."
else
	error="[BOOTSY] [ERROR] ~/.config directory not found.\
	Consider create it or using BOOTSY environment variable\
	instead as explain on the README."

	echo $error
fi


