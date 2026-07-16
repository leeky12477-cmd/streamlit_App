import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(
    page_title="서울시 공영 주차장 탐색기",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 공영 주차장 정보 통합 안내소")
st.markdown("공영 주차장 데이터를 업로드하고 자치구별 가장 저렴한 주차장과 위치 정보를 지도로 확인하세요.")

# 1. 파일 업로드 기능
st.sidebar.header("📁 데이터 업로드")
uploaded_file = st.sidebar.file_uploader("주차장 정보 CSV 파일을 업로드해주세요.", type=["csv"])

# 샘플 데이터 생성 기능 (파일이 없을 때 예시용)
@st.cache_data
def get_sample_data():
    data = {
        '주차장명': ['강남역 공영주차장', '역삼역 공영주차장', '마포 공영주차장', '홍대 서측 공영주차장', '종로 주차장'],
        '위도': [37.4979, 37.5006, 37.5411, 37.5518, 37.5721],
        '경도': [127.0276, 127.0364, 126.9472, 126.9205, 126.9796],
        '주소': ['강남구 역삼동 123-4', '강남구 역삼동 567-8', '마포구 도화동 99', '마포구 서교동 45', '종로구 종로1가 1'],
        '주차요금': [3000, 4000, 1500, 2000, 0],  # 0원은 무료
        '자치구': ['강남구', '강남구', '마포구', '마포구', '종로구'],
        '무료여부': ['유료', '유료', '유료', '유료', '무료'],
        '주말운영여부': ['운영', '미운영', '운영', '운영', '운영']
    }
    return pd.DataFrame(data)

if uploaded_file is not None:
    try:
        # 인코딩 문제 방지를 위해 utf-8과 cp949 예외처리 적용
        try:
            df = pd.read_csv(uploaded_file, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(uploaded_file, encoding='cp949')
        st.sidebar.success("성공적으로 파일을 불러왔습니다!")
    except Exception as e:
        st.sidebar.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
        st.stop()
else:
    st.sidebar.info("샘플 데이터를 사용하여 앱을 데모 모드로 실행합니다.")
    df = get_sample_data()

# 2. 데이터 정제 및 컬럼 매핑 안내
st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ 컬럼 매핑 설정")
st.sidebar.caption("업로드한 파일의 컬럼명과 앱 기능 매핑")

# 파일 내 실제 컬럼 이름 가져오기
all_cols = list(df.columns)

# 사용자가 직접 컬럼을 선택할 수 있도록 사이드바에 셀렉트 박스 배치 (자동 매칭 유도)
def find_best_match(targets, choices):
    for t in targets:
        for c in choices:
            if t in c:
                return c
    return choices[0] if choices else ""

col_name = st.sidebar.selectbox("주차장명 컬럼", all_cols, index=all_cols.index(find_best_match(['명', '이름', '주차장'], all_cols)))
col_lat = st.sidebar.selectbox("위도(Latitude) 컬럼", all_cols, index=all_cols.index(find_best_match(['위도', 'lat', 'y'], all_cols)))
col_lon = st.sidebar.selectbox("경도(Longitude) 컬럼", all_cols, index=all_cols.index(find_best_match(['경도', 'lon', 'lng', 'x'], all_cols)))
col_addr = st.sidebar.selectbox("주소 컬럼", all_cols, index=all_cols.index(find_best_match(['주소', '소재지'], all_cols)))
col_fee = st.sidebar.selectbox("요금 컬럼", all_cols, index=all_cols.index(find_best_match(['요금', '금액', '비용'], all_cols)))
col_gu = st.sidebar.selectbox("자치구 컬럼", all_cols, index=all_cols.index(find_best_match(['구', '자치구', '시군구'], all_cols)))
col_free = st.sidebar.selectbox("무료여부 컬럼", all_cols, index=all_cols.index(find_best_match(['무료', '구분'], all_cols)))
col_weekend = st.sidebar.selectbox("주말운영 컬럼", all_cols, index=all_cols.index(find_best_match(['주말', '토요일', '일요일'], all_cols)))

# 필수 수치 데이터 변환
df[col_lat] = pd.to_numeric(df[col_lat], errors='coerce')
df[col_lon] = pd.to_numeric(df[col_lon], errors='coerce')
df[col_fee] = pd.to_numeric(df[col_fee], errors='coerce').fillna(0)

# 위도/경도 결측치 제거
df = df.dropna(subset=[col_lat, col_lon])

# 3. 데이터 필터링 조건 (사이드바)
st.sidebar.markdown("---")
st.sidebar.subheader("🔍 검색 필터")

# 자치구 선택
gu_list = ["전체"] + sorted(list(df[col_gu].unique()))
selected_gu = st.sidebar.selectbox("자치구를 선택하세요", gu_list)

# 요금/운영 형태 조건 필터
free_filter = st.sidebar.multiselect("무료 여부", options=df[col_free].unique(), default=df[col_free].unique())
weekend_filter = st.sidebar.multiselect("주말 운영 여부", options=df[col_weekend].unique(), default=df[col_weekend].unique())

# 데이터 필터링 적용
filtered_df = df.copy()
if selected_gu != "전체":
    filtered_df = filtered_df[filtered_df[col_gu] == selected_gu]
if free_filter:
    filtered_df = filtered_df[filtered_df[col_free].isin(free_filter)]
if weekend_filter:
    filtered_df = filtered_df[filtered_df[col_weekend].isin(weekend_filter)]

# 4. 상단 미니 대시보드 (KPI)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("검색된 주차장 수", f"{len(filtered_df)} 개")

with col2:
    avg_fee = filtered_df[col_fee].mean()
    st.metric("평균 주차 요금", f"{int(avg_fee):,} 원" if not pd.isna(avg_fee) else "0 원")

# 자치구 선택 시 가장 요금이 싼 곳 탐색
with col3:
    if not filtered_df.empty:
        cheapest_parking = filtered_df.loc[filtered_df[col_fee].idxmin()]
        cheapest_name = cheapest_parking[col_name]
        cheapest_price = cheapest_parking[col_fee]
        st.metric("최저 요금 주차장", f"{cheapest_name}", f"{int(cheapest_price):,} 원")
    else:
        st.metric("최저 요금 주차장", "데이터 없음")

st.markdown("---")

# 5. 지도 및 상세 정보 레이아웃
main_col, side_col = st.columns([2, 1])

with main_col:
    st.subheader("📍 주차장 지도 시각화")
    st.caption("마커에 마우스를 대면(Hover) 주소와 요금이 요약 표시되며, 클릭하면 길찾기 링크가 포함된 팝업이 뜹니다.")
    
    if not filtered_df.empty:
        # 지도 중심 설정 (필터링된 주차장들의 평균 위/경도)
        map_center = [filtered_df[col_lat].mean(), filtered_df[col_lon].mean()]
        m = folium.Map(location=map_center, zoom_start=13, control_scale=True)
        
        # 주차장 마커 추가
        for idx, row in filtered_df.iterrows():
            name = row[col_name]
            addr = row[col_addr]
            fee = int(row[col_fee])
            free_status = row[col_free]
            weekend_status = row[col_weekend]
            
            # 마우스 대면 나오는 툴팁 설정 (요청 기능)
            tooltip_text = f"""
            <b>{name}</b><br>
            주소: {addr}<br>
            요금: {fee:,}원 ({free_status})
            """
            
            # 클릭 시 열리는 상세 팝업 창 정보 구성
            kakao_link = f"https://map.kakao.com/link/search/{addr}"
            popup_html = f"""
            <div style="font-family: Arial, sans-serif; width: 220px;">
                <h4 style="margin: 0 0 5px 0; color: #1f77b4;">{name}</h4>
                <p style="font-size: 12px; margin: 3px 0;"><b>주소:</b> {addr}</p>
                <p style="font-size: 12px; margin: 3px 0;"><b>기본 요금:</b> {fee:,}원</p>
                <p style="font-size: 12px; margin: 3px 0;"><b>주말 운영:</b> {weekend_status}</p>
                <hr style="margin: 8px 0;">
                <a href="{kakao_link}" target="_blank" style="display: inline-block; background-color: #fee500; color: #3c1e1e; padding: 5px 10px; border-radius: 4px; text-decoration: none; font-size: 11px; font-weight: bold;">카카오맵 길찾기 ↗</a>
            </div>
            """
            popup = folium.Popup(popup_html, max_width=250)
            
            # 요금에 따라 마커 색상 구분하기 (최저가 혹은 무료는 녹색, 나머지는 파란색)
            if fee == 0:
                marker_color = 'green'
            elif not filtered_df.empty and fee == filtered_df[col_fee].min():
                marker_color = 'lightgreen'
            else:
                marker_color = 'blue'
                
            folium.Marker(
                location=[row[col_lat], row[col_lon]],
                popup=popup,
                tooltip=tooltip_text,
                icon=folium.Icon(color=marker_color, icon='info-sign')
            ).add_to(m)
            
        # Streamlit 화면에 folium 지도 렌더링
        st_folium(m, width="100%", height=500)
    else:
        st.warning("선택 조건에 맞는 주차장 데이터가 존재하지 않습니다.")

with side_col:
    st.subheader("💵 자치구 최저가 TOP 5")
    if not filtered_df.empty:
        # 요금 기준 오름차순 정렬 후 주요 정보만 노출
        cheap_top5 = filtered_df[[col_name, col_fee, col_addr, col_weekend]].sort_values(by=col_fee).head(5)
        
        # 보기 좋게 포맷팅된 데이터프레임 노출
        cheap_top5_display = cheap_top5.rename(columns={
            col_name: "주차장명",
            col_fee: "요금(원)",
            col_addr: "주소",
            col_weekend: "주말운영"
        })
        st.dataframe(cheap_top5_display, use_container_width=True, hide_index=True)
        
        # 부가 안내 정보
        st.info("💡 **팁**: 지도 위의 녹색 아이콘은 무료 주차장 혹은 현재 필터 범위 내 최저가 주차장입니다.")
    else:
        st.info("비교할 데이터가 없습니다.")
