wget -c -nc https://docs.qiime2.org/2018.4/data/tutorials/moving-pictures/demux.qza

qiime sourmash compute --i-sequence-file demux.qza --p-ksizes 21 --p-scaled 10000 --o-min-hash-signature sigs || { echo "compute fail"; rm demux.qza; exit 1; }

qiime sourmash compare --i-min-hash-signature sigs.qza --p-ksize 21 --o-compare-output compare.mat || { echo "compare fail"; rm sigs.qza; exit 1; }

echo "tests passed"
#rm -f sigs.qza compare.mat.qza demux.qza
