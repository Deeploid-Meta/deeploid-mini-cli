Пайплайн для запуска vsearch (от обработки данных до таксономии) \

Аргументы: \
('-r', '--raw_reads_dir', help='Forward reads file (or single-end) in fastq|fq|gz|tar.gz format', required=True) \
('-o', '--outdir', help='Output folder with artifacts and data', required=True) \
('-se', '--is_single_ended', help='Analyse as single ended', required=False, default=False) \
('-t', '--trimming', help='Trim raw reads before analysis', required=False, default=False) 

Пример запуска (для paired-ended data с триммингом): python vsearch_pipeline.py -r raw_reads -o output_folder_pe_trimmed -se False -t True \
В папке raw_reads должны лежать .fastq файлы в формате {sample_name}_1.fastq и {sample_name}_2.fastq.
Если флаг -se True, то будут использованы только {sample_name}_1.fastq файлы для анализа.
