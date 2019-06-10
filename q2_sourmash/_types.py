# ----------------------------------------------------------------------------
# Copyright (c) 2016-2018, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from qiime2.plugin import SemanticType
from q2_types.sample_data import SampleData

GenericSequenceFile = SemanticType('GenericSequenceFileFmt', variant_of=SampleData.field['type'])
MinHashSig = SemanticType('MinHashSig', variant_of=SampleData.field['type'])
SBT = SemanticType('SBT', variant_of=SampleData.field['type'])
OutputText = SemanticType('OutputText', variant_of=SampleData.field['type'])
