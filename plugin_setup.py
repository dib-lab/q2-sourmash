# ----------------------------------------------------------------------------
# Copyright (c) 2016-2018, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------


import q2_sourmash
import tempfile

<<<<<<< HEAD
from qiime2.plugin import Plugin, Metadata, Str, List, Citations, SemanticType, SingleFileDirectoryFormat, TextFileFormat, ValidationError
from qiime2.plugin import model
=======
from qiime2.plugin import Plugin, Metadata, Str, List, Citations, SemanticType, SingleFileDirectoryFormat, TextFileFormat
>>>>>>> 58c5556d76b2ebdf6bea05ba8bf4a02a916ab63d

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
<<<<<<< HEAD

plugin.register_semantic_types(MinHashSig)

load_signature_json()

class MinHashSigJson(TextFileFormat):
    def _validate_(self, level):
        pass

class MinHashSigJsonDirFormat(model.DirectoryFormat):
    signatures = model.FileCollection( 
        r'.*\.sig', format=MinHashSigJson)

    @signature.set_path_maker
    def signature_path_maker(self, name):
        return(name + '.sig')

plugin.register_views(MinHashSigJson, MinHashSigJsonDirFormat)

plugin.register_semantic_type_to_format(
    MinHashSig,
    artifact_format=MinHashSigJsonDirFormat
)
=======

plugin.register_semantic_types(MinHashSig)

class MinHashSigJson(TextFileFormat):
    def

__validate__
>>>>>>> 58c5556d76b2ebdf6bea05ba8bf4a02a916ab63d
