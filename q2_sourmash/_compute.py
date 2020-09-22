# ----------------------------------------------------------------------------
# Copyright (c) 2016-2018, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from q2_types.per_sample_sequences import SingleLanePerSampleSingleEndFastqDirFmt, FastqGzFormat
from q2_types.feature_data import DNAIterator
import qiime2.util
import pandas as pd
from q2_sourmash._format import MinHashSigJsonDirFormat
import os
import subprocess
import glob
import sys
import tempfile
import shutil

def compute_fasta(sequence_file: DNAIterator,
                  ksizes: int,
                  scaled: int,
                  track_abundance: bool=True) -> MinHashSigJsonDirFormat:
    output = MinHashSigJsonDirFormat()

    # write files in tmp dir
    #with tempfile.TemporaryDirectory() as temp_dir:
    for seq in sequence_file:
        tmp_fp = os.path.join(str(output), str(seq.metadata['id']) + '.fasta')
        with open(tmp_fp, 'w') as indiv_fasta:
            seq.write(indiv_fasta)

    command = ['sourmash',
               'compute',
               str(output) + "/*",
               '--ksizes',
               str(ksizes),
               '--scaled',
               str(scaled)]

    if track_abundance:
        command.append('--track-abundance')

    subprocess.run(' '.join(command), check=True, shell=True, cwd=str(output))

    for seq_file in glob.glob(os.path.join(str(output), '*fasta')):
        os.remove(seq_file)

    sys.stdout.flush()

    return output


def compute(sequence_file:SingleLanePerSampleSingleEndFastqDirFmt, ksizes: int, scaled: int, track_abundance: bool=True) -> MinHashSigJsonDirFormat:

    #read in FastqManifestFormat to convert from sample name to filename
    manifest = pd.read_csv(os.path.join(str(sequence_file), sequence_file.manifest.pathspec), header=0, comment='#')

    output = MinHashSigJsonDirFormat()

    for seq_file in glob.glob(os.path.join(str(sequence_file), '*fastq.gz')):
        filepath = str(seq_file)
        filename = os.path.basename(filepath)
        sampleid = list(manifest[manifest['filename']==filename]['sample-id'])
        # print(sampleid, filename)
        qiime2.util.duplicate(filepath, os.path.join(str(output), sampleid[0]+'.fastq.gz'))

    command = ['sourmash', 'compute', str(output) + "/*", '--ksizes', str(ksizes), '--scaled', str(scaled)]

    if track_abundance:
        command.append('--track-abundance')

    subprocess.run(' '.join(command), check=True, shell=True, cwd=str(output))

    for seq_file in glob.glob(os.path.join(str(output), '*fastq.gz')):
        os.remove(seq_file)

    sys.stdout.flush()

    return output
