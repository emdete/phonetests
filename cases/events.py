#!/usr/bin/env python3
__copyright__ = 'Copyright (c) 2021 fgau'
__license__ = 'GPLv2'


import struct
import sys

from logging import getLogger
logger = getLogger(__name__)

class Case(object):
    def __init__(self, std):
        pass

    def start(self):
        yield 'Plug & unplug the headphone'
        toggles = 0
        infile_path = '/dev/input/event14'
        '''
        FORMAT represents the format used by linux kernel input event struct
        See https://github.com/torvalds/linux/blob/v5.5-rc5/include/uapi/linux/input.h#L28
        Stands for: long int, long int, unsigned short, unsigned short, unsigned int
        '''
        FORMAT = 'llHHI'
        EVENT_SIZE = struct.calcsize(FORMAT)
        with open(infile_path, 'rb') as in_file:
            event = in_file.read(EVENT_SIZE)
            while event:
                (tv_sec, tv_usec, type_, code, value) = struct.unpack(FORMAT, event)
                if type_ != 0 or code != 0 or value != 0:
                    toggles += 1
                    yield 'Event type {}, code {}, value {} at {}.{}'.format(
                        type_, code, value, tv_sec, tv_usec)
                else:
                    # Events with code, type and value == 0 are 'separator' events
                    pass
                if toggles >= 2:
                    return
                event = in_file.read(EVENT_SIZE)

