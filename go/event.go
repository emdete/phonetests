package main

import (
	"log"
	"strings"
	"path/filepath"
	"syscall"
)

func event() {
	eventpath := "/dev/input"
	if events, err := filepath.Glob(eventpath+"/event*"); err != nil {
		panic(err)
	} else {
		for _,path := range events {
			// flow in C code:
			// openat(AT_FDCWD, "/dev/input/event14", O_RDONLY) = 3
			// ioctl(3, EVIOCGVERSION, [0x10001]) = 0
			// ioctl(3, EVIOCGID, {bustype=0, vendor=0, product=0, version=0}) = 0
			// ioctl(3, EVIOCGNAME(256), "HDA Intel PCH Headphone Mic\0") = 28
			// ioctl(3, EVIOCGBIT(0, 31), [EV_SYN, EV_SW]) = 8
			// ioctl(3, EVIOCGSW(6144), [ 0 ]) = 8
			// ioctl(3, EVIOCGBIT(EV_SW, 767), [SW_HEADPHONE_INSERT]) = 8
			// ioctl(3, EVIOCGPROP(248), [ 0 ]) = 8
			// ioctl(3, EVIOCGRAB, 1) = 0
			// ioctl(3, EVIOCGRAB, 0) = 0
			// pselect6(4, [3], NULL, NULL, NULL, NULL) = 1 (in [3])
			// read(3, "B\"\340a\0\0\0\0\304\30\16\0\0\0\0\0\5\0\2\0\1\0\0\0B\"\340a\0\0\0\0"..., 1536) = 48
			// read(3, "o\"\340a\0\0\0\0005\365\f\0\0\0\0\0\5\0\2\0\0\0\0\0o\"\340a\0\0\0\0"..., 1536) = 48
			if fd, err := syscall.Open(path, syscall.O_RDONLY, 0); err != nil {
				panic(err)
			} else {
				if rawname, err := IoctlEVDEVGetRawName(fd); err != nil {
					panic(err)
				} else {
					log.Printf("%s: %s", path, rawname)
					if strings.Contains(rawname, "Headphone") {
						var r syscall.FdSet
						r.Bits[fd/64] = 1 << (fd%64)
						if _, err := syscall.Select(fd+1, &r, nil, nil, nil); err == nil {
							buffer := make([]byte, 24 * 3)
							if size, err := syscall.Read(fd, buffer); err != nil {
								panic(err)
							} else {
								log.Printf("%s: %d %v", path, size, buffer)
							}
						}
					}
				}
			}
		}
	}
}
