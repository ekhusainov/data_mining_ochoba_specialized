# data_mining_ochoba_specialized
 Более простая версия для скачивания, убрал всё лишнее.

Установка и создание окружения в conda:
```
conda create -n $environment_name python=3.10
```
```
conda activate $environment_name
```
```
pip install -e .
```

Скачиваем посты с VC.RU с 1 по 101 (1 + 100).

```
python src/data_mining.py download -s vc -c posts -f 1 -n 100
```

Скачиваем комменты с VC.RU с 1 по 101 (1 + 100).

```
python src/data_mining.py download -s vc -c comments -f 1 -n 100
```

Скачиваем посты с TJOURNAL.RU с 1 по 101 (1 + 100).

```
python src/data_mining.py download -s tj -c posts -f 1 -n 100
```

Скачиваем комменты с TJOURNAL.RU с 1 по 101 (1 + 100).

```
python src/data_mining.py download -s tj -c comments -f 1 -n 100
```

Скачиваем посты с DTF.RU с 1 по 101 (1 + 100).

```
python src/data_mining.py download -s dtf -c posts -f 1 -n 100
```

Скачиваем комменты с DTF.RU с 1 по 101 (1 + 100).

```
python src/data_mining.py download -s dtf -c comments -f 1 -n 100
```

-j yes — запаковывает скаченное в json.dumps. По умолчанию это не делает.

```
python src/data_mining.py download -s vc -c posts -f 1 -n 100 -j yes
```