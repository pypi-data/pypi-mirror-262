# BILKOM

Python package for checking train timetables from [Bilkom.pl](https://bilkom.pl)

## Source code

Check out source code in github repo: [bilkom-python](https://github.com/wnuczek/bilkom-python)

You can also try it out in jupyter notebook: [bilkom.ipynb](https://github.com/wnuczek/bilkom-python/blob/main/bilkom.ipynb)

## How to use

### Install

```bash
pip install bilkom
```

### Use as standalone script

```bash
python -m bilkom --station_name Otwock
```

### Use as package

```python
from bilkom import Bilkom
from datetime import datetime

bilkom = Bilkom()
bilkom.set_station_info(station_name="Otwock")
table = bilkom.get_station_table(date=datetime(2024,3,12)) # date is optional - defaults to datetime.now()
```

### Search for stations

```python
from bilkom import Bilkom

bilkom = Bilkom()
stations = bilkom.search_for_stations(station_name="Otwock")
```
