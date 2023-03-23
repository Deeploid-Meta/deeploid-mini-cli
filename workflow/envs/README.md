# File description

1. _qiime2.yaml_ - Мишины зависимости из файла сборки qiime2-2022.8-py38-linux-conda.yml
   - фактически копия qiime2-2022.8-py38-linux-conda.yml
   - Здесь все прописано и выглядит страшно
2. _qiime.yaml_ - Вариант от Никиты, где идет указание для conda на файл сборки qiime2-2022.8-py38-linux-conda.yml
   - ну типа инкапсуляция, мб потом пригодится
   - все страшное лежит уже в сборке
3. _vsearch.yaml_ - пока пусто, но там как в qiime2.yaml
4. _deblur.yaml_ - пока пусто, но там как в qiime2.yaml
5. _dada2.yaml_ - (name: dada2-v1.14)

## Tests

Запускаю на винде под WSL2(ubuntu-20.04)

библиотеки скачиваю с сайта [qiime2](https://docs.qiime2.org/2022.8/install/native/)

- qiime2_2023_2_py38.yaml установилось, но проблема в `ValueError: The scikit-learn version (0.23.1) used to generate this artifact does not match the current version of scikit-learn installed (0.24.1). Please retrain your classifier for your current deployment to prevent data-corruption errors.`
- qiime2_2020_8_py36.yaml установилось, работает идеально для `MVP`, но проблема у Миши в пайплайне неработает `Traceback (most recent call last):
               File "workflow/scripts/qiime2_pipeline.py", line 297, in <module>
                 main()
               File "workflow/scripts/qiime2_pipeline.py", line 249, in main
                 taxonomy=result_taxonomy.classification)
               TypeError: barplot() missing 1 required positional argument: 'metadata'`
- qiime2.yaml (мишино окружение) не встает, дает ошибку `Encountered problems while solving: package numpy-1.18.1-py36h4f9e942_0 requires libgfortran-ng >=7,<8.0a0, but none of the providers can be installed`
- qiime2_2022_11_py38.yaml установилось, но проблема в `ValueError: The scikit-learn version (0.23.1) used to generate this artifact does not match the current version of scikit-learn installed (0.24.1). Please retrain your classifier for your current deployment to prevent data-corruption errors.`
- qiime2_2022_8_py38.yaml (мишино но с сайта) не встает, дает ошибку `Encountered problems while solving: package numpy-1.18.1-py36h4f9e942_0 requires libgfortran-ng >=7,<8.0a0, but none of the providers can be installed` Мб проблема в нампай снейк окружения, я хз( у меня в снейке стоит 1.24.2)
- dada2.yaml - (name: dada2-v1.14)

"import numpy print(numpy.__version__)"
