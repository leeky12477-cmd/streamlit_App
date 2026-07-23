import random
import time
import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="오늘의 운세 뽑기 🔮",
    page_icon="🎲",
    layout="centered"
)

# 2. 커스텀 CSS (깔끔하고 모던한 모노/파스텔 스타일)
st.markdown("""
    <style>
    /* 전체 배경 */
    .stApp {
        background: linear-gradient(180deg, #F8FAFC 0%, #EDF2F7 100%);
    }
    
    /* 타이틀 디자인 */
    .title-container {
        text-align: center;
        padding: 20px 0 10px 0;
    }
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1A202C;
        margin-bottom: 6px;
        letter-spacing: -0.5px;
    }
    .sub-title {
        font-size: 1rem;
        color: #4A5568;
        font-weight: 500;
    }

    /* 첫 화면 카드 */
    .intro-card {
        background: white;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.05);
        border: 1px solid #E2E8F0;
        margin-bottom: 20px;
    }
    .intro-badge {
        display: inline-block;
        background-color: #EDF2F7;
        color: #2D3748;
        font-weight: 700;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        margin-bottom: 10px;
    }

    /* 결과 메인 카드 */
    .fortune-card {
        background: white;
        border-radius: 24px;
        padding: 28px;
        text-align: center;
        box-shadow: 0 15px 25px -5px rgba(0, 0, 0, 0.06);
        border: 1px solid #E2E8F0;
        margin-bottom: 20px;
    }
    .result-emoji {
        font-size: 4.2rem;
        line-height: 1;
        margin-bottom: 12px;
    }
    .result-status {
        font-size: 2rem;
        font-weight: 800;
        color: #1A202C;
        margin-bottom: 6px;
    }
    .stars {
        font-size: 1.2rem;
        color: #ECC94B;
        margin-bottom: 16px;
    }
    .summary-text {
        font-size: 1.05rem;
        line-height: 1.7;
        color: #2D3748;
        background-color: #F7FAFC;
        padding: 18px;
        border-radius: 16px;
        border-left: 4px solid #4A5568;
        text-align: left;
    }

    /* 행운 요소 박스 */
    .lucky-box {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 16px 8px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
    }
    .lucky-title {
        font-size: 0.8rem;
        color: #718096;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .lucky-value {
        font-size: 1rem;
        color: #1A202C;
        font-weight: 700;
    }

    /* 음악 추천 박스 */
    .music-box {
        background: #F0F9FF;
        border-radius: 16px;
        padding: 18px;
        text-align: center;
        border: 1px solid #BAE6FD;
        margin-top: 15px;
        color: #0369A1;
    }

    /* 한마디 메시지 박스 */
    .quote-box {
        background: #F7FAFC;
        border-radius: 16px;
        padding: 18px;
        text-align: center;
        font-size: 1rem;
        color: #2D3748;
        font-weight: 600;
        border: 1px solid #E2E8F0;
        margin-top: 15px;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 세션 상태 초기화 (결과 화면 및 횟수 제한용)
if "drawn" not in st.session_state:
    st.session_state.drawn = False
if "count" not in st.session_state:
    st.session_state.count = 0

MAX_DRAWS = 3 # 하루 최대 뽑기 횟수 제한

# 4. 타이틀 영역
st.markdown("""
    <div class='title-container'>
        <div class='main-title'>🎲 오늘의 운세 뽑기</div>
        <div class='sub-title'>오늘 하루, 나를 기다리는 기분 좋은 운세를 확인해보세요!</div>
    </div>
""", unsafe_allow_html=True)

st.write("")

# ----------------------------------------------------
# 화면 1: 첫 화면 (카테고리 선택 및 횟수 제한 안내)
# ----------------------------------------------------
if not st.session_state.drawn:
    st.markdown(f"""
        <div class='intro-card'>
            <div class='intro-badge'>🔮 TODAY's FORTUNE</div>
            <h3 style='margin-top:0; color:#1A202C; font-size:1.25rem;'>어떤 운세가 궁금하신가요?</h3>
            <p style='color:#718096; font-size:0.9rem; margin-bottom:0;'>
                카테고리를 선택하고 운세를 뽑아보세요.<br>
                <b>(남은 기회: {MAX_DRAWS - st.session_state.count} / {MAX_DRAWS}회)</b>
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 카테고리 선택
    category = st.selectbox(
        "👉 카테고리를 선택해주세요",
        ["종합운 🌟", "금전운 💰", "학업/시험운 📚", "재물운 💎", "연애/대인관계운 💕"]
    )

    st.write("")

    # 횟수 제한 로직
    if st.session_state.count >= MAX_DRAWS:
        st.warning("⚠️ 오늘의 기회를 모두 사용하셨습니다! 내일 다시 뽑아주세요. 🍀")
        st.button("🎲 오늘의 운세 뽑기", disabled=True, use_container_width=True)
    else:
        if st.button("🎲 오늘의 운세 뽑기!", use_container_width=True, type="primary"):
            st.session_state.selected_category = category
            st.session_state.count += 1
            st.session_state.drawn = True
            st.rerun()

# ----------------------------------------------------
# 화면 2: 결과 화면 (긁기 연출 + BGM 추천 포함)
# ----------------------------------------------------
else:
    # 운세 데이터
    fortunes = {
        "대길 (大吉)": {
            "score": 98,
            "stars": "⭐⭐⭐⭐⭐",
            "emoji": "🥳",
            "summary": "뭘 해도 이상하게 잘 풀리는 날입니다! 망설이던 일이 있다면 일단 지르고 보세요. 의외의 대박이나 소소한 횡재수가 기다리고 있습니다.",
            "dos": [
                "평소 사고 싶었던 거나 먹고 싶었던 게 있다면 자신 있게 질러보기!",
                "좋아하는 사람이나 친구한테 부담 없이 먼저 툭 연락해보기.",
                "오늘만큼은 '되면 되고 말고!' 하는 당당한 마음가짐으로 행동하기."
            ],
            "donts": [
                "다 잘 되고 있는데 사서 걱정하고 괜히 눈치 보기.",
                "좋은 기회가 왔는데 '내가 할 수 있을까?' 하고 주춤거리는 것.",
                "오늘 할 수 있는 재미있는 일들을 내일로 미루기."
            ]
        },
        "길 (吉)": {
            "score": 85,
            "stars": "⭐⭐⭐⭐☆",
            "emoji": "😎",
            "summary": "전반적으로 기분 좋은 일들이 소소하게 터지는 날입니다. 무난하면서도 보람찬 하루를 보낼 수 있는 아주 매끄러운 흐름이에요.",
            "dos": [
                "맛있는 디저트나 최애 음료 한 잔으로 스스로에게 소소한 포상 주기.",
                "평소보다 한 걸음 여유 있게 움직이며 주변 분위기 즐기기.",
                "길 가다 마주치는 맛집이나 관심 있는 장소 무작정 들어가보기."
            ],
            "donts": [
                "괜히 분위기에 휩쓸려 내 스타일도 아닌 일에 억지로 끼어들기.",
                "약속 시간 간당간당하게 뛰어가다가 소지품 떨어뜨리기.",
                "남들이 뭐라 하든 말든 귀 닫고 내 마이웨이 유지 안 하기."
            ]
        },
        "소길 (小吉)": {
            "score": 70,
            "stars": "⭐⭐⭐☆☆",
            "emoji": "🙂",
            "summary": "크게 특별할 건 없지만 평화롭고 잔잔한 하루입니다. 커다란 이벤트를 기대하기보다는 무탈한 일상의 소확행을 만끽하세요.",
            "dos": [
                "최애 음악 들으면서 기분 좋게 멍때리는 시간 갖기.",
                "책상이나 가방 속 정리하면서 불필요한 물건 싹 버리기.",
                "오늘 해야 할 일 딱 필요한 만큼만 깔끔하게 끝내고 쉬기."
            ],
            "donts": [
                "남들의 인스타나 SNS 보면서 '나만 심심한가?' 비교하기.",
                "남들의 사소한 오지랖이나 신경 쓰이는 말에 과하게 반응하기.",
                "체력도 없는데 억지로 무리한 스케줄 잡아서 피로 누적시키기."
            ]
        },
        "평 (平)": {
            "score": 55,
            "stars": "⭐⭐☆☆☆",
            "emoji": "😐",
            "summary": "잔잔한 호수 같은 날입니다. 큰 변화나 도전을 시도하기보다는 기존의 상태를 잘 유지하며 평정심을 지키는 게 가장 좋습니다.",
            "dos": [
                "퇴근이나 하교 후에 내가 제일 좋아하는 영상 보면서 푹 쉬기.",
                "따뜻한 물로 샤워하고 평소보다 일찍 침대에 눕기.",
                "마음 편해지는 나만의 루틴대로 차분하게 하루 마치기."
            ],
            "donts": [
                "잘 모르는 일에 홧김에 큰돈 쓰거나 충동적으로 결정 내리기.",
                "피곤한 상태에서 억지로 밤새거나 컨디션 갉아먹기.",
                "상대방 말에 별 뜻 없는데 혼자 깊게 생각해서 꼬아 듣기."
            ]
        },
        "흉 (凶)": {
            "score": 40,
            "stars": "⭐☆☆☆☆",
            "emoji": "🫠",
            "summary": "오늘은 약간 '억울한 일'이나 사소한 해프닝이 생길 수 있는 날입니다. 그냥 '오늘 액땜했다!' 치고 부드럽게 넘겨버리는 대범함이 필요해요.",
            "dos": [
                "한 귀로 듣고 한 귀로 흘리는 스킬 적극 활용하기.",
                "맛있는 거 먹으면서 오늘 하루 고생한 나 자신 토닥여주기.",
                "스마트폰 멀리하고 일찍 잠자리에 들어서 빠르게 하루 리셋하기."
            ],
            "donts": [
                "욱하는 마음에 홧김에 한마디 쏘아붙였다가 일 크게 키우기.",
                "길 가다 발 걸리거나 계단 내려갈 때 스마트폰만 쳐다보기.",
                "별것도 아닌 일에 하루 종일 기분 망치고 끙끙 앓기."
            ]
        }
    }

    # 행운 요소 및 추천 음악 데이터
    lucky_colors = ["로즈 핑크 🌸", "포레스트 그린 🌲", "미드나잇 블루 🌙", "버터 옐로우 🧈", "아이보리 화이트 🤍"]
    lucky_places = ["햇살 잘 드는 카페 ☕", "아늑한 내 방 침대 🛌", "조용한 공원 산책로 🌿", "자주 가는 편의점 🏪", "서점이나 소품샵 📚"]
    lucky_numbers = [3, 7, 12, 21, 77, 99]
    
    music_list = [
        "🎧 신나는 시티팝 (드라이브하는 기분 내기)",
        "🎧 잔잔한 로파이(Lo-Fi) 비트 (힐링이 필요할 때)",
        "🎧 청량한 밴드 사운드 (텐션 올리고 싶을 때)",
        "🎧 따뜻한 아쿠스틱 기타 곡 (마음 정리가 필요할 때)",
        "🎧 신나는 K-POP 플레이리스트 (에너지 충전!)"
    ]
    
    healing_quotes = [
        "“오늘 하루 정도는 대충 살아도 세상은 잘 돌아갑니다.”",
        "“뜻밖의 행운은 원래 기대 안 하고 있을 때 툭 찾아오는 법이에요.”",
        "“어차피 지나갈 하루라면, 최대한 웃으면서 즐겁게 보내버립시다!”",
        "“남들 시선 상관없이 오늘 내가 제일 기분 좋은 게 정답입니다.”",
        "“오늘 어떤 일이 있든, 결국엔 전부 다 잘 될 거니까 걱정 마세요.”"
    ]

    # 로딩 연출
    with st.spinner("🔮 운세 복권을 인쇄하는 중..."):
        time.sleep(0.5)

    # 랜덤 결과 추출
    status_key = random.choice(list(fortunes.keys()))
    res = fortunes[status_key]
    selected_do = random.choice(res["dos"])
    selected_dont = random.choice(res["donts"])
    color = random.choice(lucky_colors)
    place = random.choice(lucky_places)
    number = random.choice(lucky_numbers)
    bgm = random.choice(music_list)
    quote = random.choice(healing_quotes)

    cat_name = st.session_state.selected_category.split()[0]

    # (1) 복권 긁기 연출 (Expander 클릭 연출)
    st.info("🪙 **아래 복권을 클릭해서 오늘의 운세를 긁어보세요!**")
    
    with st.expander("✨ [클릭] 오늘의 운세 복권 긁기 ✨", expanded=False):
        # 복권을 열면 나오는 결과
        st.markdown(f"""
            <div class='fortune-card'>
                <div class='result-emoji'>{res['emoji']}</div>
                <div class='result-status'>[{cat_name}] {status_key}</div>
                <div class='stars'>{res['stars']}</div>
                <div class='summary-text'>💡 <b>오늘의 한줄 요약:</b><br>{res['summary']}</div>
            </div>
        """, unsafe_allow_html=True)

        # 운세 지수
        st.write(f"📊 **오늘의 {cat_name} 지수: {res['score']}점**")
        st.progress(res['score'] / 100)
        st.write("")

        # Action Item (해볼 것 / 피할 것)
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"**⭕ 오늘은 이렇게 해보세요!**\n\n👉 {selected_do}")
        with col2:
            st.error(f"**❌ 오늘은 이건 피하세요!**\n\n👉 {selected_dont}")

        st.write("")

        # 행운 요소
        st.subheader("🍀 오늘의 행운 포인트")
        lcol1, lcol2, lcol3 = st.columns(3)
        with lcol1:
            st.markdown(f"<div class='lucky-box'><div class='lucky-title'>🎨 행운의 컬러</div><div class='lucky-value'>{color}</div></div>", unsafe_allow_html=True)
        with lcol2:
            st.markdown(f"<div class='lucky-box'><div class='lucky-title'>📍 행운의 장소</div><div class='lucky-value'>{place}</div></div>", unsafe_allow_html=True)
        with lcol3:
            st.markdown(f"<div class='lucky-box'><div class='lucky-title'>🔢 행운의 숫자</div><div class='lucky-value'><b>{number}</b></div></div>", unsafe_allow_html=True)

        # 추천 BGM 영역
        st.markdown(f"<div class='music-box'>🎵 <b>오늘 당신을 위한 BGM 추천</b><br><br>{bgm}</div>", unsafe_allow_html=True)

        # 한마디 메시지
        st.markdown(f"<div class='quote-box'>💌 오늘의 한마디<br><br>{quote}</div>", unsafe_allow_html=True)
        
        st.balloons()

    st.write("")

    # (2) 다시 뽑기 버튼 (횟수 안내 포함)
    left_draws = MAX_DRAWS - st.session_state.count
    if left_draws > 0:
        if st.button(f"🔄 다시 뽑기 (남은 기회: {left_draws}회)", use_container_width=True):
            st.session_state.drawn = False
            st.rerun()
    else:
        st.warning("⚠️ 오늘의 재뽑기 기회를 모두 사용하셨습니다.")
        if st.button("🏠 처음 화면으로 돌아가기", use_container_width=True):
            st.session_state.drawn = False
            st.rerun()
