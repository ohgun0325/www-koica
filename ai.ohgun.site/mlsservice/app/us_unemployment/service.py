import requests
import pandas as pd
import folium
from typing import Optional, Union
from pathlib import Path


class USUnemploymentMap:
    """
    미국 주별 실업률 Choropleth 맵을 생성하는 서비스 클래스.
    """

    def __init__(
        self,
        geo_url: str = "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_states.json",
        data_url: str = "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_unemployment_oct_2012.csv",
        location: Optional[list[Union[int, float]]] = None,
        zoom_start: int = 3,
    ) -> None:
        self.geo_url = geo_url
        self.data_url = data_url
        self.location = location or [48, -102]
        self.zoom_start = zoom_start

    def fetch_geo(self):
        """주 경계 GeoJSON을 가져온다."""
        return requests.get(self.geo_url).json()

    def fetch_data(self) -> pd.DataFrame:
        """실업률 CSV 데이터를 DataFrame으로 가져온다."""
        return pd.read_csv(self.data_url)

    def build_map(self) -> folium.Map:
        """Choropleth 맵을 생성해 반환한다."""
        state_geo = self.fetch_geo()
        state_data = self.fetch_data()

        m = folium.Map(location=self.location, zoom_start=self.zoom_start)

        folium.Choropleth(
            geo_data=state_geo,
            name="choropleth",
            data=state_data,
            columns=["State", "Unemployment"],
            key_on="feature.id",
            fill_color="YlGn",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name="Unemployment Rate (%)",
        ).add_to(m)

        folium.LayerControl().add_to(m)
        return m

    def save_html(self, path: Optional[str] = None) -> str:
        """맵을 HTML로 저장하고 경로를 반환한다.

        기본 저장 위치: 현재 모듈의 `save/us_unemployment.html`
        """
        # 기본 저장 경로 설정
        if path is None:
            save_dir = Path(__file__).resolve().parent / "save"
            save_dir.mkdir(exist_ok=True)
            path = save_dir / "us_unemployment.html"
        else:
            path = Path(path)
            path.parent.mkdir(exist_ok=True, parents=True)

        m = self.build_map()
        m.save(path)
        return str(path)


# 사용 예시
if __name__ == "__main__":
    service = USUnemploymentMap()
    service.save_html()