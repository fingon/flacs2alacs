#
# Author: Markus Stenberg <fingon@iki.fi>
#
# Copyright (c) 2018 Markus Stenberg
#
# Created:       Fri Nov  9 11:30:36 2018 mstenber
# Last modified: Fri Nov  9 11:41:37 2018 mstenber
# Edit time:     1 min
#
#

# Example of how _I_ use this
all:
	python3 flacs2alacs.py ~/Music/{flac,alac}
	find ~/Music/flac/ -name '*-resized-*.jpg' -print0 | xargs -0 rm
	find ~/Music/flac/ -name '*-resized-*.jpeg' -print0 | xargs -0 rm
