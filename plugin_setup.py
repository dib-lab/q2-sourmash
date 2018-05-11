# ----------------------------------------------------------------------------
# Copyright (c) 2016-2018, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------


import q2_sourmash

from qiime2.plugin import Plugin, Metadata, Str, List, Citations, SemanticType, SingleFileDirectoryFormat, TextFileFormat

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

MinHashSig = SemanticType('MinHashSig')

plugin.register_semantic_types(MinHashSig)

class MinHashSigJson(TextFileFormat):
    def

__validate__
