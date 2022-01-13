package main

import (
	"log"
	"math"
	"strings"
	"strconv"
	"io/fs"
	"path/filepath"
	)

// func readFile(path string) (string, error) { from rfkill.go

func thermal() {
	temp := 0.0
	type_ := ""
	type2 := ""
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
					return err
				} else {
					value = val
				}
				if filename == "temp" {
					if tf, err := strconv.ParseInt(value, 10, 64); err == nil {
						temp2 := math.Max(temp, float64(tf) / 1000.0)
						if temp2 != temp {
							temp = temp2
							type_ = type2
						}
					}
				} else {
					type2 = value
				}
				log.Printf("%s %s=%s\n", path, filename, value)
			}
		}
		return nil
	}); err != nil {
		panic(err)
	}
	log.Printf("temp max=%f from %s", temp, type_)
}
