# ----------------------------------------------------------------------------
# Copyright (c) 2016-2018, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import qiime2.plugin.model as model

class MinHashSigJson(model.TextFileFormat):
    def _validate_(self, level):
        pass #Fill in with some sort of json test?

class MinHashSigJsonDirFormat(model.DirectoryFormat):
    signatures = model.FileCollection(
        r'.*\.sig', format=MinHashSigJson)

    @signatures.set_path_maker
    def signature_path_maker(self, name):
        return(name + '.sig')

class SequenceBloomTree(model.TextFileFormat):
    def _validate_(self, level):
        pass #Fill in with some sort of json test?
