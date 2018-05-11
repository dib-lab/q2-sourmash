# ----------------------------------------------------------------------------
# Copyright (c) 2016-2018, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from q2_types.distance_matrix import DistanceMatrix
from q2_sourmash._format import MinHashSigJsonDirFormat
import os
import subprocess

def compare(min_hash_signature:MinHashSigJsonDirFormat, ksize: int, ignore_abundance: bool=True) -> DistanceMatrix:

    output = DistanceMatrix
    command = ['sourmash', 'compare', str(min_hash_signature) + "/*", '--ksize', str(ksize),
    '-o', 'tmp']

    if ignore_abundance:
        command.append('--ignore-abundance')

    subprocess.run(' '.join(command), check=True, shell=True)

    return output
