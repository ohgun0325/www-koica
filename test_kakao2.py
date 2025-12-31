import requests

queries = [
    "도봉경찰서",
    "서울 도봉경찰서",
    "서울 도봉구 노해로 403",
    "노해로 403 도봉경찰서",
    "중랑경찰서",
    "서울 중랑경찰서",
    "서울 중랑구 신내로 153",
    "신내로 153 중랑경찰서",
]

key = "KakaoAK 5d7c72ef44244f2d0c9e3d3927fc891d"
headers = {"Authorization": key}

for q in queries:
    r = requests.get(
        "https://dapi.kakao.com/v2/local/search/keyword.json",
        headers=headers,
        params={"query": q},
    )
    data = r.json()
    cnt = len(data.get("documents", []))
    print(f"\nQ: {q} | status={r.status_code} | count={cnt}")
    if cnt:
        d = data["documents"][0]
        print(f"  addr: {d.get('address_name')}")
        print(f"  x: {d.get('x')}, y: {d.get('y')}")

