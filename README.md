# flacs2alacs #

This utility script maintains flac tree hierarchy -> alac tree hierarchy,
with entirely automatic (and hopefully correct) conversion steps in the
middle.

This can be used constantly as it checks timestamps, and does nothing if
FLAC has not chanced since ALAC was created. (I prefer having single source
of truth for metadata, and in this case, it is my FLAC hierarchy. Storage
is cheap, join the dark side. )

Requirements:

- python 3
- ffmpeg
- atomicparsley (to handle cover art)

There MUST be .jpg file in each subdirectory with .flacs. All files are
handled 'safely' (first write to temp file, and then rename).

Usage:

```

python3 flacs2alacs.py srcdir dstdir

```

Example:

```
python3 flacs2alacs.py ~/Music/{flac,alac}


```

## TODO

- eventually make removal part of the equation too ( now if I rename
  .flacs, .m4as stick around and cause duplication ); unfortunately syncing
  state with iTunes is painful so I think I will simply not rename
  anything, ever, as I do not really care about the file hierarchy that
  much anyway, just the metadata + covers..

- real command-line option parsing
