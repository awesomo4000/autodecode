#! /usr/bin/env python
"""
<alrhodes@gmail.com>
"""
import binascii, copy, gzip, pprint, urlparse, sys, zlib
from   IPython import embed
from   StringIO import StringIO

#--- decoders
def unquote(s)     : return urlparse.unquote(s)
def b64_decode(s)  : return s.decode("base64")
def gunzip(s)      : return gzip.GzipFile(fileobj=StringIO(s)).read()
def unhexlify(s)   : return binascii.unhexlify(s)
def de_zlib(s)     : return zlib.decompress(s)
#def deserialize_java(s): return javaobj.loads(s)

decoders = [ unquote, b64_decode, gunzip, unhexlify, de_zlib ]

#--- log

DEBUG = False
#DEBUG = True
def debug(msg):
    if DEBUG:
        sys.stdout.write("[*] %s\n" % msg)
        sys.stdout.flush()
    return

#--- algorithm

def try_apply(f, x, o=None):
    y = None
    try:
        y = f(x) 
    except:
        return ( f, x, None )
    if y == x:
        return ( f, x, None )
    else:
        return ( f, x, y )

def build_graph(funs, s):
    graph = {}
    new   = []
    for f in funs: 
        f,x,y = try_apply(f,s)
        if y is not None:
            graph.setdefault(x,[]).append((f,y))
            new.append(y)
    debug("00 x=%s,new=%s" % (repr(x),repr(new)))
    pp = pprint.PrettyPrinter(indent=1)
    debug("###################")
    if DEBUG: pp.pprint(graph)
    debug("===================")
    debug("new=%s"%repr(new))
    debug("#####################")
    while new:
        debug("--------LOOP2-------------")
        debug("prepop:x=%s,new=%s"%(repr(x),repr(new)))
        x = new.pop(0)
        debug("postpop:x=%s,new=%s"% (repr(x),repr(new)))
        for f in funs:
            f,x,y = try_apply(f,x)
            if y is not None:
                graph.setdefault(x,[]).append((f,y))
                debug("f=%s,y=%s"% (f,repr(y)))
                new.append(y)
                debug("new2=%s" % repr(new))
            #graph.setdefault(x,[]).append((f,y))
    debug("-------_END_----------")
    return graph

def find_path(graph,start):
    debug("****************************")
    debug("find_all_paths")
    debug("****************************")
    path, q = [start], [start]
    debug("-=-=  path=%s,q=%s" % (path,q))
    while q:
        debug("00 @@@ while q=%s"%repr(q))
        v = q.pop(0)
        debug("")
        debug("-->v=%s" % repr(v))
        debug("-->q=%s" % repr(q))
        debug("")
        if not graph.has_key(v):
            path.append(v)
            continue
        for f,x in graph[v]:
            debug("====>fx=%s"%repr((f,x)))
            if not (f,x) in path:
                path.append((f,x))
                q.append(x)
    return path

def display(e,verbose=0):
    try:
        return '%s(%s)=%s' % (e[0].func_name,
                         repr(e[1])[:24],
                         repr(e[2])[:24] )
    except:
        return repr(node)

if __name__ == "__main__":
    data    = sys.stdin.read()
    graph   = build_graph (decoders, data  )
    pp = pprint.PrettyPrinter(indent=1)
    #DEBUG = 1
    if DEBUG: pp.pprint(graph)
    debug("====================================")
    path = find_path(graph,data)[1:]
    print("%s" % repr(data))
    for entry in path:
        if len(entry) == 2:
            f,y = entry
            print
            try:
                print '->',f.func_name,'=\n',repr(y)
            except:
                print '->',repr(f),repr(y)
        else:
            print repr(entry)
    sys.exit(0)

