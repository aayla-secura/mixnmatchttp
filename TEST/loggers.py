import logging
import sys

mm = logging.getLogger('mixnmatchttp')
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(1)
mm.setLevel(1)
mm.addHandler(handler)

test = logging.getLogger('TEST')
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(1)
test.setLevel(1)
test.addHandler(handler)
