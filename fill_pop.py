import pandas as pd
from pathlib import Path

csv_path = Path("/app/app/seoul_crime/save/seoul_merged_all.csv")
pop_path = Path("/app/app/seoul_crime/data/pop.xls")

merged = pd.read_csv(csv_path)
pop = pd.read_excel(pop_path, header=2)

if "자치구" not in pop.columns:
    raise SystemExit("자치구 column not found in pop.xls")

pop = pop[["자치구", "세대", "계", "남자", "여자"]]
pop = pop.dropna(subset=["자치구"])
pop["자치구"] = pop["자치구"].astype(str).str.strip()
pop_map = pop.set_index("자치구").to_dict(orient="index")

# strip 기관명
merged["기관명"] = merged["기관명"].astype(str).str.strip()

for idx, row in merged.iterrows():
    key = row["기관명"]
    if key in pop_map:
        info = pop_map[key]
        for src, dst in [("세대", "인구_세대"), ("계", "인구_계"), ("남자", "인구_남자"), ("여자", "인구_여자")]:
            if pd.isna(row.get(dst)) or row.get(dst) == "":
                merged.at[idx, dst] = info[src]
    else:
        # debug missing key
        pass

for col in ["인구_세대", "인구_계", "인구_남자", "인구_여자"]:
    merged[col] = pd.to_numeric(merged[col], errors="coerce")

merged.to_csv(csv_path, index=False, encoding="utf-8-sig")
print("Done. NaN counts:", merged[["인구_세대", "인구_계", "인구_남자", "인구_여자"]].isna().sum().to_dict())
# print rows still NaN
missing = merged[merged[["인구_세대", "인구_계", "인구_남자", "인구_여자"]].isna().any(axis=1)][["관서명","기관명","인구_세대","인구_계","인구_남자","인구_여자"]]
print("Missing rows:\\n", missing)
print("Pop keys sample:", list(pop_map.keys())[:5])
print("Missing 기관명 repr:", [repr(x) for x in missing['기관명'].unique()])

