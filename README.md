# Золотой стандарт

Нашим стандартом на данный момент будет выступать макет из 20 различных видов бактерий, ДНК которых смешали в равном количестве в 1 пробирке.

Макет необработанных данных последовательности является общедоступным \
https://github.com/andreiprodan/mock-sequences 

Геномная ДНК из микробного имитационного сообщества был секвенирован в трех отдельных прогонах (mock_1, mock_2, mock_3). Три пробных прогона образцов имеют 36464, 84054 и 146653 парных считываний соответственно.

Обратные чтения из 3-го пробного запуска (mock_3) были разделены на 2 части, из-за ограниченности размера файла на github. Нужно разархевировать и объединить файлы fastq, чтобы восстановить исходные обратные риды fastq.

Два штамма (Bacteroides vulgatus и Clostridium beijerinckii) имеют несколько вариантов последовательности в области V4 гена 16S рРНК. Bacteriodes vulgatus имеет три варианта (в соотношении 5:1:1), тогда как Clostridium beijerinckii имеет два варианта (в соотношении 13:1). Последовательности 16S рРНК золотистого стафилококка и эпидермидного стафилококка идентичны в области V4. Таким образом, макет содержит в общей сложности 22 варианта (ASV) гена 16S в области V4.

| Species |	Strain |	NCBI_reference |	16S Copy Number |	16S variants in V4 region |
| :------- | :-------: | :-------: | :---: | :----: |
| Acinetobacter baumannii |	ATCC 17978 |	NC_009085 |	5 |	1 |
| Actinomyces odontolyticus |	ATCC 17982 |	NZ_AAYI02000000 |	2 |	1 |
| Bacillus cereus |	ATCC 10987 |	NC_003909 |	12 |	1 |
| Bacteroides vulgatus* |	ATCC 8482 |	NC_009614 |	7	| 3 (5:1:1 ration) |
| Clostridium beijerinckii* |	NCIMB 8052 |	NC_009617 |	14 |	2 (13:1 ration) |
| Deinococcus radiodurans |	R1 (smooth)	| NC_001263 and NC_001264 |	3 |	1 |
| Enterococcus faecalis |	OG1RF |	NC_17316 |	4 |	1 |
| Escherichia coli |	K12 substrain MG1655 |	NC_000913 |	7 |	1 |
| Helicobacter pylori |	26695 |	NC_000915 |	2 |	1 |
| Lactobacillus gasseri |	63 AM |	NC_008530 |	6 |	1 |
| Listeria monocytogenes |	EGDe |	NC_003210 |	6 |	1 |
| Neisseria meningitidis |	MC58 |	NC_003112 |	4 |	1 |
| Propionibacterium acnes |	KPA171202 |	NC_006085 |	3 |	1 |
| Pseudomonas aeruginosa |	PAO1-LAC |	NC_002516 |	4 |	1 |
| Rhodobacter sphaeroides |	ATH 2.4.1 |	NC_007493 and NC_007494 |	3 |	1 |
| Staphylococcus aureus# |	TCH1516 |	NC_010079 |	5 |	1 (V4 identical to S. epidermidis) |
| Staphylococcus epidermidis# |	FDA strain PCI 1200 |	NC_004461 |	5 |	1 (V4 identical to S. aureus) |
| Streptococcus agalactiae |	2603 V/R |	NC_004116 |	7 |	1 |
| Streptococcus mutans |	UA159 |	NC_004350 |	5 |	1 |
| Streptococcus pneumoniae |	TIGR4 |	NC_003028 |	4 |	1 |
