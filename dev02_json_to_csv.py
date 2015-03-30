##encoding=UTF8

from angora.DATA import *
import pandas as pd

csv = list()
data = load_js(r"backup\averagebill_data_by_county.json")
for k, v in data.items():
    county, state, month = k.split("_")
    csv.append(("%s_%s" % (county, state), month, v))
        
df = pd.DataFrame(csv, columns=["county", "month", "cost"])
df.to_csv("by_county.txt")

csv = list()
data = load_js(r"backup\averagebill_data_by_state.json")
for k, v in data.items():
    state, month = k.split("_")
    csv.append((state, month, v))
        
df = pd.DataFrame(csv, columns=["state", "month", "cost"])
df.to_csv("by_state.txt")