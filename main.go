package main

import (
	"fmt"
	"os"
	"os/exec"
)

// Terraform, Python, Html, Adoc

func createFiles(files []string) {
	for _, file := range files {
		os.Create(file)
	}
}

func createDirectories(dirs []string) {
	for _, dir := range dirs {
		os.Mkdir(dir, 0777)
	}
}

func git() {
	files := []string{".gitignore", "README.md"}

	init := exec.Command("git", "init")

	_, err := init.Output()

	if err != nil {
		fmt.Println(err.Error())
		return
	}

	createFiles(files)
}

func terraform() {

	files := []string{
		"main.tf",
		"outputs.tf",
		"providers.tf",
		"variables.tf",
		"versions.tf",
	}

	createFiles(files)
}

func python() {
	files := []string{
		"main.py",
		"requirements.txt",
	}
	createFiles(files)
}

func html() {
	dirs := []string{
		"static",
		"static/css",
		"static/js",
		"assets",
		"assets/images",
	}
	files := []string{
		"static/css/main.css",
		"static/js/main.js",
		"index.html",
	}

	createDirectories(dirs)
	createFiles(files)
}

func main() {
	fmt.Println("Hello World!")

	dir := "foo"

	os.Mkdir(dir, 0777)
	os.Chdir(dir)

	//terraform()
	//python()
	html()
	git()
}
