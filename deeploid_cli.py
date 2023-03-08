import argparse
import os
import os.path
import random
import string
from datetime import datetime
from inspect import getsourcefile


def config_maker(settings, config_file):
    """
    Creates config
    """
    config = f"""
    "tool" : "{settings["tool"]}"
    "forward_reads": "{settings["forward_reads"]}"
    "reverse_reads" : "{settings["reverse_reads"]}"
    "outdir" : "{settings["outdir"]}"
    "database" : "{settings["database"]}"
    "threads" : "{settings["threads"]}"
    "working_dir" : "{settings["working_dir"]}"
    "taxonomy": "{settings["taxonomy"]}"
    """

    if not os.path.exists(os.path.dirname(config_file)):
        os.mkdir(os.path.dirname(config_file))

    with open(config_file, "w") as fw:
        fw.write(config)
        print(f"CONFIG IS CREATED! {config_file}")


def main(settings):
    '''
    Runs snakemeake
    '''
    command = f"""
    snakemake --snakefile {settings["working_dir"]}/workflow/snakefile \
              --configfile {settings["config_file"]} \
              --cores {settings["threads"]} \
              --use-conda """
    print(command)
    os.system(command)
    print('snakemake runs...')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='deeploid pipeline for 16s rrna data analysis')

    parser.add_argument(
        '-t', '--tool',
        help='Tool to use in  dada2|qiime2|vsearch|deblur',
        required=True, default="qiime2")
    parser.add_argument(
        '-1', '--forward_reads',
        help='Forward reads file (or single-end) in fastq|fq|gz|tar.gz format',
        required=True)
    parser.add_argument(
        '-2', '--reverse_reads',
        help='Reverse reads file in fastq|fq|gz|tar.gz format',
        required=True)
    parser.add_argument(
        '-o', '--outdir', help='Output folder (default = reads folder)',
        required=False, default="output")
    parser.add_argument(
        '-wd', '--working_dir', help='Path to execution directory',
        required=False, default=".")
    parser.add_argument(
        '-db', '--database', help='Path to database (fasta)',
        required=False, default=False)
    parser.add_argument(
        '-nt', '--threads', help='Number of threads (default = 8)',
        required=False, default=int(8), type=int)
    parser.add_argument(
        '-tx', '--taxonomy', help='file.txt with taxonomy',
        required=True)

    args = vars(parser.parse_args())

    execution_folder = args["working_dir"]
    execution_folder_danila = os.path.dirname(
        os.path.abspath(getsourcefile(lambda: 0)))
    execution_time = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    random_letters = "".join(
        [random.choice(string.ascii_letters) for n in range(3)])
    # пока что не вижу смысла создавать по времени конфиг, это все решится на стороне бэка
    config_file = os.path.join(execution_folder, f"config/config.yaml")
    settings = {
        'tool': args["tool"],
        'forward_reads': args["forward_reads"],
        'reverse_reads': args["reverse_reads"],
        'outdir': args["outdir"],
        'database': args["database"],
        'threads': args["threads"],
        'working_dir': execution_folder,
        'config_file': config_file,
        'taxonomy': args["taxonomy"]
    }

    config_maker(settings, config_file)
    main(settings)
