# Как скачать данные

Если скачивать файлы по ссылке (предоставленной в файле SRA_ID), с помощью командной строки, о большая вероятность повреждения или удаления данных. Поэтому существвует удобный инструмент SRAtools для их скачивания

Скачайте инструмент \
``wget https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/3.0.1/sratoolkit.3.0.1-ubuntu64.tar.gz``\
``tar zxvf sratoolkit.3.0.1-ubuntu64.tar.gz``

Альтернатива - становка через Conda:
`conda install -c bioconda -c conda-forge -c defaults sra-tools`

Далее обязательно создайте пустую папку, куда и будут загружаться данные \
``mkdir ncbi``

Настройте инструмент (укажите созданную папку cahce->location of user-repository) \
``cd sratoolkit.3.0.1-ubuntu64/bin``\
``./vdb-config –i``

Дальше все просто, указываете команду и необходимый вам образец \
``./prefetch SRR22371859``

Определяем риды. Если это paired-end (forward и reverse) данные,то будут сгенерированы два файла, а именно SRR22371859_1.fastq и SRR22371859_2.fastq; Если это single-end данные,то будет только один файл SRR22371859.fastq. \
``./fasterq-dump --split-3 ~/deeploid/ncbi/sra/SRR22371859.sra -e 10 -o ~/deeploid/ncbi/sra/SRR22371859``
