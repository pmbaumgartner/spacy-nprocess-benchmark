import json
from pathlib import Path

import pandas as pd

files = Path("data/").glob("*.json")
data = [json.loads(file.read_text()) for file in files]

import hiplot as hip

hip.Experiment.from_iterable(data).display()

df = pd.DataFrame(data)
df.to_csv("data/agg/data.csv")
