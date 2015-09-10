#! /usr/bin/env python

import sys
import binascii, zlib, urllib2, random

def b2a(s):
  return binascii.hexlify(s)

def gz(s):
  return zlib.compress(s)

def b64e(s):
  return s.encode('base64')

def urlq(s):
  return urllib2.quote(s)

encoders = [ b2a, gz, b64e, urlq ]
iters = 20

s = "tickle my HAIRY sack like its christmas time"

for i in xrange(0, iters):
  e = random.choice(encoders)
  s = e(s)
  sys.stderr.write("i %d len %d\n" %(i, len(s)))

print b64e(gz(s))
