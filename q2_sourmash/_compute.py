# ----------------------------------------------------------------------------
# Copyright (c) 2016-2018, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import qiime2.util
import os
import subprocess
import glob
from typing import Union
from ._format import MinHashSigDirFmt, GenericSequenceFileDirFmt

def compute(sequence_file: GenericSequenceFileDirFmt, ksizes: int, scaled: int, track_abundance: bool=True, metadata_file: str) -> MinHashSigDirFmt:

    output = MinHashSigDirFmt()

    #read in FastqManifestFormat to convert from sample name to filename
    if metadata_file:
        # read metadata in from command line option
        metadata = pd.read_csv(metadata_file, header=0, comment='#')
    
    elif sequence_file.manifest:
        if metadata_file:
            sys.stderr.write('*** WARNING: Both MANIFEST and metadata files are provided. The metadata file provided in command line is used\n')
        else:
            metadata = pd.read_csv(os.path.join(str(sequence_file), sequence_file.manifest.pathspec), header=0, comment='#')

    else:
        metadata = None

    files = glob.glob(os.path.join(str(sequence_file), '*'))
    to_remove = set(['MANIFEST', 'metadata.yml'])
    seq_files = [f for f in files if f not in to_remove]

    for seq_file in seq_files:
        filepath = str(seq_file)
        filename = os.path.basename(filepath)
        try:
            sampleid = list(metadata[metadata['filename']==filename]['sample-id'])
        except:
            sys.stderr.write('*** WARNING: no metadata file is provided; the first part of file name splited by "." is used as label of that sample\n')
            sampleid = filename.split('.')[0]

        qiime2.util.duplicate(filepath, os.path.join(str(output), f'{sampleid[0]}'))

    command = ['sourmash', 'compute', str(output) + "/*", '--ksizes', str(ksizes), '--scaled', str(scaled)]

    if track_abundance:
        command.append('--track-abundance')

    # subprocess cwd can automactically adjust all paths
    subprocess.run(' '.join(command), check=True, shell=True, cwd=str(output))

    for seq_file in seq_files:
        os.remove(seq_file)

    return output
