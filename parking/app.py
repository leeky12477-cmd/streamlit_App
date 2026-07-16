import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import os

# --- 1. 페이지 기본 설정 ---
st.set_page_config(
    page_title="서울시 공영주차장 스마트 안내 가이드",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🚗 서울시 공영주차장 스마트 안내 가이드")
st.markdown("업로드한 주차장 데이터를 바탕으로 위치, 요금 및 운영 정보를 직관적으로 시각화합니다.")

# --- 2. 데이터 로드 및 전처리 함수 ---
@st.cache_data
def load_data(file_source):
    try:
        # CP949 혹은 UTF-8 호환성을 위해 encoding 설정
        df = pd.read_csv(file_source, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(file_source, encoding='cp949')
    
    # 위도, 경도 결측치 제거 및 숫자 변환
    df = df.dropna(subset=['위도', '경도'])
    df['위도'] = pd.to_numeric(df['위도'], errors='coerce')
    df['경도'] = pd.to_numeric(df['경도'], errors='coerce')
    df = df.dropna(subset=['위도', '경도'])
    
    # 자치구 컬럼 생성 (주소에서 첫 번째 단어 추출 후 '구'로 끝나는지 확인)
    def extract_gu(address):
        if pd.isna(address):
            return "기타"
        parts = str(address).split()
        for part in parts:
            if part.endswith('구'):
                return part
        return "기타"
    
    df['자치구'] = df['주소'].apply(extract_gu)
    
    # 요금 관련 결측치 보완 및 정수 변환
    df['기본 주차 요금'] = pd.to_numeric(df['기본 주차 요금'], errors='coerce').fillna(0).astype(int)
    df['기본 주차 시간(분 단위)'] = pd.to_numeric(df['기본 주차 시간(분 단위)'], errors='coerce').fillna(0).astype(int)
    df['추가 단위 요금'] = pd.to_numeric(df['추가 단위 요금'], errors='coerce').fillna(0).astype(int)
    df['추가 단위 시간(분 단위)'] = pd.to_numeric(df['추가 단위 시간(분 단위)'], errors='coerce').fillna(0).astype(int)
    
    return df

# --- 3. 데이터 입력 소스 설정 (파일 업로드 및 기본 파일 사용) ---
uploaded_file = st.sidebar.file_uploader("📂 주차장 CSV 파일 업로드", type=["csv"])

# 기본 제공된 파일의 경로 (업로드하지 않았을 때 백업으로 사용)
DEFAULT_FILE_PATH = "서울시 공영주차장 안내 정보.csv"

raw_df = None
if uploaded_file is not None:
    raw_df = load_data(uploaded_file)
    st.sidebar.success("성공적으로 업로드된 파일을 로드했습니다!")
elif os.path.exists(DEFAULT_FILE_PATH):
    raw_df = load_data(DEFAULT_FILE_PATH)
    st.sidebar.info("기본 내장된 서울시 주차장 데이터를 사용 중입니다.")
else:
    st.warning("👉 좌측 사이드바에서 서울시 공영주차장 CSV 파일을 업로드해 주세요!")
    st.stop()

# --- 4. 필터 및 검색 사이드바 UI ---
st.sidebar.header("🔍 상세 필터")

# 자치구 필터 (요구사항)
gu_list = sorted([gu for gu in raw_df['자치구'].unique() if gu != "기타"])
selected_gu = st.sidebar.selectbox("📍 자치구 선택", ["전체"] + gu_list)

# 유/무료 및 주차장 종류 필터 (추천 기능)
pay_types = raw_df['유무료구분명'].dropna().unique()
selected_pay = st.sidebar.multiselect("💵 유/무료 구분", pay_types, default=list(pay_types))

parking_types = raw_df['주차장 종류명'].dropna().unique()
selected_park_type = st.sidebar.multiselect("🅿️ 주차장 종류", parking_types, default=list(parking_types))

# 데이터 필터링 적용
df_filtered = raw_df.copy()
if selected_gu != "전체":
    df_filtered = df_filtered[df_filtered['자치구'] == selected_gu]
if selected_pay:
    df_filtered = df_filtered[df_filtered['유무료구분명'].isin(selected_pay)]
if selected_park_type:
    df_filtered = df_filtered[df_filtered['주차장 종류명'].isin(selected_park_type)]

# --- 5. 자치구별 가장 요금이 싼 곳 분석 (요구사항) ---
st.subheader("🏆 이 지역에서 가장 저렴한 주차장")
gu_context = selected_gu if selected_gu != "전체" else "서울시 전체"

# 기본 주차요금이 존재하는 곳(유료 주차장 중 요금이 0원보다 큰 곳)을 기준으로 비교
paid_parks = df_filtered[df_filtered['기본 주차 요금'] > 0]

if not paid_parks.empty:
    # 5분당 요금으로 환산하여 공정한 비교 수행 (요금 / 시간 * 5)
    paid_parks['5분당_환산요금'] = (paid_parks['기본 주차 요금'] / paid_parks['기본 주차 시간(분 단위)']) * 5
    cheapest_park = paid_parks.loc[paid_parks['5분당_환산요금'].idxmin()]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="🥇 최저가 주차장명", value=cheapest_park['주차장명'])
    with col2:
        st.metric(label="⏱️ 기본 요금 정보", value=f"{cheapest_park['기본 주차 시간(분 단위)']}분당 {cheapest_park['기본 주차 요금']:,}원")
    with col3:
        st.metric(label="🗺️ 주소", value=cheapest_park['주소'])
else:
    st.info(f"💡 현재 필터 조건(무료 주차장 포함 등) 내에 비교 가능한 유료 주차장이 없습니다.")

st.markdown("---")

# --- 6. 지도 시각화 (요구사항: 마우스 오버 시 정보 툴팁 및 클릭 시 팝업) ---
st.subheader("🗺️ 주차장 위치 시각화 지도")
st.caption("📍 마커에 마우스를 올리면(Hover) 주소와 요금이 요약 표시되고, 클릭하면 더 상세한 운영 시간 및 주말 정보가 표시됩니다.")

if not df_filtered.empty:
    # 선택된 자치구 기준으로 지도 중심 설정
    center_lat = df_filtered['위도'].mean()
    center_lng = df_filtered['경도'].mean()
    
    # 지도 생성
    m = folium.Map(location=[center_lat, center_lng], zoom_start=13 if selected_gu != "전체" else 11)
    
    # 성능 및 시각적 직관성을 위해 최대 150개 마커만 지도에 표시 (과도한 렉 방지)
    display_limit = 150
    display_df = df_filtered.head(display_limit)
    
    if len(df_filtered) > display_limit:
        st.warning(f"⚠️ 검색 결과가 너무 많아 상위 {display_limit}개의 주차장만 지도에 표시합니다. 사이드바 필터를 이용해 범위를 좁혀보세요.")

    for idx, row in display_df.iterrows():
        # 마우스 호버 시 보여줄 툴팁 구성 (요소: 주소, 요금)
        tooltip_text = f"""
        <strong>🏢 {row['주차장명']}</strong><br>
        📍 주소: {row['주소']}<br>
        💵 기본요금: {row['기본 주차 시간(분 단위)']}분 / {int(row['기본 주차 요금']):,}원 (추가: {row['추가 단위 시간(분 단위)']}분당 {int(row['추가 단위 요금']):,}원)
        """
        
        # 클릭 시 보여줄 상세 팝업 구성 (무료 여부, 야간 운영, 토/공휴일 정보 포함)
        popup_html = f"""
        <div style="width:250px; font-family: sans-serif;">
            <h4 style="margin: 0 0 5px 0; color: #1f77b4;">{row['주차장명']}</h4>
            <hr style="margin: 5px 0;">
            <b>💰 유무료 구분:</b> {row['유무료구분명']}<br>
            <b>⏰ 평일 운영:</b> {row['평일 운영 시작시각(HHMM)']} ~ {row['평일 운영 종료시각(HHMM)']}<br>
            <b>📅 주말 운영:</b> {row['주말 운영 시작시각(HHMM)']} ~ {row['주말 운영 종료시각(HHMM)']}<br>
            <b>🌙 야간 무료개방:</b> {row['야간무료개방여부명']}<br>
            <b>🚩 토요일 유/무료:</b> {row['토요일 유,무료 구분명']}<br>
            <b>🎈 공휴일 유/무료:</b> {row['공휴일 유,무료 구분명']}<br>
            <b>📞 문의처:</b> {row['전화번호']}
        </div>
        """
        popup = folium.Popup(popup_html, max_width=300)
        
        # 주차장 종류에 따른 마커 색상 구분
        marker_color = 'blue' if row['유무료구분명'] == '유료' else 'green'
        
        folium.Marker(
            location=[row['위도'], row['경도']],
            popup=popup,
            tooltip=tooltip_text,
            icon=folium.Icon(color=marker_color, icon='info-sign')
        ).add_to(m)
        
    # Streamlit 화면에 지도 출력
    st_folium(m, width="100%", height=600, returned_objects=[])
else:
    st.error("❌ 필터링 조건에 부합하는 주차장 데이터가 없습니다.")

# --- 7. 전체 데이터 테이블 제공 ---
with st.expander("📊 필터링된 주차장 전체 데이터 보기"):
    st.dataframe(df_filtered[['주차장명', '주소', '총 주차면', '유무료구분명', '기본 주차 요금', '기본 주차 시간(분 단위)', '야간무료개방여부명', '전화번호']])
