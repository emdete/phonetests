package main

import (
	"log"
	"strings"
	"io/fs"
	"path/filepath"
	)

// func readFile(path string) (string, error) { from rfkill.go

func thermal() {
	thermalpath := "/sys/devices/virtual/thermal"
	if err := filepath.Walk(thermalpath, func(path string, info fs.FileInfo, err error) error {
		if thermalpath == path {
			return nil
		}
		if err != nil {
			return err
		}
		if _,n := filepath.Split(path); strings.HasPrefix(n, "thermal_zone") {
			for _,filename := range []string{"type", "temp"} {
				value := "undefined"
				if val, err := readFile(filepath.Join(path, filename)); err != nil {
					//return err
				} else {
					value = val
				}
					log.Printf("%s %s=%s\n", path, filename, value)
			}
		}
		return nil
	}); err != nil {
		panic(err)
	}
}
