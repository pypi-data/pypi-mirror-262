# -*- coding: utf-8 -*-
import maplpy
import sys


def mindopt_apl():
    maplpy.MaplModel.start_cmd(len(sys.argv), sys.argv)

