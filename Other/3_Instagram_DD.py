import os
import json
import numpy as np
import pandas as pd

path = '/Users/dd/Documents/Python/instagram-dzung/connections/followers_and_following'

with open('/Users/dd/Documents/Python/instagram-dzung/connections/followers_and_following/followers_1.json','r',encoding = 'utf-8') as f:
    df = json.load(f)
# for key in df:
    # print(f"{key}:{type(df[key])}")
print(df)
# print(json.dumps(df['relationships_following'][3:], indent = 4, ensure_ascii = False))