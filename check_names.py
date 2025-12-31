import pandas as pd
from app.seoul_crime.seoul_method import SeoulMethod

m = SeoulMethod()
df = m.load_crime()

targets = ["중랑서", "도봉서"]
for name in targets:
    vals = df[df["관서명"] == name]["관서명"].unique()
    print(name, "matches", vals)

print("\nall names repr/len:")
for v in df["관서명"].unique():
    print(repr(v), len(v))

