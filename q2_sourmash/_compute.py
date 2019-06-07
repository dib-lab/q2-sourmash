# ----------------------------------------------------------------------------
# Copyright (c) 2016-2018, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from q2_types.per_sample_sequences import SingleLanePerSampleSingleEndFastqDirFmt, FastqGzFormat
import qiime2.util
from q2_sourmash._format import MinHashSigDirFmt
import os
import subprocess
import glob

def compute(sequence_file:SingleLanePerSampleSingleEndFastqDirFmt, ksizes: int, scaled: int, track_abundance: bool=True) -> MinHashSigDirFmt:

    output = MinHashSigDirFmt()
    for seq_file in glob.glob(os.path.join(str(sequence_file), '*fastq.gz')):
        filepath = str(seq_file)
        filename = os.path.basename(filepath)
        qiime2.util.duplicate(filepath, os.path.join(str(output), filename))

    command = ['sourmash', 'compute', str(output) + "/*", '--ksizes', str(ksizes), '--scaled', str(scaled)]

    if track_abundance:
        command.append('--track-abundance')

    subprocess.run(' '.join(command), check=True, shell=True, cwd=str(output))

    for seq_file in glob.glob(os.path.join(str(output), '*fastq.gz')):
        os.remove(seq_file)

    return output
