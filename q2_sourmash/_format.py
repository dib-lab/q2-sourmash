# ----------------------------------------------------------------------------
# Copyright (c) 2016-2018, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import qiime2.plugin.model as model

class MinHashSigFmt(model.TextFileFormat):
    def _validate_(self, level):
        pass #Fill in with some sort of json test?

class MinHashSigDirFmt(model.DirectoryFormat):
    signatures = model.FileCollection(
        r'.*\.sig', format=MinHashSigFmt)

    @signatures.set_path_maker
    def signature_path_maker(self, name):
        return(name + '.sig')

SingleMinHashSigDirFmt = model.SingleFileDirectoryFormat(
    'SingleMinHashSigDirFmt',
    'minhash.sig',
    MinHashSigFmt
)

class SBTFmt(model.TextFileFormat):
    def _validate_(self, level):
        pass #Fill in with some sort of sbt test?

SBTDirFmt = model.SingleFileDirectoryFormat(
    'SBTDirFmt', 
    'minhashsig.stb.json', 
    SBTFmt
)

class OutputTextFmt(model.TextFileFormat):
    def _validate_(self, level):
        pass

OutputTextDirFmt = model.SingleFileDirectoryFormat(
    'OutputTextDirFmt',
    'output.txt',
    OutputTextFmt
)

class GenericSequenceFileFmt(model.TextFileFormat):
    def _validate_(self, level):
        pass

GenericSequenceFileDirFmt = model.SingleFileDirectoryFormat(
    'GenericSequenceFileDirFmt',
    'sequences',
    GenericSequenceFileFmt
)
