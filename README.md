# QIIME 2 Sourmash Plugin

This is a QIIME 2 plugin. For details on QIIME 2, see https://qiime2.org. For details on sourmash, see http://sourmash.readthedocs.io/. 

## Installing the QIIME 2 sourmash plugin 

q2-sourmash is a QIIME 2 plugin for sourmash, a tool computing and comparing MinHash signatures for nucleotide sequences fast and effieciently. You can find out more about sourmash by reading the paper [(Brown and Irber, JOSS 2018)](http://joss.theoj.org/papers/10.21105/joss.00027) or checking out the [sourmash documentation](https://sourmash.readthedocs.io/en/latest/). 

You need to have QIIME 2 version 2018.4 or later. Also, regardless of which way you install, you need to be in a QIIME 2 environment for this to work. [Install QIIME 2](https://docs.qiime2.org/2018.8/install/) and activate the QIIME 2 virtual environment (e.g. `source activate qiime2-2018.8`), and then install sourmash by running:

`conda install -c bioconda sourmash`

To install the plugin, run the following command:

```
pip install https://github.com/dib-lab/q2-sourmash/archive/master.zip
```

To check that the installation worked, type `qiime` on the command line. The sourmash plugin should show up in the list of available plugins.

## Using the QIIME2 sourmash plugin

Currently there are two main methods for use in the Qiime2 sourmash plugin: `compute` to calcualte MinHash signatures from nucleotide sequences and `compare` to calculate a Jaccard distance between samples. 

### Computing signatures

The `compute` calcuates the minhash signatures for a given set of nucleotide sequences. To run, one must simply supply a `.qza` archive (directory) containing sequence file ending with 'fastq.gz'.

First download a test set of fastq.gz files already in the form of a qza archive and the associated metadata. Here we are using data from the [Moving Pictures tutorial](https://docs.qiime2.org/2018.8/tutorials/moving-pictures/):

```
wget -c -nc https://docs.qiime2.org/2018.4/data/tutorials/moving-pictures/demux.qza
wget -c -nc https://data.qiime2.org/2018.8/tutorials/moving-pictures/sample_metadata.tsv 
```

To calculate sourmash signatures for all sequence files within the archive use the following:

`qiime sourmash compute --i-sequence-file demux.qza --p-ksizes 21 --p-scaled 10000 --o-min-hash-signature sigs.qza`

The following flags are required: 

* `--i-sequence-file` : the path to the qza directory
* `--p-ksizes` : the k-size of the hash (integer)
* `--p-scaled` : the scaled value (integer)
* `--o-min-hash-signature` : the output qza file name

The output archive, in this case `sigs.qza`, contains the signature files for each of the fastq.gz files that were input. They can be viewed using the [qiime online viewer](https://view.qiime2.org/) or by unzipping the qza file. 

```
qiime tools export --input-path sigs.qza --output-path sigs
```

### Comparing signatures

Signatures that have been calculated as above can then be compared using `sourmash compare`. This will calculate a pair-wise Jaccard distance between each of the samples included in the provided qza archive: 

```
qiime sourmash compare --i-min-hash-signature sigs.qza --p-ksize 21 --o-compare-output compare.mat.qza
```

The output, `compare.mat.qza`, can then be investigated as above by unzipping the qza archive or can be pushed through subsequent analyses (e.g. generate a PCoA plot):
```
qiime diversity pcoa --i-distance-matrix compare.mat.qza  --o-pcoa pcoa.compare.mat.qza
qiime emperor plot --i-pcoa pcoa.compare.mat.qza --o-visualization emperor.qzv --m-metadata-file sample_metadata.tsv
```

