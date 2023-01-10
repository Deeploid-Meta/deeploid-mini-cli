import argparse
import shutil
from pathlib import Path

from qiime2.sdk import PluginManager

import qiime2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='qiime2 train classifier')
    parser.add_argument(
        '-1', '--database',
        help='DB in fasta format',
        required=True)
    parser.add_argument(
        '-2', '--taxonomy',
        help='Database taxonomy', required=True,
        default=False)
    parser.add_argument(
        '-o', '--outdir', help='Output folder (default = reads folder)',
        required=False, default=False)
    parser.add_argument(
        '-t', '--threads', help='Number of threads (default = 8)',
        required=False, default=8, type=int)
    return parser


def main():
    parser = build_parser()
    args = vars(parser.parse_args())

    # Create output directory
    output = Path(args['outdir'])
    output.mkdir(exist_ok=True)

    # Create qiime2 artifacts directory
    qiime2_artifacts = output / 'qiime2_artifacts'
    qiime2_artifacts.mkdir(exist_ok=True)

    # Create temporary directory
    tmp_output = output / Path('tmp')
    tmp_output.mkdir(exist_ok=True)

    # Create working directory
    working_dir = output / Path('working_dir')
    working_dir.mkdir(exist_ok=True)

    database_path = Path(args['database'])
    taxonomy_path = Path(args['taxonomy'])

    # Import data
    database = qiime2.Artifact.import_data(
        'FeatureData[Sequence]', str(database_path))
    database.save(
        str(qiime2_artifacts / 'database.qza'))

    taxonomy = qiime2.Artifact.import_data(
        'FeatureData[Taxonomy]', str(taxonomy_path))
    taxonomy.save(
        str(qiime2_artifacts / 'taxonomy.qza'))

    num_threads = args['threads']

    # Load plugins
    plugin_manager = PluginManager(True)

    # Extract reference reads
    feature_classifier = plugin_manager.plugins['feature-classifier']
    extract_reads = feature_classifier.actions['extract_reads']

    ref_seqs = extract_reads(
        sequences=database,
        f_primer='GTGCCAGCMGCCGCGGTAA',
        r_primer='GGACTACHVGGGTWTCTAAT',
        trunc_len=120,
        min_length=100,
        max_length=400,
        n_jobs=num_threads
    )

    fit_classifier = feature_classifier.actions['fit_classifier_naive_bayes']
    result = fit_classifier(
        reference_reads=ref_seqs.reads,
        reference_taxonomy=taxonomy
    )
    result.classifier.save(
        str(output / f'{database_path.stem}_classifier.qza'))

    # Remove temporary files
    shutil.rmtree(working_dir)
    shutil.rmtree(tmp_output)


if __name__ == "__main__":
    main()
