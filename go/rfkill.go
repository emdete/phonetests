package main

import (
	"bufio"
	"encoding/binary"
	"syscall"
	"log"
	"os"
	"path/filepath"
	"io/fs"
	)


var rfkill_type = map[byte]string {
	0: "RFKILL_TYPE_ALL",
	1: "RFKILL_TYPE_WLAN",
	2: "RFKILL_TYPE_BLUETOOTH",
	3: "RFKILL_TYPE_UWB",
	4: "RFKILL_TYPE_WIMAX",
	5: "RFKILL_TYPE_WWAN",
	6: "RFKILL_TYPE_GPS",
	7: "RFKILL_TYPE_FM",
	8: "RFKILL_TYPE_NFC",
}

var rfkill_operation = map[byte]string {
	0: "RFKILL_OP_ADD",
	1: "RFKILL_OP_DEL",
	2: "RFKILL_OP_CHANGE",
	3: "RFKILL_OP_CHANGE_ALL",
}

var rfkill_hard_block_reasons = map[byte]string {
	1 << 0: "RFKILL_HARD_BLOCK_SIGNAL",
	1 << 1: "RFKILL_HARD_BLOCK_NOT_OWNER",
}

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

func readEvents() {
	path := "/dev/rfkill"
	if fd, err := syscall.Open(path, syscall.O_RDONLY, 0); err != nil {
		panic(err)
	} else {
		for {
			buffer := make([]byte, 8)
			if size, err := syscall.Read(fd, buffer); err != nil || size != 8 {
				panic(err)
			} else {
				// from /usr/include/linux/rfkill.h struct rfkill_event
				idx := binary.LittleEndian.Uint32(buffer[0:4]) // __u32
				type_ := buffer[4] // __u8
				op := buffer[5] // __u8
				soft := buffer[6] // __u8
				hard := buffer[7] // __u8
				log.Printf("idx=%d, type_=%s, op=%s, soft=%d, hard=%d\n",
					idx, rfkill_type[type_], rfkill_operation[op], soft, hard)
			}
			break // TODO
		}
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
	readEvents()
}

