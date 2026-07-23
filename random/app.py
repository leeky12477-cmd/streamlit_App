import random
import time
import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="신비로운 오늘의 운세 🔮",
    page_icon="✨",
    layout="centered"
)

# 2. 커스텀 CSS (화려하고 예쁜 스타일링)
st.markdown("""
    <style>
    /* 배경 및 기본 폰트 설정 */
    .stApp {
        background: linear-gradient(180deg, #F9FAFB 0%, #EEF2FF 100%);
    }
    
    /* 타이틀 애니메이션 & 디자인 */
    .title-container {
        text-align: center;
        padding: 20px 0 10px 0;
    }
    .main-title {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(90deg, #4F46E5, #7C3AED, #EC4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #4B5563;
        font-weight: 500;
    }

    /* 첫 화면 안내 카드 */
    .intro-card {
        background: white;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.1);
        border: 1px solid #E0E7FF;
        margin-bottom: 25px;
    }
    .intro-badge {
        display: inline-block;
        background-color: #EEF2FF;
        color: #4F46E5;
        font-weight: 700;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.9rem;
        margin-bottom: 12px;
    }

    /* 결과 카드 스타일 */
    .fortune-card {
        background: white;
        border-radius: 24px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.08);
        border: 2px solid #F3E8FF;
        margin-bottom: 25px;
    }
    .result-emoji {
        font-size: 5rem;
        line-height: 1;
        margin-bottom: 15px;
        filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));
    }
    .result-status {
        font-size: 2.2rem;
        font-weight: 800;
        color: #111827;
        margin-bottom: 6px;
    }
    .stars {
        font-size: 1.4rem;
        color: #F59E0B;
        margin-bottom: 20px;
    }
    .summary-text {
        font-size: 1.05rem;
        line-height: 1.7;
        color: #374151;
        background-color: #F9FAFB;
        padding: 18px 22px;
        border-radius: 16px;
        border-left: 5px solid #8B5CF6;
        text-align: left;
    }

    /* 행운의 요소 박스 */
    .lucky-box {
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 16px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .lucky-title {
        font-size: 0.85rem;
        color: #6B7280;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .lucky-value {
        font-size: 1.1rem;
        color: #1F2937;
        font-weight: 700;
    }

    /* 힐링 한마디 카드 */
    .quote-box {
        background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        font-size: 1.05rem;
        color: #92400E;
        font-weight: 600;
        border: 1px solid #FDE68A;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 타이틀 영역
st.markdown("""
    <div class='title-container'>
        <div class='main-title'>✨ 신비로운 오늘의 운세 ✨</div>
        <div class='sub-title'>당신의 하루를 환하게 밝혀줄 운명의 메시지를 확인해보세요</div>
    </div>
""", unsafe_allow_html=True)

st.write("")

# 세션 상태 초기화 (결과 화면 전환용)
if "drawn" not in st.session_state:
    st.session_state.drawn = False

# ----------------------------------------------------
# 화면 1: 뽑기 전 화면 (예쁘게 꾸며진 입력 폼)
# ----------------------------------------------------
if not st.session_state.drawn:
    st.markdown("""
        <div class='intro-card'>
            <div class='intro-badge'>🔮 TODAY's FORTUNE</div>
            <h3 style='margin-top:0; color:#1F2937;'>오늘 하루, 어떤 운이 당신을 기다리고 있을까요?</h3>
            <p style='color:#6B7280; font-size:0.95rem; margin-bottom:0;'>
                아래의 정보를 선택하고 <b>[운세 카드 뽑기]</b> 버튼을 누르면<br>
                오늘의 총평부터 행운의 아이템, 구체적인 조언까지 모두 알려드려요!
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 입력 탭/컬럼 구성
    col_a, col_b = st.columns(2)
    
    with col_a:
        category = st.selectbox(
            "1️⃣ 궁금한 운세 종류",
            ["종합운 🌟", "금전운 💰", "학업/사업운 📚", "재물운 💎", "연애운 💕"]
        )
    
    with col_b:
        zodiac = st.selectbox(
            "2️⃣ 당신의 별자리 (선택)",
            ["물병자리 ♒", "물고기자리 ♓", "양자리 ♈", "황소자리 ♉", 
             "쌍둥이자리 ♊", "게자리 ♋", "사자자리 ♌", "처녀자리 ♍", 
             "천칭자리 ♎", "전갈자리 ♏", "사수자리 ♐", "염소자리 ♑"]
        )

    st.write("")
    st.write("")

    # 버튼 클릭 시 운세 뽑기 진행
    if st.button("🔮 오늘의 운세 카드 뽑기!", use_container_width=True, type="primary"):
        st.session_state.selected_category = category
        st.session_state.selected_zodiac = zodiac
        st.session_state.drawn = True
        st.rerun()

# ----------------------------------------------------
# 화면 2: 운세 결과 화면
# ----------------------------------------------------
else:
    # 운세 데이터 정의
    fortunes = {
        "대길 (大吉)": {
            "score": 98,
            "stars": "⭐⭐⭐⭐⭐",
            "emoji": "🥳🎉",
            "summary": "손대는 일마다 놀라운 성과와 긍정적인 에너지가 가득한 최고의 날입니다! 망설이고 있던 중요한 도전이나 계획이 있다면 고민하지 말고 지금 당장 시작해보세요.",
            "dos": [
                "그동안 미뤄두었던 중요한 과제나 망설이던 연락을 오늘 바로 실행으로 옮겨보세요.",
                "자신감 있고 당당하게 의견을 표현하세요. 뜻밖의 귀인을 만나 적극적인 지원을 받을 확률이 매우 높습니다.",
                "좋아하는 사람이나 소중한 지인에게 먼저 따뜻한 커피 한 잔과 함께 마음을 전해보세요."
            ],
            "donts": [
                "스스로의 가능성을 낮게 평가하거나 불필요한 겸손으로 다가온 절호의 기회를 지나쳐버리는 것.",
                "오늘 충분히 끝낼 수 있는 일을 '내일 해야지' 하며 미루는 순간 행운의 흐름이 꺾일 수 있습니다.",
                "남들의 시선이나 평가에 너무 신경 쓰느라 본인이 진짜 원하는 바를 포기하는 행동."
            ]
        },
        "길 (吉)": {
            "score": 82,
            "stars": "⭐⭐⭐⭐☆",
            "emoji": "😊🌸",
            "summary": "차분하면서도 알찬 보람을 거둘 수 있는 매끄러운 날입니다. 꾸준히 쌓아온 노력이 빛을 발하여 주변 사람들에게 시기 대신 따뜻한 인정을 받게 됩니다.",
            "dos": [
                "평소 고마웠던 주변 사람들에게 작은 감사 인사나 정성 어린 말 한마디를 나누어보세요.",
                "점심시간이나 퇴근 후 20분 정도 가벼운 산책을 하며 맑은 공기를 마시고 기분을 전환해보세요.",
                "새롭게 관심을 갖고 있던 취미나 공부가 있다면 관련 자료를 차분히 탐색해보는 시간을 가지세요."
            ],
            "donts": [
                "주변 분위기에 휩쓸려 충동구매를 하거나 계획에 없던 과도한 지출을 진행하는 것.",
                "가까운 사이일수록 예의를 갖추지 않고 감정적으로 대화를 이끌어가는 솔직함.",
                "약속 시간에 임박해 서두르다가 중요한 소지품을 잃어버리거나 실수를 유발하는 행동."
            ]
        },
        "소길 (小吉)": {
            "score": 67,
            "stars": "⭐⭐⭐☆☆",
            "emoji": "🙂🌱",
            "summary": "큰 파도 없이 평화롭고 잔잔한 하루입니다. 커다란 대박이나 변화를 노리기보다는 일상의 소소한 행복(소확행)을 만끽하는 것이 훨씬 유리합니다.",
            "dos": [
                "책상 위나 방 안 등 내 생활 영역을 말끔히 정리정돈하여 쾌적한 환경을 만들어보세요.",
                "따뜻한 차나 좋아하는 음료 한 잔을 마시며 나만의 조용한 휴식 시간을 가져보세요.",
                "오늘 처리해야 할 작은 업무나 루틴들을 하나씩 체크리스트로 지워나가는 재미를 느끼기."
            ],
            "donts": [
                "타인의 문제나 남들의 싸움에 과도하게 오지랖을 부려 쓸데없는 감정 에너지를 낭비하는 것.",
                "몸에 무리가 가는 격렬한 운동을 갑자기 강행하거나 과도한 음주·야식을 즐기는 행동.",
                "SNS 등을 통해 스스로를 다른 사람의 화려한 모습과 비교하며 사기를 떨어뜨리는 생각."
            ]
        },
        "평 (平)": {
            "score": 50,
            "stars": "⭐⭐☆☆☆",
            "emoji": "😐☕",
            "summary": "급격한 변화보다는 현재 상태를 유연하게 유지하며 내실을 다져야 하는 무난한 하루입니다. 안정을 최우선으로 두는 것이 가장 지혜롭습니다.",
            "dos": [
                "평소 지켜오던 자신만의 일상 루틴을 묵묵히 이어나가며 제페이스를 유지하세요.",
                "퇴근/하교 후 일찍 잠자리에 들어 그동안 쌓인 컨디션 저하와 피로를 충분히 회복해보세요.",
                "마음을 편안하게 해주는 음악을 듣거나 가벼운 독서로 심신을 차분히 다스려보세요."
            ],
            "donts": [
                "잘 알지 못하는 분야에 홧김에 큰돈을 투자하거나 불확실한 계약을 급하게 진행하는 것.",
                "중요한 안건에 대해 혼자서 독단적으로 판단하고 유별나게 고집을 부리는 행위.",
                "컨디션이 저하된 상태에서 억지로 무리한 밤샘 작업이나 과로를 강행하는 것."
            ]
        },
        "흉 (凶)": {
            "score": 30,
            "stars": "⭐☆☆☆☆",
            "emoji": "🥺🌧️",
            "summary": "컨디션이 약간 저하되거나 사소한 오해가 생기기 쉬운 조심스러운 날입니다. 오늘만큼은 적극적인 나섬보다 느긋하고 방어적인 태도로 하루를 보내세요.",
            "dos": [
                "말을 하기 전에 '상대방이 어떻게 들을까?' 한 번 더 생각하는 신중함을 가져보세요.",
                "이동 시 길가나 계단에서 스마트폰을 보지 말고 안전 운전 및 보행에 각별히 신경 쓰세요.",
                "스트레스가 심하다면 잠시 하던 일을 내려놓고 명상이나 깊은 심호흡을 자주 해주세요."
            ],
            "donts": [
                "감정이 격해진 상태에서 중요한 인생의 결정을 내리거나 홧김에 솔직한 말을 쏟아내는 것.",
                "타인의 험담이나 뒷소문에 동조하여 함께 뒷이야기를 나누는 위험한 행동.",
                "타인과의 가벼운 논쟁에서 끝까지 이기려고 자존심 싸움을 벌이는 일."
            ]
        }
    }

    # 행운 데이터
    lucky_colors = ["로즈 핑크 🌸", "포레스트 그린 🌲", "미드나잇 블루 🌙", "버터 옐로우 🧈", "클래식 화이트 🤍", "라벤더 퍼플 🪻"]
    lucky_items = ["따뜻한 차 한 잔 ☕", "편안한 운동화 👟", "손거울 🪞", "다이어리와 펜 📝", "텀블러 🧊", "푹신한 쿠션 🛋️"]
    lucky_numbers = [3, 7, 8, 11, 21, 77, 99]
    healing_quotes = [
        "“오늘 흘린 작은 땀방울은 내일의 가장 눈부신 결실이 될 거예요.”",
        "“잠시 쉬어가도 괜찮아요. 당신은 이미 충분히 잘하고 있으니까요.”",
        "“뜻밖의 행운은 항상 무심코 지나치던 평범한 순간 속에 숨어있답니다.”",
        "“오늘 하루 당신이 가는 길마다 따뜻한 햇살이 가득하기를 응원합니다.”",
        "“마음먹은 대로 되지 않아도 괜찮아요. 더 멋진 기회가 찾아오는 과정일 뿐이에요.”"
    ]

    # 로딩 애니메이션 효과
    with st.spinner(f"🔮 {st.session_state.selected_zodiac}의 기운을 모아 {st.session_state.selected_category} 카드를 뽑는 중..."):
        time.sleep(0.8) # 약간의 연출용 대기 시간

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
            <div class='summary-text'>💡 <b>오늘의 총평:</b><br>{res['summary']}</div>
        </div>
    """, unsafe_allow_html=True)

    # (2) 운세 지수 (프로그레스 바)
    st.write(f"📊 **오늘의 {cat_name} 지수: {res['score']}점**")
    st.progress(res['score'] / 100)
    st.write("")

    # (3) Action Item (해야 할 일 / 피해야 할 일)
    col1, col2 = st.columns(2)
    with col1:
        st.success(f"**⭕ 오늘은 꼭 이렇게 해보세요!**\n\n{selected_do}")
    with col2:
        st.error(f"**❌ 오늘은 이런 행동을 피하세요!**\n\n{selected_dont}")

    st.write("")

    # (4) 행운 요소
    st.subheader("🍀 오늘의 행운 요소")
    lcol1, lcol2, lcol3 = st.columns(3)
    with lcol1:
        st.markdown(f"<div class='lucky-box'><div class='lucky-title'>🎨 행운의 컬러</div><div class='lucky-value'>{color}</div></div>", unsafe_allow_html=True)
    with lcol2:
        st.markdown(f"<div class='lucky-box'><div class='lucky-title'>🎁 행운의 아이템</div><div class='lucky-value'>{item}</div></div>", unsafe_allow_html=True)
    with lcol3:
        st.markdown(f"<div class='lucky-box'><div class='lucky-title'>🔢 행운의 숫자</div><div class='lucky-value'>{number}</div></div>", unsafe_allow_html=True)

    # (5) 힐링 메시지
    st.markdown(f"<div class='quote-box'>💌 오늘의 힐링 메시지<br><br>{quote}</div>", unsafe_allow_html=True)

    st.write("")
    st.balloons()

    # (6) 다시 뽑기 버튼
    if st.button("🔄 다른 운세 다시 뽑기", use_container_width=True):
        st.session_state.drawn = False
        st.rerun()
