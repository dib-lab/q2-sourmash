# ----------------------------------------------------------------------------
# Copyright (c) 2016-2018, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import glob
import os
import subprocess
import sys
from typing import Union

import pandas as pd
import qiime2.util
from q2_types.per_sample_sequences import (
    SingleLanePerSampleSingleEndFastqDirFmt
)
from q2_types_genomics.per_sample_data import MultiMAGSequencesDirFmt

from q2_sourmash._format import MinHashSigJsonDirFormat


def _duplicate_mag_seqs(manifest, sequence_file):
    output = MinHashSigJsonDirFormat()
    for i, row in manifest.iterrows():
        _, bin_id, src_fp = row["sample-id"], row["mag-id"], row["filename"]
        src_fp = os.path.join(str(sequence_file), src_fp)
        dest_fp = os.path.join(str(output), f'{bin_id}.fasta')
        qiime2.util.duplicate(src_fp, dest_fp)
    return output


def _duplicate_seqs(manifest, sequence_file):
    output = MinHashSigJsonDirFormat()
    for seq_file in glob.glob(os.path.join(str(sequence_file), '*.fastq.gz')):
        src_fp = str(seq_file)
        filename = os.path.basename(src_fp)
        sample_id = list(
            manifest[manifest['filename'] == filename]['sample-id']
        )
        dest_fp = os.path.join(str(output), f'{sample_id[0]}.fastq.gz')
        qiime2.util.duplicate(src_fp, dest_fp)
    return output


def compute(
        sequence_file: Union[
            SingleLanePerSampleSingleEndFastqDirFmt, MultiMAGSequencesDirFmt
        ],
        ksizes: int,
        scaled: int,
        track_abundance: bool = True
) -> MinHashSigJsonDirFormat:
    # read in FastqManifestFormat to convert from sample name to filename
    manifest = pd.read_csv(
        os.path.join(str(sequence_file), sequence_file.manifest.pathspec),
        header=0, comment='#'
    )

    if isinstance(sequence_file, MultiMAGSequencesDirFmt):
        output = _duplicate_mag_seqs(manifest, sequence_file)
    else:
        output = _duplicate_seqs(manifest, sequence_file)

    command = [
        'sourmash', 'compute', f'{output}/*',
        '--ksizes', str(ksizes),
        '--scaled', str(scaled)
    ]

    if track_abundance:
        command.append('--track-abundance')

    subprocess.run(' '.join(command), check=True, shell=True, cwd=str(output))

    if isinstance(sequence_file, MultiMAGSequencesDirFmt):
        ext = '*.fasta'
    else:
        ext = '*.fastq.gz'
    for fp in glob.glob(os.path.join(str(output), ext)):
        os.remove(fp)

    sys.stdout.flush()

    return output
