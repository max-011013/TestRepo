import pandas as pd
import json

df = pd.read_json("_result.json")
df.to_csv("output.csv")