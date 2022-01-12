#!/usr/bin/env python
from logging import getLogger, StreamHandler
log = getLogger('__name__')
from os import environ
from os import system
from os import scandir
from importlib import import_module
from time import sleep

while False:
	with open('/dev/gnss0') as file_:
		while True:
			line = file_.readline()
			if line:
				print('gnss0', line.strip())
			else:
				print('sleep')
				sleep(1)

cases = dict()
for case in scandir('cases/'):
	if case.name[0] not in ('.', '_', ):
		cases[case.name[:-3]] = import_module(f'cases.{case.name[:-3]}').Case(None)

for k in cases:
	log.error('%s:', k)
	for m in cases[k].start():
		log.error('%s: %s', k, m)
