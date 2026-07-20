import streamlit as st
from googleapiclient.discovery import build
import pandas as pd
import re
from datetime import datetime
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 1. 페이지 기본 설정 및 스타일
st.set_page_config(page_title="유튜브 댓글 분석기", layout="wide")
st.title("📊 유튜브 댓글 반응 및 추이 분석기")

# 외부 CSS 없이 깔끔한 마크다운 경계선 활용
st.markdown("---")

# 2. API 키 로드 (Streamlit Secrets)
if "YOUTUBE_API_KEY" in st.secrets:
    api_key = st.secrets["YOUTUBE_API_KEY"]
else:
    st.error("🔒 Streamlit Secrets에 'YOUTUBE_API_KEY'가 설정되지 않았습니다.")
    st.stop()

# 3. 유튜브 URL에서 Video ID 추출 함수
def extract_video_id(url):
    pattern = r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    if match:
        return match.group(4)
    return None

# 4. 유튜브 댓글 수집 함수
@st.cache_data(show_spinner="유튜브에서 댓글을 가져오는 중...")
def get_youtube_comments(video_id, max_comments):
    youtube = build("youtube", "v3", developerKey=api_key)
    comments = []
    
    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=min(max_comments, 100), # 한 번에 최대 100개
            textFormat="plainText"
        )
        
        while request and len(comments) < max_comments:
            response = request.execute()
            
            for item in response.get("items", []):
                snippet = item["snippet"]["topLevelComment"]["snippet"]
                text = snippet["textDisplay"]
                like_count = snippet["likeCount"]
                published_at = snippet["publishedAt"]
                
                comments.append({
                    "Comment": text,
                    "Likes": like_count,
                    "PublishedAt": published_at
                })
                
                if len(comments) >= max_comments:
                    break
                    
            # 다음 페이지가 있으면 계속 수집
            if "nextPageToken" in response and len(comments) < max_comments:
                request = youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=min(max_comments - len(comments), 100),
                    pageToken=response["nextPageToken"],
                    textFormat="plainText"
                )
            else:
                break
                
        return pd.DataFrame(comments)
    except Exception as e:
        st.error(# 🌟 Law 7 준수: 특수문자 피하고 텍스트로 대체
            f"댓글을 가져오는 중 오류가 발생했습니다. API 키나 영상 링크를 확인해주세요. 에러 내용: {e}"
        )
        return pd.DataFrame()

# 5. 사이드바 - 사용자 입력창
st.sidebar.header("🔍 설정")
video_url = st.sidebar.text_input("유튜브 영상 링크를 입력하세요:", "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
max_comments = st.sidebar.slider("분석할 댓글 개수 선택:", min_value=10, max_value=1000, value=100, step=10)

video_id = extract_video_id(video_url)

if video_id:
    # 6. 메인 화면 UI 구획화 (영상 배치)
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📺 선택한 영상")
        st.video(video_url)
        
    with col2:
        st.subheader("📈 데이터 수집 현황")
        df = get_youtube_comments(video_id, max_comments)
        if not df.empty:
            st.success(f"성공적으로 {len(df)}개의 댓글을 수집했습니다!")
            st.dataframe(df.head(5), use_container_width=True)
            
    if not df.empty:
        st.markdown("---")
        
        # 데이터 전처리 (시간대 분리)
        df['PublishedAt'] = pd.to_datetime(df['PublishedAt'])
        df['Date'] = df['PublishedAt'].dt.date
        df['Hour'] = df['PublishedAt'].dt.hour
        
        # 레이아웃 분할: 추이 및 반응도
        st.subheader("📊 댓글 통계 및 시각화")
        tab1, tab2, tab3 = st.tabs(["🕒 시간대별 추이", "❤️ 댓글 반응도", "☁️ 한글 워드클라우드"])
        
        with tab1:
            st.markdown("#### 날짜/시간별 댓글 작성 추이")
            # 날짜별 작성 추이 그래프
            trend_df = df.groupby('Date').size().reset_index(name='Count')
            fig_date = px.line(trend_df, x='Date', y='Count', title="일자별 댓글 작성 추이", labels={'Count': '댓글 수'})
            st.plotly_chart(fig_date, use_container_width=True)
            
        with tab2:
            st.markdown("#### 댓글 반응도 분석 (좋아요 수)")
            # 좋아요 수가 많은 상위 댓글
            top_liked = df.sort_values(by='Likes', ascending=False).head(5)
            fig_likes = px.bar(top_liked, x='Likes', y='Comment', orientation='h', 
                               title="가장 반응이 좋았던(좋아요가 많은) 댓글 Top 5",
                               labels={'Likes': '좋아요 수', 'Comment': '댓글 내용'})
            fig_likes.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_likes, use_container_width=True)
            
        with tab3:
            st.markdown("#### 댓글 키워드 분석")
            
            # 한글 텍스트만 정제
            raw_text = " ".join(df['Comment'].astype(str).tolist())
            korean_text = re.sub(r'[^가-힣\s]', '', raw_text) # 한글과 공백만 남김
            
            # 무의미한 단어(조사 등) 필터링용 간단한 불용어 처리
            stopwords = set(["진짜", "너무", "진짜 너무", "보고", "영상", "그냥", "완전", "대박", "유튜브", "정말", "봅니다", "좋네요"])
            words = [word for word in korean_text.split() if len(word) > 1 and word not in stopwords]
            refined_text = " ".join(words)
            
            if refined_text.strip():
                try:
                    # 폰트 경로 설정 (깃허브 루트 폴더에 업로드한 파일 이름과 일치해야 함)
                    font_path = "NanumGothic.ttf" 
                    
                    wordcloud = WordCloud(
                        font_path=font_path,
                        background_color="white",
                        width=800,
                        height=400,
                        max_words=100
                    ).generate(refined_text)
                    
                    fig, ax = plt.subplots(figsize=(10, 5))
                    ax.imshow(wordcloud, interpolation='bilinear')
                    ax.axis("off")
                    st.pyplot(fig)
                except Exception as e:
                    st.error(f"워드클라우드를 생성하는 중 오류가 발생했습니다: {e}")
                    st.info("루트 디렉토리에 'NanumGothic.ttf' 폰트 파일이 올바르게 업로드되었는지 확인해 주세요.")
            else:
                st.warning("분석할 수 있는 한글 댓글 키워드가 부족합니다.")
else:
    st.error("올바른 유튜브 링크를 입력해 주세요.")
