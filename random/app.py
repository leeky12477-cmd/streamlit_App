import random
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="오늘의 운세 뽑기 🔮", page_icon="🔮", layout="centered"
)


# 운세 데이터 베이스
LUCK_LEVELS = [
    {"level": "대길 (大吉)", "emoji": "🎉", "color": "#28a745"},
    {"level": "길 (吉)", "emoji": "✨", "color": "#17a2b8"},
    {"level": "평 (平)", "emoji": "☕", "color": "#6c757d"},
    {"level": "소흉 (小凶)", "emoji": "☁️", "color": "#fd7e14"},
    {"level": "흉 (凶)", "emoji": "⚡", "color": "#dc3545"},
]

COMMENTS = {
    "대길 (大吉)": [
        (
            "오늘은 뭘 해도 잘 풀리는 기적 같은 날!",
            "평소 미뤄뒀던 도전이나 고백을 해보세요.",
            "망설이다 시간을 허비하는 것.",
        ),
        (
            "행운의 신이 당신과 함께하는 날입니다.",
            "새로운 일을 시작하거나 로또를 사보는 것도 좋아요.",
            "너무 과도한 자만심.",
        ),
    ],
    "길 (吉)": [
        (
            "기분 좋은 소식이 찾아오는 무난하고 밝은 날.",
            "친한 사람들에게 안부 연락을 건네보세요.",
            "충동적인 지출.",
        ),
        (
            "노력한 만큼 성과가 나오는 보람찬 하루가 될 거예요.",
            "계획했던 일을 차근차근 진행해보세요.",
            "남과의 무의미한 비교.",
        ),
    ],
    "평 (平)": [
        (
            "잔잔하고 조용한 호수 같은 하루입니다.",
            "조용히 자기계발을 하거나 휴식을 취하세요.",
            "무리한 스케줄 잡기.",
        ),
        (
            "큰 이벤트는 없지만 평화로운 일상이 유지됩니다.",
            "맛있는 음식을 먹으며 소소한 행복을 즐겨보세요.",
            "주변 사람과의 감정 싸움.",
        ),
    ],
    "소흉 (小凶)": [
        (
            "마음이 조금 싱숭생숭하고 실수가 잦을 수 있는 날.",
            "매사에 신중하게 두 번씩 확인하고 행동하세요.",
            "섣부른 판단이나 계약.",
        ),
        (
            "작은 오해가 생길 수 있으니 말조심이 필요해요.",
            "따뜻한 차 한 잔 마시며 마음을 다스려보세요.",
            "남의 일에 쓸데없이 참견하기.",
        ),
    ],
    "흉 (凶)": [
        (
            "비구름이 조금 그늘을 만드는 날, 자중하는 것이 좋습니다.",
            "일찍 귀가해서 푹 쉬며 에너지를 충전하세요.",
            "음주운전, 위험한 행동, 감정적 대응.",
        ),
        (
            "뜻대로 되지 않아 답답할 수 있지만 곧 지나갑니다.",
            "혼자만의 시간을 가지며 조용히 보내세요.",
            "중요한 결정 내리기.",
        ),
    ],
}

CATEGORY_FORTUNES = {
    "종합운": [
        "전반적으로 순탄하며 마음의 평화를 찾을 수 있는 흐름입니다.",
        "예상치 못한 변수가 생길 수 있으니 유연하게 대처하세요.",
        "작은 노력으로도 큰 결실을 맺을 수 있는 상승세입니다.",
    ],
    "재물운": [
        "지갑이 든든해지는 날! 생각지도 못한 지출 감면이나 용돈이 생길 수 있어요.",
        "지출 관리가 필요한 날입니다. 충동구매를 꼭 주의하세요.",
        "투자나 금전 거래는 잠시 미루고 내실을 다지는 것이 좋습니다.",
    ],
    "연애운": [
        "매력이 상승하는 날! 솔로는 인연을 만날 수 있고, 커플은 애정이 깊어집니다.",
        "사소한 말 한마디로 오해가 생길 수 있으니 상대방의 말을 경청하세요.",
        "평범하지만 따뜻한 시간을 보낼 수 있는 편안한 애정운입니다.",
    ],
    "금전운": [
        "자금 흐름이 원활하여 마음의 여유가 생기는 하루입니다.",
        "불필요한 구독 서비스나 소소한 지출이 새어나가지 않는지 점검하세요.",
        "빌려준 돈이나 잊고 있던 포인트 등을 회수할 수 있는 기회!",
    ],
    "학업운": [
        "집중력이 최고조에 달하는 날! 어려운 개념도 쉽게 이해됩니다.",
        "산만해지기 쉬우니 휴대폰은 잠시 멀리 두고 환경을 정돈하세요.",
        "꾸준히 해온 공부가 빛을 발하는 날입니다. 자신감을 가지세요.",
    ],
}


# UI 구성
st.title("🔮 오늘의 운세 뽑기")
st.write("버튼을 눌러 오늘의 운세를 확인해 보세요!")

# 운세 뽑기 버튼
if st.button("✨ 오늘의 운세 뽑기 ✨", type="primary", use_container_width=True):
    # 1. 운세 등급 및 멘트 뽑기
    selected_luck = random.choice(LUCK_LEVELS)
    comment_data = random.choice(COMMENTS[selected_luck["level"]])

    # 2. 결과 출력 (메인 운세 카드)
    st.markdown("---")
    st.markdown(
        f"""
        <div style="
            text-align: center; 
            padding: 20px; 
            border-radius: 15px; 
            background-color: #f8f9fa; 
            border: 2px solid {selected_luck['color']};
            margin-bottom: 20px;">
            <h1 style="font-size: 3rem; margin: 0;">{selected_luck['emoji']}</h1>
            <h2 style="color: {selected_luck['color']}; margin: 10px 0;">오늘의 운세는 [{selected_luck['level']}] 입니다!</h2>
            <p style="font-size: 1.1rem; color: #333; font-weight: bold;">"{comment_data[0]}"</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 3. 추천 / 주의 사항
    col1, col2 = st.columns(2)
    with col1:
        st.success(f"**👍 하면 좋은 것**\n\n{comment_data[1]}")
    with col2:
        st.error(f"**👎 주의할 것**\n\n{comment_data[2]}")

    st.markdown("---")
    st.subheader("📊 카테고리별 세부 운세")

    # 4. 세부 카테고리운 출력
    icons = {
        "종합운": "🌟",
        "재물운": "💰",
        "연애운": "💖",
        "금전운": "💳",
        "학업운": "📚",
    }

    for category, icon in icons.items():
        fortune_text = random.choice(CATEGORY_FORTUNES[category])
        with st.expander(f"{icon} **{category}**", expanded=True):
            st.write(fortune_text)

    # 축하 효과 (대길이나 길인 경우)
    if selected_luck["level"] in ["대길 (大吉)", "길 (吉)"]:
        st.balloons()
