package main

import (
	"syscall"
	"unsafe"

	"golang.org/x/sys/unix"
)

var _IOC_NRBITS = 8
var _IOC_TYPEBITS = 8
var _IOC_READ uint = 0
var _IOC_NRSHIFT = 0
var _IOC_TYPESHIFT = (_IOC_NRSHIFT+_IOC_NRBITS)
var _IOC_SIZESHIFT = (_IOC_TYPESHIFT+_IOC_TYPEBITS)
var _IOC_DIRSHIFT = (_IOC_SIZESHIFT+_IOC_SIZEBITS)
var _IOC_SIZEBITS = 14

func _IOC(dir uint, type_ rune, nr uint, size uint) uint {
	return (((dir) << _IOC_DIRSHIFT) |
		((uint(type_)) << _IOC_TYPESHIFT) |
		((nr) << _IOC_NRSHIFT) |
		((size) << _IOC_SIZESHIFT))
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

