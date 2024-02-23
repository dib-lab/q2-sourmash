# ----------------------------------------------------------------------------
# Copyright (c) 2016-2018, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import qiime2.util
from q2_types.distance_matrix import DistanceMatrix
from q2_types.per_sample_sequences import SequencesWithQuality
from q2_types.sample_data import SampleData
from q2_types.per_sample_sequences import MAGs
from qiime2.plugin import Plugin, Citations

from q2_sourmash._compare import compare
from q2_sourmash._compute import compute
from ._format import MinHashSigJsonDirFormat, MinHashSigJson
from ._types import MinHashSig

plugin = Plugin(
    name='sourmash',
    version='0.0.0',
    website='http://sourmash.readthedocs.io/en/latest/',
    package='q2_sourmash',
    citations=Citations.load('citations.bib', package='q2_sourmash'),
    description=('This QIIME 2 plugin wraps sourmash and '
                 'supports the calculation and comparison of  '
                 'MinHash signatures.'),
    short_description='Plugin for generation of MinHash signatures.'
)


plugin.register_semantic_type_to_format(
    MinHashSig,
    artifact_format=MinHashSigJsonDirFormat
)
plugin.register_views(MinHashSigJson, MinHashSigJsonDirFormat)
plugin.register_semantic_types(MinHashSig)

plugin.methods.register_function(
    function=compute,
    inputs={'sequence_file': SampleData[SequencesWithQuality | MAGs]},
    parameters={
        'ksizes': qiime2.plugin.Int,
        'scaled': qiime2.plugin.Int,
        'track_abundance': qiime2.plugin.Bool
    },
    outputs=[('min_hash_signature', MinHashSig)],
    name='Compute sourmash signature',
    description='Computes a sourmash MinHash signature from fasta/q files.'
)

plugin.methods.register_function(
    function=compare,
    inputs={'min_hash_signature': MinHashSig},
    parameters={
        'ksize': qiime2.plugin.Int,
        'ignore_abundance': qiime2.plugin.Bool
    },
    outputs=[('compare_output', DistanceMatrix)],
    name='Compare sourmash signatures',
    description='Compares sourmash signatures and '
                'calculates Jacaard distance matrix.'
)
