import pandas as pd

FILE = "/app/app/seoul_crime/save/seoul_merged_all.csv"

df = pd.read_csv(FILE)
cols = ["인구_세대", "인구_계", "인구_남자", "인구_여자"]

print("NaN count:")
print(df[cols].isna().sum())

missing = df[df[cols].isna().any(axis=1)][["관서명", "기관명"] + cols]
print("\nRows with NaN:")
print(missing)

