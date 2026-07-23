import random
import time
import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="오늘의 운세 & 멘탈 케어 🔮",
    page_icon="🌿",
    layout="centered"
)

# 2. 커스텀 CSS (세련되고 모던한 고3 감성 디자인)
st.markdown("""
    <style>
    /* 전체 배경 */
    .stApp {
        background: linear-gradient(180deg, #F8FAFC 0%, #F1F5F9 100%);
    }
    
    /* 타이틀 디자인 */
    .title-container {
        text-align: center;
        padding: 25px 0 15px 0;
    }
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1E293B;
        margin-bottom: 8px;
        letter-spacing: -0.5px;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #64748B;
        font-weight: 500;
    }

    /* 첫 화면 안내 카드 */
    .intro-card {
        background: white;
        border-radius: 20px;
        padding: 28px;
        text-align: center;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.05);
        border: 1px solid #E2E8F0;
        margin-bottom: 25px;
    }
    .intro-badge {
        display: inline-block;
        background-color: #F1F5F9;
        color: #334155;
        font-weight: 700;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        margin-bottom: 14px;
        letter-spacing: 0.5px;
    }

    /* 결과 메인 카드 */
    .fortune-card {
        background: white;
        border-radius: 24px;
        padding: 32px;
        text-align: center;
        box-shadow: 0 15px 30px -10px rgba(0, 0, 0, 0.06);
        border: 1px solid #E2E8F0;
        margin-bottom: 25px;
    }
    .result-emoji {
        font-size: 4.5rem;
        line-height: 1;
        margin-bottom: 16px;
    }
    .result-status {
        font-size: 2rem;
        font-weight: 800;
        color: #0F172A;
        margin-bottom: 6px;
    }
    .stars {
        font-size: 1.3rem;
        color: #F59E0B;
        margin-bottom: 20px;
    }
    .summary-text {
        font-size: 1.05rem;
        line-height: 1.75;
        color: #334155;
        background-color: #F8FAFC;
        padding: 20px;
        border-radius: 16px;
        border-left: 4px solid #475569;
        text-align: left;
    }

    /* 행운의 요소 박스 */
    .lucky-box {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 18px 12px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
    }
    .lucky-title {
        font-size: 0.85rem;
        color: #64748B;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .lucky-value {
        font-size: 1.05rem;
        color: #0F172A;
        font-weight: 700;
    }

    /* 힐링 메시지 카드 */
    .quote-box {
        background: #F8FAFC;
        border-radius: 16px;
        padding: 22px;
        text-align: center;
        font-size: 1.05rem;
        color: #334155;
        font-weight: 600;
        border: 1px solid #E2E8F0;
        margin-top: 15px;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 타이틀 영역
st.markdown("""
    <div class='title-container'>
        <div class='main-title'>🌿 오늘의 운세 & 멘탈 케어</div>
        <div class='sub-title'>오늘 하루, 당신의 페이스를 찾아줄 운명의 메시지</div>
    </div>
""", unsafe_allow_html=True)

st.write("")

# 세션 상태 초기화 (결과 화면 전환용)
if "drawn" not in st.session_state:
    st.session_state.drawn = False

# ----------------------------------------------------
# 화면 1: 첫 화면 (차분하고 깔끔한 입력 폼)
# ----------------------------------------------------
if not st.session_state.drawn:
    st.markdown("""
        <div class='intro-card'>
            <div class='intro-badge'>🔮 DAILY FOCUS</div>
            <h3 style='margin-top:0; color:#0F172A; font-size:1.35rem;'>오늘 나에게 필요한 리듬과 흐름을 확인해보세요</h3>
            <p style='color:#64748B; font-size:0.95rem; margin-bottom:0; line-height:1.6;'>
                궁금한 영역과 정보를 선택하고 <b>[운세 카드 확인하기]</b>를 누르면<br>
                오늘의 집중도 흐름부터 유용한 행동 팁까지 차분하게 정리해 드립니다.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 입력 컬럼 구성
    col_a, col_b = st.columns(2)
    
    with col_a:
        category = st.selectbox(
            "1️⃣ 확인할 운세 분야",
            ["종합운 🌟", "학업/집중운 📚", "컨디션/건강운 🌿", "재물/소비운 💰", "대인관계운 🤝"]
        )
    
    with col_b:
        zodiac = st.selectbox(
            "2️⃣ 별자리 선택",
            ["물병자리 ♒", "물고기자리 ♓", "양자리 ♈", "황소자리 ♉", 
             "쌍둥이자리 ♊", "게자리 ♋", "사자자리 ♌", "처녀자리 ♍", 
             "천칭자리 ♎", "전갈자리 ♏", "사수자리 ♐", "염소자리 ♑"]
        )

    st.write("")
    st.write("")

    # 버튼 클릭 시 운세 뽑기 진행
    if st.button("🔮 오늘의 운세 카드 확인하기", use_container_width=True, type="primary"):
        st.session_state.selected_category = category
        st.session_state.selected_zodiac = zodiac
        st.session_state.drawn = True
        st.rerun()

# ----------------------------------------------------
# 화면 2: 결과 화면 (고3 맞춤형 수험/일상 조언)
# ----------------------------------------------------
else:
    # 수험생 및 고등학생 눈높이에 맞춘 운세 데이터
    fortunes = {
        "대길 (大吉)": {
            "score": 98,
            "stars": "⭐⭐⭐⭐⭐",
            "emoji": "🎯",
            "summary": "집중력과 몰입도가 최상에 달하는 날입니다. 그동안 차근차근 쌓아온 노력이 비로소 실체적인 성과나 확실한 이해로 이어지는 절호의 타이밍입니다.",
            "dos": [
                "취약했던 단원이나 가장 까다로웠던 과목의 고난도 문제에 적극적으로 도전해보세요.",
                "오늘 세운 학습 계획이나 목표 스케줄을 끝까지 완수하여 성취감을 극대화하세요.",
                "스스로의 가능성을 믿고 자신감 있게 목표 점수를 높여 잡는 배짱을 가지세요."
            ],
            "donts": [
                "운이 좋다고 해서 방심하거나 계획했던 공부 스케줄을 중간에 포기하는 일.",
                "주변의 사소한 잡음이나 쓸데없는 논쟁에 휘말려 귀중한 몰입 시간을 빼앗기는 것.",
                "타인의 부정적인 한마디에 흔들려 본인의 페이스를 스스로 무너뜨리는 행동."
            ]
        },
        "길 (吉)": {
            "score": 85,
            "stars": "⭐⭐⭐⭐☆",
            "emoji": "🌱",
            "summary": "안정적인 흐름 속에서 계획한 목표를 착실히 이행할 수 있는 날입니다. 큰 기복 없이 꾸준한 페이스를 유지하며 내실을 다지기에 적합합니다.",
            "dos": [
                "오답 노트를 재점검하거나 개념을 완벽하게 내 것으로 만드는 복습에 집중하세요.",
                "공부 중간중간 5분씩 가벼운 스트레칭으로 목과 어깨의 피로를 풀어주세요.",
                "수면 패턴과 식사 시간을 일정하게 유지해 차분한 컨디션을 유지해 보세요."
            ],
            "donts": [
                "갑작스럽게 불안해진다고 해서 학습 방법을 이리저리 바꾸며 혼란을 자초하는 것.",
                "스마트폰을 곁에 두고 습관적으로 숏폼 영상이나 SNS를 확인하며 집중력을 깨는 일.",
                "카페인을 과도하게 섭취하며 무리하게 밤샘 공부를 강행하는 행동."
            ]
        },
        "소길 (小吉)": {
            "score": 70,
            "stars": "⭐⭐⭐☆☆",
            "emoji": "☕",
            "summary": "무난하고 평범하지만 소소한 성취를 느낄 수 있는 하루입니다. 무리한 목표보다는 오늘 주어진 할 일에만 담담하게 최선을 다하는 것이 효율적입니다.",
            "dos": [
                "오늘 당장 해야 할 암기 분량이나 핵심 문제 풀이 등 작고 명확한 목표부터 처리하세요.",
                "공부 환경이나 책상 위를 말끔히 정리하여 시각적인 산만함을 줄여보세요.",
                "나에게 딱 맞는 차분한 백색소음이나 집중용 음악을 활용해 몰입감을 높이세요."
            ],
            "donts": [
                "남들의 진도나 문제집 회독 수에 연연하며 스스로에게 조급함을 부추기는 것.",
                "잘 풀리지 않는 한 문제에 몇 시간씩 집착하여 전체 스케줄을 망치는 행동.",
                "컨디션이 약간 떨어졌을 때 자신을 채찍질하며 과도한 자책에 빠지는 일."
            ]
        },
        "평 (平)": {
            "score": 55,
            "stars": "⭐⭐☆☆☆",
            "emoji": "🔋",
            "summary": "에너지 소모가 크고 약간의 집중력 저하가 찾아올 수 있는 날입니다. 성과를 급하게 내려고 하기보다는 컨디션 조절과 멘탈 관리에 신경 쓰세요.",
            "dos": [
                "새로운 개념을 나가기보다 이전에 배운 내용을 가볍게 읽어보는 부담 없는 공부를 하세요.",
                "퇴근 후/하교 후 일찍 잠자리에 들어 그동안 누적된 체력적 피로를 회복하세요.",
                "따뜻한 물을 자주 마시고 정돈된 장소에서 잠시 눈을 감고 휴식을 취하세요."
            ],
            "donts": [
                "컨디션이 저하된 상태에서 억지로 집중하려다 불필요한 실수를 반복하는 것.",
                "중요한 진로 결정이나 시험 전략에 대해 혼자서 조급하게 결론을 내리는 행위.",
                "친구들이나 주변 사람들의 말에 지나치게 민감하게 반응하여 감정을 소모하는 일."
            ]
        },
        "흉 (凶)": {
            "score": 40,
            "stars": "⭐☆☆☆☆",
            "emoji": "🛡️",
            "summary": "마음이 다소 불안하거나 사소한 오해가 생길 수 있는 조심스러운 하루입니다. 오늘은 무리한 도전을 피하고 자신을 보호하는 방어적인 자세가 필요합니다.",
            "dos": [
                "말이나 행동을 하기 전 한 번 더 생각하는 신중하고 차분한 태도를 유지하세요.",
                "좋아하는 영양제나 따뜻한 음료를 챙겨 먹으며 체력과 면역력을 케어하세요.",
                "마음이 복잡할 때는 오늘 하루 고생한 나 자신에게 격려의 혼잣말을 건네보세요."
            ],
            "donts": [
                "감정 상태가 좋지 않을 때 타인에게 홧김에 까칠한 언행을 내뱉는 행동.",
                "지나간 시험 결과나 과거의 실수를 자꾸 되새기며 자존감을 깎아내리는 일.",
                "늦은 시간까지 스마트폰을 보며 불면증과 피로를 유발하는 습관."
            ]
        }
    }

    # 고3 수험생 일상에 꼭 필요한 현실적 행운 아이템
    lucky_colors = ["딥 네이비 🌌", "포레스트 그린 🌲", "샤콜 그레이 📓", "아이보리 화이트 🤍", "스카이 블루 ☁️"]
    lucky_items = [
        "노이즈 캔슬링 이어폰 🎧", 
        "스톱워치/타이머 ⏱️", 
        "블루라이트 차단 안경 👓", 
        "졸음 깨는 인공눈물 💧", 
        "형광펜과 포스트잇 🖊️", 
        "텀블러에 담긴 따뜻한 차 🍵", 
        "비타민 C 영양제 💊"
    ]
    lucky_numbers = [3, 7, 12, 24, 88, 99]
    healing_quotes = [
        "“묵묵히 걸어가는 오늘의 한 걸음이 모여, 결국 당신이 바라는 목적지에 도달하게 할 것입니다.”",
        "“지금 당장 눈에 보이지 않더라도, 당신이 쏟은 노력은 물밑에서 차곡차곡 쌓이고 있습니다.”",
        "“남들과의 비교는 내려놓으세요. 당신은 오직 어제의 자신보다만 발전하면 충분합니다.”",
        "“지치고 힘든 순간이 온다는 것은, 당신이 목표를 향해 진심으로 달리고 있다는 증거입니다.”",
        "“오늘 하루도 정말 고생 많았습니다. 당신은 생각보다 훨씬 더 강하고 잘해내고 있습니다.”"
    ]

    # 로딩 애니메이션 효과
    with st.spinner(f"🌿 {st.session_state.selected_zodiac}의 리듬에 맞춰 {st.session_state.selected_category} 카드를 분석하는 중..."):
        time.sleep(0.7)

    # 랜덤 결과 추출
    status_key = random.choice(list(fortunes.keys()))
    res = fortunes[status_key]
    selected_do = random.choice(res["dos"])
    selected_dont = random.choice(res["donts"])
    color = random.choice(lucky_colors)
    item = random.choice(lucky_items)
    number = random.choice(lucky_numbers)
    quote = random.choice(healing_quotes)

    cat_name = st.session_state.selected_category.split()[0]

    # (1) 메인 운세 카드
    st.markdown(f"""
        <div class='fortune-card'>
            <div class='result-emoji'>{res['emoji']}</div>
            <div class='result-status'>[{cat_name}] {status_key}</div>
            <div class='stars'>{res['stars']}</div>
            <div class='summary-text'>💡 <b>오늘의 리듬 분석:</b><br>{res['summary']}</div>
        </div>
    """, unsafe_allow_html=True)

    # (2) 운세 지수 (프로그레스 바)
    st.write(f"📊 **오늘의 {cat_name} 집중/컨디션 지수: {res['score']}점**")
    st.progress(res['score'] / 100)
    st.write("")

    # (3) Action Item (추천 행동 / 주의할 행동)
    col1, col2 = st.columns(2)
    with col1:
        st.success(f"**⭕ 오늘 실천하면 좋은 팁**\n\n{selected_do}")
    with col2:
        st.error(f"**❌ 오늘 주의해야 할 점**\n\n{selected_dont}")

    st.write("")

    # (4) 행운 요소 (현실적인 수험/일상 아이템 배치)
    st.subheader("🍀 오늘의 행운 포인트")
    lcol1, lcol2, lcol3 = st.columns(3)
    with lcol1:
        st.markdown(f"<div class='lucky-box'><div class='lucky-title'>🎨 행운의 컬러</div><div class='lucky-value'>{color}</div></div>", unsafe_allow_html=True)
    with lcol2:
        st.markdown(f"<div class='lucky-box'><div class='lucky-title'>🎒 행운의 아이템</div><div class='lucky-value'>{item}</div></div>", unsafe_allow_html=True)
    with lcol3:
        st.markdown(f"<div class='lucky-box'><div class='lucky-title'>🔢 행운의 숫자</div><div class='lucky-value'><b>{number}</b></div></div>", unsafe_allow_html=True)

    # (5) 힐링/동기부여 메시지
    st.markdown(f"<div class='quote-box'>💬 멘탈 케어 메시지<br><br>{quote}</div>", unsafe_allow_html=True)

    st.write("")

    # (6) 다시 뽑기 버튼
    if st.button("🔄 다른 운세 다시 확인하기", use_container_width=True):
        st.session_state.drawn = False
        st.rerun()
