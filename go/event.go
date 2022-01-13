package main

import (
	//"io/fs"
	"log"
	//"strings"
	"path/filepath"
	"syscall"
)

func event() {
	eventpath := "/dev/input"
	/*
	if err := filepath.Walk(eventpath, func(path string, info fs.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if eventpath == path {
			return nil
		}
		// TODO prevent descent
		if _,n := filepath.Split(path); strings.HasPrefix(n, "event") {
		}
		return nil
	}); err != nil {
		//panic(err)
	}
	*/
	if events, err := filepath.Glob(eventpath+"/event*"); err != nil {
		panic(err)
	} else {
		for _,path := range events {
			if fd, err := syscall.Open(path, syscall.O_RDONLY, 0); err != nil {
				panic(err)
			} else {
				if rawname, err := IoctlEVDEVGetRawName(fd); err == nil {
					log.Printf("%s: %s", path, rawname)
				} else {
					panic(err)
				}
			}
		}
	}
}
