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
import numpy
import skbio

def compare(min_hash_signature:MinHashSigJsonDirFormat, ksize: int, ignore_abundance: bool=True) -> skbio.DistanceMatrix:

    np_file = 'tmp'
    label_file = 'tmp.labels.txt'
    command = ['sourmash', 'compare', str(min_hash_signature) + "/*", '--ksize', str(ksize), '-o', 'tmp']
    if ignore_abundance:
        command.append('--ignore-abundance')
    subprocess.run(' '.join(command), check=True, shell=True)
    # load np_file as np.ndarray -> np_sim
    np_sim = numpy.load(np_file)
    # convert similarity to distance
    np_dis = 1 - np_sim
    # read labels into a list -> labels
    labels = [item.strip() for item in open(label_file)]
    os.remove(np_file)
    os.remove(label_file)
    return skbio.DistanceMatrix(np_dis, labels)
