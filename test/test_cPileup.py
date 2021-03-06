#!/usr/bin/env python
# Time-stamp: <2012-03-09 23:19:55 Tao Liu>

"""Module Description: Test functions for pileup functions.

Copyright (c) 2011 Tao Liu <taoliu@jimmy.harvard.edu>

This code is free software; you can redistribute it and/or modify it
under the terms of the BSD License (see the file COPYING included with
the distribution).

@status:  experimental
@version: $Revision$
@author:  Tao Liu
@contact: taoliu@jimmy.harvard.edu
"""


import os
import sys
import unittest

from math import log10
from MACS2.cPileup import *
from MACS2.IO.cFixWidthTrack import FWTrackII

# ------------------------------------
# Main function
# ------------------------------------

class Test_pileup(unittest.TestCase):
    """Unittest for pileup_bdg() in cPileup.pyx.

    """
    def setUp(self):
        self.chrom = "chr1"
        self.plus_pos = ( 0, 1, 3, 4, 5 )
        self.minus_pos = ( 5, 6, 8, 9, 10 )
        self.d = 5
        self.expect = [ ( 0, 1, 2.0 ),
                        ( 1, 3, 4.0 ),
                        ( 3, 4, 6.0 ),
                        ( 4, 6, 8.0 ),
                        ( 6, 8, 6.0 ),
                        ( 8, 9, 4.0 ),                            
                        ( 9, 10, 2.0 )
                        ]

    def test_pileup(self):
        # build FWTrackII
        self.fwtrack2 = FWTrackII()
        for i in self.plus_pos:
            self.fwtrack2.add_loc(self.chrom, i, 0)
        for i in self.minus_pos:
            self.fwtrack2.add_loc(self.chrom, i, 1)            

        self.pileup = pileup_bdg(self.fwtrack2, self.d, halfextension=False)
        self.result = []
        chrs = self.pileup.get_chr_names()
        for chrom in chrs:
            (p,v) = self.pileup.get_data_by_chr(chrom)
            pnext = iter(p).next
            vnext = iter(v).next
            pre = 0
            for i in xrange(len(p)):
                pos = pnext()
                value = vnext()
                self.result.append( (pre,pos,value) )
                pre = pos
        # check result
        self.assertEqual(self.result, self.expect)

if __name__ == '__main__':
    unittest.main()
