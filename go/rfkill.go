package main

import (
	"bufio"
	"log"
	"os"
	"path/filepath"
	"io/fs"
	)

func readFile(path string) (string, error) {
	if f, err := os.Open(path); err != nil {
		return "", err
	} else {
		defer f.Close()
		b := bufio.NewReader(f)
		bytes, _, err := b.ReadLine()
		if err != nil {
			return "", err
		}
		return string(bytes), nil
	}
}

func rfkill() {
	rfkillpath := "/sys/class/rfkill"
	if err := filepath.Walk(rfkillpath, func(path string, info fs.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if rfkillpath == path {
			return nil
		}
		log.Printf("%s", path)
		for _,filename := range []string{"name", "hard", "soft"} {
			if name, err := readFile(filepath.Join(path, filename)); err != nil {
				return err
			} else {
				log.Printf("%s %s=%s\n", path, filename, name)
			}
		}
		return nil
	}); err != nil {
		panic(err)
	}
}

