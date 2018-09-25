# ----------------------------------------------------------------------------
# Copyright (c) 2016-2018, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------


import q2_sourmash

import qiime2.plugin
from qiime2.plugin import (
    Plugin, Metadata, Str, List, Citations, 
    SemanticType, TextFileFormat, ValidationError
)
from qiime2.plugin import model
import qiime2.util
from q2_sourmash._compute import compute
from q2_sourmash._compare import compare
from q2_types.distance_matrix import DistanceMatrix
from q2_types.sample_data import SampleData
from q2_types.per_sample_sequences import SequencesWithQuality
from ._format import (
        MinHashSigJsonDirFormat, MinHashSigJson, 
        SequenceBloomTree)
from ._types import MinHashSig
from type import Union

plugin = Plugin(
    name='sourmash',
    version='0.0.0',
    website='http://sourmash.readthedocs.io/en/latest/',
    package='q2_sourmash',
    citations=Citations.load('citations.bib', package='q2_sourmash'),
    description=('This QIIME 2 plugin wraps sourmash and '
                 'supports the calculation and comparison of  '
                 'minhash signatures.'),
    short_description='Plugin for generation of minhash signatures.'
)


plugin.register_semantic_type_to_format(
    MinHashSig,
    artifact_format=MinHashSigJson
)

plugin.register_semantic_type_to_format(
    MinHashSigDir,
    artifact_format=MinHashSigJsonDirFormat
)

plugin.register_semantic_type_to_format(
    SBT,
    artifact_format=SequenceBloomTree
)

plugin.register_views(
    MinHashSigJson, 
    MinHashSigJsonDirFormat, 
    SequenceBloomTree)

plugin.register_semantic_types(MinHashSig, MinHashSigDir, SBT)

plugin.methods.register_function(
    function=compute,
    inputs={'sequence_file': SampleData[SequencesWithQuality]},
    parameters={
        'ksizes': qiime2.plugin.Int,
        'scaled': qiime2.plugin.Int,
        'track_abundance': qiime2.plugin.Bool
    },
    outputs=[('min_hash_signature', MinHashSigDir)],
    name = 'sourmash compute',
    description = (
        'Computes a sourmash MinHash signature from fasta/q files.'
    )
)

plugin.methods.register_function(
    function=compare,
    inputs={'min_hash_signature':MinHashSigDir},
    parameters={
        'ksize': qiime2.plugin.Int,
        'ignore_abundance': qiime2.plugin.Bool
    },
    outputs=[('compare_output', DistanceMatrix)],
    name = 'sourmash compare',
    description = (
        'Compares sourmash signatures and calculats '
        'Jacaard distance matrix.'
    )
)

plugin.methods.register_function(
    function=search,
    inputs={
        'query_signature':MinHashSig, 
        'db_signature':Union(MinHashSigDir, SBT)
    },

    parameters={
        'output': qiime2.plugin.TextFileFormat,
        'ksize': qiime2.plugin.Int,
        'threshold': qiime2.plugin.Float,
        'scale': qiime2.plugin.Int,
        'containment': qiime2.plugin.Bool
    },
    outputs=[('search_output', qiime2.plugin.TextFileFormat)],
    name = 'sourmash search'
    description = (
        'Search signatures in a directory of sigs or'
        'sequence bloom tree'
    )
)
