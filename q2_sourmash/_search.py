# ----------------------------------------------------------------------------
# Copyright (c) 2016-2018, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import qiime2.plugin.model as model
from q2_types.distance_matrix import DistanceMatrix
from q2_sourmash._format import (
    MinHashSigDirFmt, 
    SBTDirFmt,
    OutputTextDirFmt
)
import os
import subprocess
import numpy
import skbio
from typing import Union

def search(
        query_signature:MinHashSigDirFmt, 
        db_signature: Union[MinHashSigDirFmt,SBTDirFmt], 
        ksize: int, 
        threshold: float, 
        scale: int, 
        containment: bool=False) -> OutputTextDirFmt:
    
    outdir = OutputTextDirFmt()
    command = [
            'sourmash', 'search', 
            str(query_signature), 
            str(db_signature) + '/*', 
            '--ksize', str(ksize),
            '--output', str(output) + '/output.txt',
            '--threshold', str(threshold),
            '--scale', str(scale)]
    if containment:
        command.append('--containment')
    p = subprocess.run(' '.join(command), check=True, shell=True)
    return outdir
