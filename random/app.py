import random
import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="오늘의 운세 뽑기 🍀",
    page_icon="🔮",
    layout="centered"
)

# 2. 커스텀 CSS (카드 스타일 및 디자인 개선)
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 2.6rem;
        font-weight: 800;
        color: #3B82F6;
        margin-bottom: 8px;
    }
    .sub-title {
        text-align: center;
        font-size: 1.1rem;
        color: #6B7280;
        margin-bottom: 25px;
    }
    .fortune-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F3F4F6 100%);
        border: 2px solid #E5E7EB;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        margin-bottom: 25px;
    }
    .result-emoji {
        font-size: 4.5rem;
        line-height: 1;
        margin-bottom: 12px;
    }
    .result-status {
        font-size: 2rem;
        font-weight: 800;
        color: #1F2937;
        margin-bottom: 8px;
    }
    .stars {
        font-size: 1.3rem;
        color: #F59E0B;
        margin-bottom: 15px;
    }
    .summary-text {
        font-size: 1.1rem;
        line-height: 1.6;
        color: #4B5563;
        background-color: #FFFFFF;
        padding: 15px 20px;
        border-radius: 12px;
        border-left: 4px solid #3B82F6;
        text-align: left;
    }
    .lucky-box {
        background-color: #EFF6FF;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        font-weight: bold;
        color: #1E40AF;
    }
    .quote-box {
        background-color: #FEF3C7;
        border-radius: 12px;
        padding: 18px;
        text-align: center;
        font-size: 1.05rem;
        color: #92400E;
        font-weight: 600;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 타이틀 영역
st.markdown("<div class='main-title'>🔮 오늘의 운세 뽑기</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>오늘 하루 나에게 찾아올 운명과 행운의 팁을 확인해보세요!</div>", unsafe_allow_html=True)

# 4. 운세 데이터베이스 (상세 내용 및 조언 보강)
fortunes = {
    "대길 (大吉)": {
        "stars": "⭐⭐⭐⭐⭐",
        "emoji": "🥳🎉",
        "summary": "손대는 일마다 놀라운 성과와 긍정적인 에너지가 가득한 날입니다! 망설이고 있던 중요한 도전이 있다면 지금 당장 시작해보세요.",
        "dos": [
            "그동안 미뤄두었던 과제나 중요한 연락을 망설이지 말고 오늘 실행으로 옮겨보세요.",
            "자신감 있고 당당하게 의견을 표현하세요. 귀인을 만나 적극적인 지원을 받을 확률이 높습니다.",
            "좋아하는 사람이나 소중한 지인에게 먼저 뜻밖의 작은 선물을 건네며 마음을 전해보세요."
        ],
        "donts": [
            "스스로의 가능성을 낮게 평가하거나 불필요한 겸손으로 다가온 기회를 지나쳐버리지 마세요.",
            "오늘 할 수 있는 일을 '내일 해야지' 하며 미루는 순간 행운의 흐름이 꺾일 수 있습니다.",
            "남들의 시선이나 평가에 너무 신경 쓰느라 본인이 진짜 원하는 바를 포기하는 것."
        ]
    },
    "길 (吉)": {
        "stars": "⭐⭐⭐⭐☆",
        "emoji": "😊🌸",
        "summary": "차분하면서도 알찬 보람을 거둘 수 있는 매끄러운 날입니다. 꾸준히 쌓아온 노력이 빛을 발하여 좋은 인정과 소식이 따릅니다.",
        "dos": [
            "평소 고마웠던 주변 사람들에게 감사 인사나 따뜻한 말 한마디를 나누어보세요.",
            "점심시간이나 퇴근 후 20분 정도 가벼운 산책을 하며 맑은 공기를 마시고 기분을 전환하세요.",
            "새롭게 관심을 갖고 있던 취미나 공부가 있다면 관련 자료를 차분히 탐색해보세요."
        ],
        "donts": [
            "분위기에 휩쓸려 충동구매를 하거나 계획에 없던 과도한 지출을 진행하는 것.",
            "가까운 사이일수록 예의를 갖추지 않고 감정적으로 대화를 이끌어가는 행동.",
            "약속 시간에 임박해 서두르다가 소지품을 잃어버리거나 실수를 유발하는 것."
        ]
    },
    "소길 (小吉)": {
        "stars": "⭐⭐⭐☆☆",
        "emoji": "🙂🌱",
        "summary": "큰 파도 없이 평화롭고 잔잔한 하루입니다. 커다란 대박을 노리기보다는 소소한 소확행을 만끽하는 것이 훨씬 유리합니다.",
        "dos": [
            "책상 위나 방 안 등 내 생활 영역을 말끔히 정리정돈하여 쾌적한 환경을 만들어보세요.",
            "따뜻한 인퓨전 티나 커피 한 잔을 마시며 나만의 조용한 휴식 시간을 가져보세요.",
            "오늘 처리해야 할 작은 업무나 루틴들을 하나씩 체크리스트로 지워나가는 소소한 재미를 느끼기."
        ],
        "donts": [
            "타인의 문제나 남의 싸움에 과도하게 오지랖을 부려 감정 에너지를 낭비하는 것.",
            "몸에 무리가 가는 격렬한 운동이나 과도한 음주·야식을 즐기는 행동.",
            "스스로를 다른 사람의 화려한 모습과 비교하며 사기를 떨어뜨리는 생각."
        ]
    },
    "평 (平)": {
        "stars": "⭐⭐☆☆☆",
        "emoji": "😐☕",
        "summary": "급격한 변화보다는 현재 상태를 유지하며 내실을 다져야 하는 무난한 하루입니다. 안정을 최우선으로 두는 것이 좋습니다.",
        "dos": [
            "평소 지켜오던 자신만의 일상 루틴을 묵묵히 이어나가며 제페이스를 유지하세요.",
            "퇴근/하교 후 일찍 잠자리에 들어 그동안 쌓인 컨디션 저하와 피로를 충분히 회복할 것.",
            "마음을 편안하게 해주는 음악을 듣거나 가벼운 독서로 심신을 다스려보세요."
        ],
        "donts": [
            "잘 알지 못하는 분야에 홧김에 큰돈을 투자하거나 불확실한 계약을 진행하는 것.",
            "중요한 안건에 대해 혼자서 독단적으로 판단하고 유별나게 고집을 부리는 행위.",
            "컨디션이 저하된 상태에서 억지로 무리한 밤샘 작업이나 과로를 강행하는 것."
        ]
    },
    "흉 (凶)": {
        "stars": "⭐☆☆☆☆",
        "emoji": "🥺🌧️",
        "summary": "컨디션이 저하되거나 사소한 오해가 생기기 쉬운 조심스러운 날입니다. 오늘만큼은 느긋하고 방어적인 태도로 하루를 보내세요.",
        "dos": [
            "말을 하기 전에 '상대방이 어떻게 들을까?' 한 번 더 생각하는 신중함을 가지세요.",
            "이동 시 길가나 계단에서 스마트폰을 보지 말고 안전 운전 및 보행에 각별히 신경 쓰세요.",
            "스트레스가 심하다면 잠시 모든 내려놓고 명상이나 심호흡을 자주 해주세요."
        ],
        "donts": [
            "중요한 인생의 결정을 내리거나 감정이 격해진 상태에서 솔직한 말을 쏟아내는 것.",
            "타인의 험담이나 뒷소문에 동조하여 함께 뒷이야기를 나누는 행동.",
            "타인과의 가벼운 논쟁에서 끝까지 이기려고 자존심 싸움을 벌이는 일."
        ]
    }
}

# 행운의 요소 데이터베이스
lucky_colors = ["로즈 핑크 🌸", "포레스트 그린 🌲", "미드나잇 블루 🌙", "버터 옐로우 🧈", "클래식 화이트 🤍", "라벤더 퍼플 🪻"]
lucky_items = ["따뜻한 차 한 잔 ☕", "편안한 운동화 👟", "손거울 🪞", "다이어리와 펜 📝", "텀블러 🧊", "푹신한 쿠션 🛋️"]
lucky_numbers = [3, 7, 8, 11, 21, 77, 99]

# 힐링 한마디 모음
healing_quotes = [
    "“오늘 흘린 작은 땀방울은 내일의 가장 눈부신 결실이 될 거예요.”",
    "“잠시 쉬어가도 괜찮아요. 당신은 이미 충분히 잘하고 있으니까요.”",
    "“뜻밖의 행운은 항상 무심코 지나치던 평범한 순간 속에 숨어있답니다.”",
    "“오늘 하루 당신이 가는 길마다 따뜻한 햇살이 가득하기를 응원합니다.”",
    "“마음먹은 대로 되지 않아도 괜찮아요. 더 멋진 기회가 찾아오는 과정일 뿐이에요.”"
]

# 5. 카테고리 선택
category = st.selectbox(
    "👉 어떤 종류의 운세가 궁금하신가요?",
    ["종합운 🌟", "금전운 💰", "학업운 📚", "재물운 💎", "연애운 💕"]
)

st.write("")

# 6. 뽑기 버튼 및 결과 화면
if st.button("🔮 오늘의 운세 뽑기!", use_container_width=True):
    # 랜덤 뽑기 처리
    status_key = random.choice(list(fortunes.keys()))
    res = fortunes[status_key]
    
    selected_do = random.choice(res["dos"])
    selected_dont = random.choice(res["donts"])
    
    color = random.choice(lucky_colors)
    item = random.choice(lucky_items)
    number = random.choice(lucky_numbers)
    quote = random.choice(healing_quotes)
    
    # 뽑기 로딩 효과
    with st.spinner("운명의 카드를 섞고 있습니다..."):
        # (1) 메인 운세 카드
        cat_name = category.split()[0]
        st.markdown(f"""
            <div class='fortune-card'>
                <div class='result-emoji'>{res['emoji']}</div>
                <div class='result-status'>[{cat_name}] {status_key}</div>
                <div class='stars'>{res['stars']}</div>
                <div class='summary-text'>💡 <b>오늘의 총평:</b><br>{res['summary']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # (2) 구체적인 해야 할 일 / 피해야 할 일
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"**⭕ 오늘은 꼭 이렇게 해보세요!**\n\n{selected_do}")
            
        with col2:
            st.error(f"**❌ 오늘은 이런 행동을 피하세요!**\n\n{selected_dont}")
            
        st.write("")
        
        # (3) 행운의 지표 (3개 컬럼 구성)
        st.subheader("🍀 오늘의 행운 요소")
        lcol1, lcol2, lcol3 = st.columns(3)
        
        with lcol1:
            st.markdown(f"<div class='lucky-box'>🎨 행운의 컬러<br><br>{color}</div>", unsafe_allow_html=True)
        with lcol2:
            st.markdown(f"<div class='lucky-box'>🎁 행운의 아이템<br><br>{item}</div>", unsafe_allow_html=True)
        with lcol3:
            st.markdown(f"<div class='lucky-box'>🔢 행운의 숫자<br><br><b>{number}</b></div>", unsafe_allow_html=True)
            
        # (4) 힐링 한마디
        st.markdown(f"<div class='quote-box'>💌 오늘의 힐링 메시지<br><br>{quote}</div>", unsafe_allow_html=True)
        
        # 축하 효과 애니메이션
        st.balloons()
