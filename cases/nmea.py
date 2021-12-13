#!/usr/bin/env python3
__copyright__ = "Copyright (c) 2008-2021 M. Dietrich <mdt@emdete.de>"
__license__ = "GPLv2"

from math import modf
from datetime import datetime

from logging import getLogger
logger = getLogger(__name__)

class Case(object):
	def __init__(self, stdscr):
		logger.debug('__init__')
		self.stdscr = stdscr
		self.dialect = []
		self.time = None
		self.position = dict()
		self.satellites = dict()
		#self.stream = open('/dev/gnss0', 'r+b', buffering=0)
		#self.stream.flush()
		#self.sendPSTMGPSRESET()
		#self.sendPSTMINITTIME()
		#self.sendPSTMDUMPEPHEMS()
		#self.sendPSTMDUMPALMANAC()

	def start(self):
		while True:
			try:
				line = self.stream.readline()
				line = line.decode('ascii')
				logger.debug('received: %s', line)
				if line:
					self.parse(line)
			except Exception as e:
				logger.warning('error: %s', e)

	def send(self, cmd):
		self.stream.write(cmd.encode('ascii'))
		self.stream.flush()

	def parse(self, line):
		line, checksum = line.strip().split('*')
		if line[0] != '$':
			logger.info('Not NMEA: "%s"', repr(line))
			return
		line = line[1:]
		logger.debug('parse: %s', line, )
		self.chk_checksum(line, checksum)
		line = line.split(',')
		word = line.pop(0)
		if not word in self.dialect:
			self.dialect.append(word)
		getattr(self, 'parse' + word, self.no_such_sentence)(word, *line)

	# Utils
	def add_checksum(self, sentence):
		csum = 0
		for c in sentence:
			csum = csum ^ ord(c)
		return '$%s*%02X\r\n'% (sentence, csum, )

	def chk_checksum(self, sentence, cksum):
		csum = 0
		for c in sentence:
			csum = csum ^ ord(c)
		csum = '%02X'% csum
		if csum != cksum:
			logger.warning('Bad checksum: "%s*%s" %s', sentence, cksum, csum, )

	def get_speed(self, speed):
		return speed * 1.852 if speed else speed

	def do_lat_lon(self, l, h):
		if not l:
			return None
		if l[-1] in ('N', 'S', 'E', 'W', ):
			h = l[-1]
			l = l[:-1]
		l = float(l)
		frac, intpart = modf(l / 100.0)
		l = intpart + frac * 100.0 / 60.0
		if h in ('S', 'W', ):
			l = -l
		return l

	# Sending
	def sendPSTMGPSRESET(self):
		# $PSTMGPSRESET,*27
		# STMGPSRESET
		self.send(self.add_checksum('PSTMGPSRESET,'))

	def sendPSTMINITTIME(self):
		# $PSTMINITTIME,30,11,2021,08,56,06*1A
		# STMINITTIME STMINITTIMEOK
		now = datetime.utcnow()
		self.send(self.add_checksum(','.join(('PSTMINITTIME',
			now.strftime('%d'), now.strftime('%m'), now.strftime('%Y'),
			now.strftime('%H'), now.strftime('%M'), now.strftime('%S'),
			))))

	def sendPSTMDUMPEPHEMS(self):
		#
		# STMDUMPEPHEMS STMEPHEM STMEPHEMOK
		return

	def sendPSTMDUMPALMANAC(self):
		#
		# STMDUMPALMANAC STMALMANAC STMALMANACOK
		return

	# Parsing
	def parseGPGGA(self, word, time, latitude, ln, longitude, lw, fix, satellites, dilution, altitude, *words):
		position = dict(self.position)
		if latitude and ln:
			position['latitude'] = self.do_lat_lon(latitude, ln)
		if longitude and lw:
			position['longitude'] = self.do_lat_lon(longitude, lw)
		if altitude:
			position['altitude'] = int(float(altitude))
		if satellites:
			position['satellites'] = int(satellites)
		position['fix'] = int(fix) >= 1
		if position['fix'] and self.position != position:
			self.position = position
			self.Position(self.position)

	def parseGPRMC(self, word, gpstime, warning, latitude, ln, longitude, lw, knots, course, gpsdate, magneticvariation, me, mw):
		if warning in ('A', 'V', ):
			position = dict(self.position)
			if gpsdate and gpstime:
				self.time = datetime(
					2000 + int(gpsdate[4:6]),
					int(gpsdate[2:4]),
					int(gpsdate[0:2]),
					int(gpstime[0:2]),
					int(gpstime[2:4]),
					int(gpstime[4:6]),
					)
			if latitude and ln:
				position['latitude'] = self.do_lat_lon(latitude, ln)
			if longitude and lw:
				position['longitude'] = self.do_lat_lon(longitude, lw)
			if knots:
				knots = float(knots)
				speed = self.get_speed(knots)
				position['speed'] = int(speed)
				if speed > 3 and course:
					position['course'] = int(float(course))
				else:
					position['course'] = None
			else:
				position['course'] = None
				position['speed'] = None
			position['fix'] = warning == 'A'
			if position['fix'] and self.position != position:
				self.position = position
				self.Position(self.position)
			self.Time(self.time)
		else:
			logger.warning('not A or V')

	def parseGPGLL(self, word, latitude, ln, longitude, lw, time, valid, mode):
		if valid in ('A', 'V', ):
			position = dict(self.position)
			if latitude and ln:
				position['latitude'] = self.do_lat_lon(latitude, ln)
			if longitude and lw:
				position['longitude'] = self.do_lat_lon(longitude, lw)
			position['fix'] = valid == 'A'
			if position['fix'] and self.position != position:
				self.position = position
				self.Position(self.position)
		else:
			logger.warning('not A or V')

	def parseGPGSA(self, word, selection, mode, s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, pdop, hdop, vdop):
		position = dict(self.position)
		if int(mode) > 1:
			position['fix'] = True
			if hdop < 4:
				self.position['radius'] = 10
			elif hdop < 6:
				self.position['radius'] = 50
			elif hdop < 8:
				self.position['radius'] = 500
			else:
				self.position['radius'] = 5000
		else:
			position['fix'] = False
			if 'radius' in self.position:
				del self.position['radius']
		if self.position != position:
			self.position = position
			self.Position(self.position)
		else:
			logger.warning('not A or V')

	def parseGPVTG(self, word, cog, cogu, cogm, cogmu, knots, sogu, speed, kphu, mode):
		position = dict(self.position)
		if mode in ('A', 'V', ):
			if speed:
				speed = float(speed)
				position['speed'] = int(speed)
				if speed > 3 and cog:
					position['course'] = int(float(cog))
				else:
					position['course'] = None
			else:
				position['course'] = None
				position['speed'] = None
			position['fix'] = valid == 'A'
			if self.position != position:
				self.position = position
				self.Position(self.position)

	def parseG_GSV(self, source, word, numbersentences, sentence, in_view, *words):
		sentence = int(sentence)
		numbersentences = int(numbersentences)
		in_view = int(in_view)
		words = list(words)
		if sentence == 1:
			self.satellites[source] = dict(
				in_view=in_view,
				)
		while words:
			prn = words.pop(0)
			elevation = words.pop(0)
			azimuth = words.pop(0)
			ss = words.pop(0)
			if prn:
				self.satellites[source][prn] = dict()
				if azimuth:
					self.satellites[source][prn]['azimuth'] = int(azimuth)
				if elevation:
					self.satellites[source][prn]['elevation'] = int(elevation)
				if ss:
					self.satellites[source][prn]['ss'] = int(ss)
		if sentence == numbersentences:
			self.Satellites(self.satellites)

	def parseGPGSV(self, *words):
		self.parseG_GSV('P', *words)

	def parseGLGSV(self, *words):
		self.parseG_GSV('L', *words)

	def parseGPTXT(self, word, *words):
		logger.info('unused: %s %s', word, words)

	def parseGPZDA(self, word, time, day, month, year, ltzh, ltzn):
		logger.info('unused: %s %s', word, time, day, month, year, ltzh, ltzn)

	def parsePGLOR(self, word, *words):
		logger.info('unused: %s %s', word, words)

	def parseGNGSA(self, word, mode1, mode2, prn, pdop, hdop, vdop, *words):
		logger.info(f'unused: word={word}, mode1={mode1}, mode2={mode2}, prn={prn}, pdop={pdop}, hdop={hdop}, vdop={vdop}, {words}')

	def parsePSTMCPU(self, word, *words):
		logger.info('unused: %s %s', word, words)

	def no_such_sentence(self, word, *words):
		logger.warning('Unknown sentence: %s %s', word, words)

	# Events
	def Time(self, p):
		logger.debug('Time: %s', p)

	def Satellites(self, p):
		logger.debug('Satellites: %s', p)
		for source, g in p.items():
			for i, s in g.items():
				if hasattr(s, 'values'):
					i = int(i)
					s = ', '.join([f'{k}={v}' for k,v in s.items() if v])

	def Position(self, p):
		logger.debug('Position: %s', p)
		p = ', '.join([f'{k}={v}' for k,v in p.items() if v])


def main():
	nmea = Nmea()
	nmea.start()

if __name__ == '__main__':
	main()
# vim:tw=0:nowrap
