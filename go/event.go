package main

import (
	"io/fs"
	"log"
	"path/filepath"
	"syscall"
)

func event() {
	eventpath := "/dev/input"
	if err := filepath.Walk(eventpath, func(path string, info fs.FileInfo, err error) error {
		if eventpath == path {
			return nil
		}
		log.Printf("%s", path)
		if fd, err := syscall.Open(path, syscall.O_RDONLY, 0); err != nil {
			return err
		} else {
			if rawname, err := IoctlEVDEVGetRawName(fd); err == nil {
				log.Printf("%s: %s", path, rawname)
			}
		}
		return nil
	}); err != nil {
		//panic(err)
	}
}
