import random
import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="오늘의 운세 복권 🎲",
    page_icon="🔮",
    layout="centered"
)

# 2. 커스텀 CSS (깔끔하고 모던한 스타일)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #F8FAFC 0%, #EDF2F7 100%);
    }
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
    </style>
""", unsafe_allow_html=True)

# 3. 세션 상태 초기화
if "drawn" not in st.session_state:
    st.session_state.drawn = False
if "count" not in st.session_state:
    st.session_state.count = 0

MAX_DRAWS = 3 # 하루 최대 3회 제한

# 4. 타이틀 영역
st.markdown("""
    <div class='title-container'>
        <div class='main-title'>🎲 오늘의 운세 복권</div>
        <div class='sub-title'>마우스로 복권을 직접 긁어 오늘의 운세를 확인해보세요!</div>
    </div>
""", unsafe_allow_html=True)

st.write("")

# ----------------------------------------------------
# 화면 1: 카테고리 선택 화면 (종합운, 재물운, 학업운, 금전운, 연애운)
# ----------------------------------------------------
if not st.session_state.drawn:
    st.markdown(f"""
        <div class='intro-card'>
            <div class='intro-badge'>🔮 TODAY's FORTUNE</div>
            <h3 style='margin-top:0; color:#1A202C; font-size:1.25rem;'>궁금한 운세를 선택하고 복권을 뽑아보세요</h3>
            <p style='color:#718096; font-size:0.9rem; margin-bottom:0;'>
                <b>(오늘의 남은 기회: {MAX_DRAWS - st.session_state.count} / {MAX_DRAWS}회)</b>
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 5가지 카테고리 선택
    category = st.selectbox(
        "👉 뽑고 싶은 운세를 선택해주세요",
        ["종합운 🌟", "재물운 💎", "학업운 📚", "금전운 💰", "연애운 💕"]
    )

    st.write("")

    # 횟수 제한 확인 및 뽑기 진행
    if st.session_state.count >= MAX_DRAWS:
        st.warning("⚠️ 오늘의 뽑기 기회를 모두 사용하셨습니다! 내일 다시 시도해주세요. 🍀")
        st.button("🎲 운세 복권 뽑기", disabled=True, use_container_width=True)
    else:
        if st.button("🎲 운세 복권 뽑기!", use_container_width=True, type="primary"):
            st.session_state.selected_category = category
            st.session_state.count += 1
            st.session_state.drawn = True
            st.rerun()

# ----------------------------------------------------
# 화면 2: 긁기 화면 (행운 요소 명칭 라벨 직관화)
# ----------------------------------------------------
else:
    # 운세 데이터
    fortunes = {
        "대길 (大吉)": {
            "score": 98,
            "stars": "⭐⭐⭐⭐⭐",
            "emoji": "🥳",
            "summary": "뭘 해도 이상하게 잘 풀리는 날입니다! 망설이던 일이 있다면 일단 지르고 보세요. 의외의 대박이나 소소한 횡재수가 기다리고 있습니다.",
            "dos": "평소 사고 싶었던 거나 하고 싶었던 게 있다면 자신 있게 도전해보기!",
            "donts": "다 잘 되고 있는데 사서 걱정하고 괜히 눈치 보기."
        },
        "길 (吉)": {
            "score": 85,
            "stars": "⭐⭐⭐⭐☆",
            "emoji": "😎",
            "summary": "전반적으로 기분 좋은 일들이 소소하게 터지는 날입니다. 무난하면서도 보람찬 하루를 보낼 수 있는 아주 매끄러운 흐름이에요.",
            "dos": "맛있는 디저트나 최애 음료 한 잔으로 스스로에게 소소한 포상 주기.",
            "donts": "괜히 분위기에 휩쓸려 내 스타일도 아닌 일에 억지로 끼어들기."
        },
        "소길 (小吉)": {
            "score": 70,
            "stars": "⭐⭐⭐☆☆",
            "emoji": "🙂",
            "summary": "크게 특별할 건 없지만 평화롭고 잔잔한 하루입니다. 커다란 이벤트를 기대하기보다는 무탈한 일상의 소확행을 만끽하세요.",
            "dos": "최애 음악 들으면서 기분 좋게 멍때리는 휴식 시간 갖기.",
            "donts": "남들의 SNS 보면서 '나만 심심한가?' 스스로 비교하며 우울해하기."
        },
        "평 (平)": {
            "score": 55,
            "stars": "⭐⭐☆☆☆",
            "emoji": "😐",
            "summary": "잔잔한 호수 같은 날입니다. 큰 변화나 도전을 시도하기보다는 기존의 상태를 잘 유지하며 평정심을 지키는 게 가장 좋습니다.",
            "dos": "퇴근이나 하교 후에 내가 제일 좋아하는 영상 보면서 푹 쉬기.",
            "donts": "잘 모르는 일에 홧김에 큰돈 쓰거나 충동적으로 결정 내리기."
        },
        "흉 (凶)": {
            "score": 40,
            "stars": "⭐☆☆☆☆",
            "emoji": "🫠",
            "summary": "오늘은 약간 '억울한 일'이나 사소한 해프닝이 생길 수 있는 날입니다. 그냥 '오늘 액땜했다!' 치고 부드럽게 넘겨버리는 대범함이 필요해요.",
            "dos": "한 귀로 듣고 한 귀로 흘리는 무던한 스킬 적극 활용하기.",
            "donts": "욱하는 마음에 홧김에 한마디 쏘아붙였다가 일 크게 키우기."
        }
    }

    # 행운 및 음악 데이터
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

    # 무작위 결과 추출
    status_key = random.choice(list(fortunes.keys()))
    res = fortunes[status_key]
    color = random.choice(lucky_colors)
    place = random.choice(lucky_places)
    number = random.choice(lucky_numbers)
    bgm = random.choice(music_list)
    quote = random.choice(healing_quotes)
    cat_name = st.session_state.selected_category.split()[0]

    # HTML/JS 자동 긁기 기능 및 명확한 라벨링 적용
    scratch_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                margin: 0;
                padding: 10px;
                background: transparent;
            }}
            .scratch-container {{
                position: relative;
                width: 100%;
                max-width: 480px;
                border-radius: 20px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.1);
                overflow: hidden;
                background: white;
                border: 2px solid #E2E8F0;
            }}
            .content {{
                padding: 25px;
                text-align: center;
                box-sizing: border-box;
            }}
            .emoji {{ font-size: 3.5rem; margin-bottom: 5px; }}
            .status {{ font-size: 1.8rem; font-weight: 800; color: #1A202C; margin-bottom: 5px; }}
            .stars {{ font-size: 1.2rem; color: #ECC94B; margin-bottom: 15px; }}
            .summary {{
                font-size: 0.95rem; line-height: 1.6; color: #2D3748;
                background: #F7FAFC; padding: 15px; border-radius: 12px;
                border-left: 4px solid #4A5568; text-align: left; margin-bottom: 15px;
            }}
            .box-grid {{
                display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px;
            }}
            .do-box {{ background: #F0FDF4; border: 1px solid #BBF7D0; padding: 10px; border-radius: 10px; font-size: 0.85rem; color: #166534; text-align: left; }}
            .dont-box {{ background: #FEF2F2; border: 1px solid #FECACA; padding: 10px; border-radius: 10px; font-size: 0.85rem; color: #991B1B; text-align: left; }}
            
            /* 행운 요소 3개 컬럼 그리드 레이아웃 */
            .lucky-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr 1fr;
                gap: 8px;
                margin-bottom: 15px;
            }}
            .lucky-card {{
                background: #F8FAFC;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
                padding: 10px 5px;
                text-align: center;
            }}
            .lucky-label {{
                font-size: 0.75rem;
                color: #718096;
                font-weight: 600;
                margin-bottom: 4px;
            }}
            .lucky-val {{
                font-size: 0.85rem;
                color: #1A202C;
                font-weight: 700;
            }}

            .music {{ background: #F0F9FF; color: #0369A1; padding: 10px; border-radius: 10px; font-size: 0.85rem; margin-bottom: 10px; font-weight: 600; }}
            .quote {{ font-size: 0.85rem; color: #4A5568; font-style: italic; }}
            
            canvas {{
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                cursor: pointer;
                touch-action: none;
                transition: opacity 0.5s ease;
            }}
            .guide-text {{
                margin-top: 8px; font-size: 0.85rem; color: #718096; font-weight: 600;
            }}
        </style>
    </head>
    <body>
        <div class="scratch-container" id="container">
            <div class="content">
                <div class="emoji">{res['emoji']}</div>
                <div class="status">[{cat_name}] {status_key}</div>
                <div class="stars">{res['stars']}</div>
                <div class="summary">💡 <b>오늘의 한줄 요약:</b><br>{res['summary']}</div>
                <div class="box-grid">
                    <div class="do-box"><b>⭕ 해보세요</b><br>{res['dos']}</div>
                    <div class="dont-box"><b>❌ 피하세요</b><br>{res['donts']}</div>
                </div>
                
                <!-- 명확하게 단어를 표기한 행운 카드 영역 -->
                <div class="lucky-grid">
                    <div class="lucky-card">
                        <div class="lucky-label">🎨 행운의 컬러</div>
                        <div class="lucky-val">{color}</div>
                    </div>
                    <div class="lucky-card">
                        <div class="lucky-label">📍 행운의 장소</div>
                        <div class="lucky-val">{place}</div>
                    </div>
                    <div class="lucky-card">
                        <div class="lucky-label">🔢 행운의 숫자</div>
                        <div class="lucky-val">{number}</div>
                    </div>
                </div>

                <div class="music">🎵 {bgm}</div>
                <div class="quote">💌 {quote}</div>
            </div>
            <canvas id="scratchCanvas"></canvas>
        </div>
        <div class="guide-text" id="guide">👆 마우스로 쓱쓱 긁어보세요! (조금만 긁으면 알아서 열려요)</div>

        <script>
            const canvas = document.getElementById('scratchCanvas');
            const ctx = canvas.getContext('2d');
            const container = document.getElementById('container');
            const guide = document.getElementById('guide');

            let isRevealed = false;

            function initCanvas() {{
                canvas.width = container.offsetWidth;
                canvas.height = container.offsetHeight;

                // 은색 레이어
                ctx.fillStyle = '#CBD5E1';
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                // 안내문
                ctx.fillStyle = '#64748B';
                ctx.font = 'bold 20px sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText('🪙 여기를 긁어보세요!', canvas.width / 2, canvas.height / 2 - 10);
                
                ctx.font = '14px sans-serif';
                ctx.fillText('오늘의 운세 복권', canvas.width / 2, canvas.height / 2 + 20);
            }}

            let isDrawing = false;

            // 긁은 비율(면적) 계산 함수
            function checkScratchPercentage() {{
                if (isRevealed) return;

                const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
                const pixels = imageData.data;
                let transparentPixels = 0;

                for (let i = 3; i < pixels.length; i += 4) {{
                    if (pixels[i] === 0) {{
                        transparentPixels++;
                    }}
                }}

                const percentage = (transparentPixels / (pixels.length / 4)) * 100;

                // 40% 이상 긁었으면 자동으로 나머지 전체 지우기
                if (percentage >= 40) {{
                    isRevealed = true;
                    canvas.style.opacity = '0';
                    setTimeout(() => {{
                        canvas.style.display = 'none';
                    }}, 500);
                    guide.innerText = "✨ 오늘의 운세가 모두 공개되었습니다!";
                }}
            }}

            function scratch(e) {{
                if (!isDrawing || isRevealed) return;
                const rect = canvas.getBoundingClientRect();
                const x = (e.clientX || e.touches[0].clientX) - rect.left;
                const y = (e.clientY || e.touches[0].clientY) - rect.top;

                ctx.globalCompositeOperation = 'destination-out';
                ctx.beginPath();
                ctx.arc(x, y, 30, 0, Math.PI * 2);
                ctx.fill();

                checkScratchPercentage();
            }}

            canvas.addEventListener('mousedown', (e) => {{ isDrawing = true; scratch(e); }});
            canvas.addEventListener('mousemove', scratch);
            canvas.addEventListener('mouseup', () => isDrawing = false);
            
            canvas.addEventListener('touchstart', (e) => {{ isDrawing = true; scratch(e); }});
            canvas.addEventListener('touchmove', scratch);
            canvas.addEventListener('touchend', () => isDrawing = false);

            window.onload = initCanvas;
        </script>
    </body>
    </html>
    """

    # 복권 긁기 컴포넌트
    components.html(scratch_html, height=620)

    st.write("")

    # 재뽑기 및 횟수 안내
    left_draws = MAX_DRAWS - st.session_state.count
    if left_draws > 0:
        if st.button(f"🔄 다른 운세 다시 뽑기 (남은 기회: {left_draws}회)", use_container_width=True):
            st.session_state.drawn = False
            st.rerun()
    else:
        st.warning("⚠️ 오늘의 재뽑기 기회를 모두 사용하셨습니다.")
        if st.button("🏠 처음 화면으로 돌아가기", use_container_width=True):
            st.session_state.drawn = False
            st.rerun()
