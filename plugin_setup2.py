from qiime2.plugin import Plugin
import sourmash

# initiate a qiime2.plugin.Plugin object
plugin = Plugin(
    name='sourmash',
    version=sourmash.__version__,
    website='https://github.com/dib-lab/q2-sourmash',
    package='q2_sourmash',
    description=('This QIIME 2 plugin supports for sourmash compute,'
                 'search and gather'),
    short_description=('Plugin for shotgun metagenomic read '
                        'classification'),
)

# define the above instance as entry point in setup.py
setup(
    entry_points={
        'qiime2.plugins': [
            'q2_sourmash=q2_sourmash.plugin_setup:plugin'
            ]
    }
)

# registering a method
def beta_phylogenetic(table: biom.Table, phylogeny: skbio.TreeNode,
                      metric: str)-> skbio.DistanceMatrix:

def sourmash_compute()
def sourmash_compare()

def alpha_group_significance(output_dir: str, alpha_diversity: pd.Series,
                             metadata: qiime2.Metadata) -> None:

## skipped
plugin.methods.register_function(
    function=q2_diversity.beta_phylogenetic,
    inputs={'table': FeatureTable[Frequency],
            'phylogeny': Phylogeny[Rooted]},
    parameters={'metric': Str % Choices(beta.phylogenetic_metrics()),
                'n_jobs': Int % Range(1, None)},
    outputs=[('distance_matrix', DistanceMatrix % Properties('phylogenetic'))],
    input_descriptions={
        'table': ('The feature table containing the samples over which beta '
                  'diversity should be computed.'),
        'phylogeny': ('Phylogenetic tree containing tip identifiers that '
                      'correspond to the feature identifiers in the table. '
                      'This tree can contain tip ids that are not present in '
                      'the table, but all feature ids in the table must be '
                      'present in this tree.')
    },
    parameter_descriptions={
        'metric': 'The beta diversity metric to be computed.',
        'n_jobs': '[Excluding weighted_unifrac] - %s' %
                  sklearn_n_jobs_description
    },
    output_descriptions={'distance_matrix': 'The resulting distance matrix.'},
    name='Beta diversity (phylogenetic)',
    description=("Computes a user-specified phylogenetic beta diversity metric"
                 " for all pairs of samples in a feature table."),
    citations=[
        citations['lozupone2005unifrac'],
        citations['lozupone2007quantitative']]
)

### pipeline

def core_metrics(ctx, table, sampling_depth, metadata, n_jobs=1):
    rarefy = ctx.get_action('feature_table', 'rarefy')
    alpha = ctx.get_action('diversity', 'alpha')
    beta = ctx.get_action('diversity', 'beta')
    pcoa = ctx.get_action('diversity', 'pcoa')
    emperor_plot = ctx.get_action('emperor', 'plot')

    results = []
    rarefied_table, = rarefy(table=table, sampling_depth=sampling_depth)
    results.append(rarefied_table)

    for metric in 'observed_otus', 'shannon', 'pielou_e':
        results += alpha(table=rarefied_table, metric=metric)

    dms = []
    for metric in 'jaccard', 'braycurtis':
        beta_results = beta(table=rarefied_table, metric=metric, n_jobs=n_jobs)
        results += beta_results
        dms += beta_results

    pcoas = []
    for dm in dms:
        pcoa_results = pcoa(distance_matrix=dm)
        results += pcoa_results
        pcoas += pcoa_results

    for pcoa in pcoas:
        results += emperor_plot(pcoa=pcoa, metadata=metadata)

    return tuple(results)

plugin.pipelines.register_function(
    function=q2_diversity.core_metrics,
    inputs={
        'table': FeatureTable[Frequency],
    },
    parameters={
        'sampling_depth': Int % Range(1, None),
        'metadata': Metadata,
        'n_jobs': Int % Range(0, None),
    },
    outputs=[
        ('rarefied_table', FeatureTable[Frequency]),
        ('observed_otus_vector', SampleData[AlphaDiversity]),
        ('shannon_vector', SampleData[AlphaDiversity]),
        ('evenness_vector', SampleData[AlphaDiversity]),
        ('jaccard_distance_matrix', DistanceMatrix),
        ('bray_curtis_distance_matrix', DistanceMatrix),
        ('jaccard_pcoa_results', PCoAResults),
        ('bray_curtis_pcoa_results', PCoAResults),
        ('jaccard_emperor', Visualization),
        ('bray_curtis_emperor', Visualization),
    ],
    input_descriptions={
        'table': 'The feature table containing the samples over which '
                 'diversity metrics should be computed.',
    },
    parameter_descriptions={
        'sampling_depth': 'The total frequency that each sample should be '
                          'rarefied to prior to computing diversity metrics.',
        'metadata': 'The sample metadata to use in the emperor plots.',
        'n_jobs': '[beta methods only] - %s' % sklearn_n_jobs_description
    },
    output_descriptions={
        'rarefied_table': 'The resulting rarefied feature table.',
        'observed_otus_vector': 'Vector of Observed OTUs values by sample.',
        'shannon_vector': 'Vector of Shannon diversity values by sample.',
        'evenness_vector': 'Vector of Pielou\'s evenness values by sample.',
        'jaccard_distance_matrix':
            'Matrix of Jaccard distances between pairs of samples.',
        'bray_curtis_distance_matrix':
            'Matrix of Bray-Curtis distances between pairs of samples.',
        'jaccard_pcoa_results':
            'PCoA matrix computed from Jaccard distances between samples.',
        'bray_curtis_pcoa_results':
            'PCoA matrix computed from Bray-Curtis distances between samples.',
        'jaccard_emperor':
            'Emperor plot of the PCoA matrix computed from Jaccard.',
        'bray_curtis_emperor':
            'Emperor plot of the PCoA matrix computed from Bray-Curtis.',
    },
    name='Core diversity metrics (non-phylogenetic)',
    description=("Applies a collection of diversity metrics "
                 "(non-phylogenetic) to a feature table.")
)


