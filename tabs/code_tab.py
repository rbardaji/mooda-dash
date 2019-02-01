""" All related to the content of the code tab"""
# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html

LAYOUT = [
    dcc.Markdown('''
Use the following code to obtain the same:

```python
from mooda import WaterFrame
import numpy as np
import pandas as pd

# Creating a DataFrame
number_of_values = 10
dates = pd.date_range('20180101000000', periods=number_of_values)
x = np.linspace(-np.pi, 4*np.pi, number_of_values)
df = pd.DataFrame({'TEMP': np.sin(x)+10, 'PSAL': np.cos(x)*2 + 30}, index=dates)
df.index.name = 'TIME'

# Creating metadata information
metadata = dict()
metadata['instrument'] = 'CTD'
metadata['latitude'] = '42.03'
metadata['longitude'] = '2.11'

# Creating parameter meanings
meaning = dict()
meaning['TEMP'] = {'long_name': 'sea_water_temperature',
                    'units': 'degree_celsius'}
meaning['PSAL'] = {'long_name': 'sea_water_practical_salinity',
                'units': 'PSU'}

# Creating the WaterFrame
wf = WaterFrame(df=df, metadata=metadata, meaning=meaning)
wf
```
    '''),

    html.Button("Copy code")
]
