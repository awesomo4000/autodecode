#! /usr/bin/env python
"""Usage: %s <input_string> <iters>
"""
import sys
import binascii, gzip, os, zlib, urllib2, random, StringIO, sys
def usage():
    sys.stdout.write(__doc__ % os.path.basename(sys.argv[0]))

def b2a(s):
    return binascii.hexlify(s)

def zlc(s):
    return zlib.compress(s)

def gz(s):
    stringio = StringIO.StringIO()
    gzip_file = gzip.GzipFile(fileobj=stringio, mode='w')
    gzip_file.write(s)
    gzip_file.close()
    return stringio.getvalue()

def b64e(s):
    return s.encode('base64')

def urlq(s):
    return urllib2.quote(s)

def main(s, iters):
    encoders = [ b2a, zlc, gz, b64e, urlq ]
    for i in xrange(0, iters):
        e = random.choice(encoders)
        s = e(s)
        sys.stderr.write("i %d enc %s len %d\n" %(i,
                                           e.func_name,len(s)))
    sys.stdout.write("%s" % s)

if __name__ == "__main__":

    try:
        s     = sys.argv[1]
        iters = int(sys.argv[2])
    except:
        usage()
        sys.exit(1)

    main(s,iters)

