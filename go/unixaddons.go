package main

import (
	"syscall"
	"unsafe"

	"golang.org/x/sys/unix"
)

var _IOC_NRBITS uint = 8
var _IOC_TYPEBITS uint = 8
var _IOC_SIZEBITS uint = 14
var _IOC_NRSHIFT uint = 0
var _IOC_TYPESHIFT uint = (_IOC_NRSHIFT+_IOC_NRBITS)
var _IOC_SIZESHIFT uint = (_IOC_TYPESHIFT+_IOC_TYPEBITS)
var _IOC_DIRSHIFT uint = (_IOC_SIZESHIFT+_IOC_SIZEBITS)
var _IOC_READ uint = 2

func _IOC(dir uint, type_ rune, nr uint, size uint) uint {
	ret := (((dir) << _IOC_DIRSHIFT) |
		((uint(type_)) << _IOC_TYPESHIFT) |
		((nr) << _IOC_NRSHIFT) |
		((size) << _IOC_SIZESHIFT))
	return ret
}

func errnoErr(e syscall.Errno) error {
	return syscall.Errno(e)
}

func ioctlPtr(fd int, req uint, arg unsafe.Pointer) (err error) {
	_, _, e1 := unix.Syscall(unix.SYS_IOCTL, uintptr(fd), uintptr(req), uintptr(arg))
	if e1 != 0 {
		err = errnoErr(e1)
	}
	return
}

func EVIOCGNAME(length uint) uint {
	return _IOC(_IOC_READ, 'E', 0x06, length)
}

func IoctlEVDEVGetRawName(fd int) (string, error) {
	var value [256]byte
	err := ioctlPtr(fd, EVIOCGNAME(256), unsafe.Pointer(&value[0]))
	return unix.ByteSliceToString(value[:]), err
}

