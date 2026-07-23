import random
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="오늘의 운세 뽑기 🍀",
    page_icon="🔮",
    layout="centered"
)

# 커스텀 CSS (디자인을 조금 더 귀엽게!)
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        color: #4A90E2;
        margin-bottom: 20px;
    }
    .fortune-box {
        background-color: #F8F9FA;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
    }
    .result-emoji {
        font-size: 4rem;
        margin-bottom: 10px;
    }
    .result-status {
        font-size: 1.8rem;
        font-weight: bold;
        color: #333333;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 헤더 타이틀
st.markdown("<div class='main-title'>🔮 오늘의 운세 뽑기 🔮</div>", unsafe_allow_html=True)
st.write("원하는 운세 카테고리를 선택하고 버튼을 눌러 오늘의 운세를 확인해보세요!")

# 운세 데이터 정의
fortunes = {
    "대길 (大吉)": {
        "emoji": "🥳🎉",
        "dos": ["새로운 일 도전하기", "좋아하는 사람에게 연락하기", "맛있는 음식 먹기", "자신감 있게 말하기"],
        "donts": ["너무 겸손해하기", "오늘 할 일 미루기", "망설이기"]
    },
    "길 (吉)": {
        "emoji": "😊🌸",
        "dos": ["주변 사람에게 감사 표현하기", "가벼운 산책하기", "계획했던 일 시작하기"],
        "donts": ["충동구매 하기", "늦잠 자기", "약속 시간에 늦기"]
    },
    "소길 (小吉)": {
        "emoji": "🙂🌱",
        "dos": ["방 정리정돈 하기", "따뜻한 차 마시기", "차분하게 하루 정리하기"],
        "donts": ["무리한 운동 하기", "감정적으로 대응하기", "과식하기"]
    },
    "평 (平)": {
        "emoji": "😐☕",
        "dos": ["평소대로 루틴 지키기", "일찍 잠자리에 들기", "책 한 권 읽기"],
        "donts": ["큰 돈 쓰기", "새로운 계약 체결하기", "남과 비교하기"]
    },
    "흉 (凶)": {
        "emoji": "🥺🌧️",
        "dos": ["말조심하기", "안전 운전/보행하기", "스스로에게 휴식 선물하기"],
        "donts": ["중요한 결정 내리기", "비밀 이야기 털어놓기", "비판적인 말 하기"]
    }
}

# 1. 카테고리 선택
category = st.selectbox(
    "어떤 운세가 궁금하신가요?",
    ["종합운 🌟", "금전운 💰", "학업운 📚", "재물운 💎", "연애운 💕"]
)

st.markdown("---")

# 2. 뽑기 버튼 및 결과 출력
if st.button("🔮 운세 뽑기!", use_container_width=True):
    # 랜덤 결과 선택
    status, data = random.choice(list(fortunes.items()))
    do_item = random.choice(data["dos"])
    dont_item = random.choice(data["donts"])
    
    # 뽑기 효과
    with st.spinner("오늘의 운세를 읽는 중..."):
        # 결과 카드 출력
        st.markdown(f"""
            <div class='fortune-box'>
                <div class='result-emoji'>{data['emoji']}</div>
                <div class='result-status'>[{category.split()[0]}] 결과: {status}</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("") # 간격 조정
        
        # 행동 조언 (콜아웃 상자로 깔끔하게 표시)
        col1, col2 = st.columns(2)
        
        with col1:
            st.success(f"**⭕ 오늘은 이런 걸 해보세요!**\n\n👉 {do_item}")
            
        with col2:
            st.error(f"**❌ 오늘은 이런 걸 피하세요!**\n\n👉 {dont_item}")
            
        st.balloons() # 축하 효과 애니메이션
