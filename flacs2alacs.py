#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-
#
# Author: Markus Stenberg <fingon@iki.fi>
#
# Copyright (c) 2018 Markus Stenberg
#
# Created:       Fri Nov  9 10:07:49 2018 mstenber
# Last modified: Wed Jun 23 21:35:29 2021 mstenber
# Edit time:     38 min
#

import os
import os.path
import subprocess
import tempfile


def get_flacs_and_covers(path):
    for dirpath, dirnames, filenames in os.walk(srcdir):
        filenames_and_suffixes = [(fn, fn.split('.')[-1].lower())
                                  for fn in filenames]
        # print(dirpath, filenames_and_suffixes)
        flacs = [x for x in filenames_and_suffixes if x[1] == 'flac']
        if not flacs:
            continue
        jpgs = [x for x in filenames_and_suffixes
                if x[1] in ['jpg', 'jpeg'] and '-resized-' not in x[0]]
        # atomicparsley seems to stick -resized- files all over the place, sigh
        if not jpgs:
            print('!!! no .jpg in %s' % dirpath)
            continue
        for flac in flacs:
            assert dirpath[:len(path)] == path
            relpath = dirpath[len(path)+1:]
            yield relpath, flac[0], jpgs[0][0]


def convert_flac_to_alac(srcdir, dstdir, t):
    dirname, flacname, jpegname = t
    alacname = flacname[:-4] + 'm4a'
    srcpath = os.path.join(srcdir, dirname, flacname)
    jpgpath = os.path.join(srcdir, dirname, jpegname)
    dstpath = os.path.join(dstdir, dirname, alacname)
    with tempfile.TemporaryDirectory(dir=dstdir) as tempdir:
        tmppath = os.path.join(tempdir, alacname)
        st0 = os.stat(srcpath)
        try:
            st = os.stat(dstpath)
            uptodate = st0.st_mtime <= st.st_mtime
        except FileNotFoundError:
            uptodate = False
        if uptodate:
            return
        os.makedirs(os.path.dirname(dstpath), exist_ok=True)
        try:
            os.unlink(tmppath)
        except FileNotFoundError:
            pass
        subprocess.run(['ffmpeg', '-i', srcpath,
                        '-vn',  # do not make video even if it has art :p
                        '-acodec', 'alac',
                        tmppath], check=True)
        subprocess.run(['AtomicParsley', tmppath,
                        '--artwork', jpgpath,
                        '--overWrite'], check=True)
        # print(tmppath, dstpath)
        os.rename(tmppath, dstpath)


if __name__ == '__main__':
    import functools
    import multiprocessing
    import sys
    srcdir, dstdir = sys.argv[1:]  # two mandatory arguments
    l = get_flacs_and_covers(srcdir)
    l = list(l)
    # print(l)
    # convert_flac_to_alac(srcdir, dstdir, l[0])
    # l = [l[0]]
    print('%d files' % len(l))
    with multiprocessing.Pool() as p:
        fun = functools.partial(convert_flac_to_alac, srcdir, dstdir)
        for e in p.map(fun, l):
            # sys.stdout.write('.')
            # .. if we don't capture output, both ffmpeg+AtomicParsley spam screen 'enough' ..

            pass
    # print()
