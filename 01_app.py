import streamlit as st
import random

st.set_page_config(
    page_title="🌤️ 날씨 메뉴 추천",
    page_icon="🍽️",
    layout="centered"
)

# ------------------------------
# CSS (귀여운 디자인)
# ------------------------------
st.markdown("""
<style>
.stApp{
    background: linear-gradient(to bottom,#FFF8F0,#FFEAF4);
}

.title{
    font-size:45px;
    text-align:center;
    color:#ff5c8d;
    font-weight:bold;
}

.subtitle{
    text-align:center;
    color:#666;
    font-size:18px;
    margin-bottom:20px;
}

.menu-card{
    background:white;
    padding:20px;
    border-radius:20px;
    box-shadow:0 5px 15px rgba(0,0,0,0.15);
    margin-top:15px;
}

.nutrient{
    background:#FFF6C7;
    padding:10px;
    border-radius:15px;
    margin:5px;
    font-size:17px;
}

.stButton>button{
    background:#ff7eb3;
    color:white;
    border-radius:15px;
    height:50px;
    width:100%;
    font-size:20px;
}

.stSelectbox label{
    font-size:20px;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------
# 메뉴 데이터
# ------------------------------

menus = {
    "☀️ 맑음":[
        {
            "name":"비빔밥",
            "image":"https://images.unsplash.com/photo-1553163147-622ab57be1c7",
            "kcal":620,
            "protein":"18g",
            "carb":"82g",
            "fat":"18g"
        },
        {
            "name":"샐러드",
            "image":"https://images.unsplash.com/photo-1546069901-ba9599a7e63c",
            "kcal":320,
            "protein":"15g",
            "carb":"22g",
            "fat":"14g"
        }
    ],

    "🌧️ 비":[
        {
            "name":"김치찌개",
            "image":"https://images.unsplash.com/photo-1604908176997-431ff0b5c7e2",
            "kcal":580,
            "protein":"30g",
            "carb":"45g",
            "fat":"22g"
        },
        {
            "name":"칼국수",
            "image":"https://images.unsplash.com/photo-1617093727343-374698b1b08d",
            "kcal":650,
            "protein":"20g",
            "carb":"90g",
            "fat":"18g"
        }
    ],

    "❄️ 눈":[
        {
            "name":"떡국",
            "image":"https://images.unsplash.com/photo-1512058564366-18510be2db19",
            "kcal":540,
            "protein":"21g",
            "carb":"65g",
            "fat":"16g"
        },
        {
            "name":"곰탕",
            "image":"https://images.unsplash.com/photo-1547592180-85f173990554",
            "kcal":490,
            "protein":"35g",
            "carb":"28g",
            "fat":"20g"
        }
    ],

    "☁️ 흐림":[
        {
            "name":"돈까스",
            "image":"https://images.unsplash.com/photo-1604908177522-4326d2b53f14",
            "kcal":840,
            "protein":"36g",
            "carb":"72g",
            "fat":"41g"
        },
        {
            "name":"우동",
            "image":"https://images.unsplash.com/photo-1612929633738-8fe44f7ec841",
            "kcal":530,
            "protein":"17g",
            "carb":"78g",
            "fat":"12g"
        }
    ],

    "🔥 더움":[
        {
            "name":"냉면",
            "image":"https://images.unsplash.com/photo-1553621042-f6e147245754",
            "kcal":480,
            "protein":"18g",
            "carb":"76g",
            "fat":"8g"
        },
        {
            "name":"초밥",
            "image":"https://images.unsplash.com/photo-1579871494447-9811cf80d66c",
            "kcal":520,
            "protein":"26g",
            "carb":"62g",
            "fat":"12g"
        }
    ],

    "🥶 추움":[
        {
            "name":"부대찌개",
            "image":"https://images.unsplash.com/photo-1544025162-d76694265947",
            "kcal":730,
            "protein":"34g",
            "carb":"49g",
            "fat":"35g"
        },
        {
            "name":"삼계탕",
            "image":"https://images.unsplash.com/photo-1604908177241-f84c20d75f1d",
            "kcal":690,
            "protein":"42g",
            "carb":"32g",
            "fat":"30g"
        }
    ]
}

# ------------------------------
# 화면
# ------------------------------

st.markdown('<div class="title">🍴 오늘 뭐 먹지?</div>', unsafe_allow_html=True)

st.markdown(
'<div class="subtitle">🌤️ 날씨에 맞는 메뉴를 추천해드려요!</div>',
unsafe_allow_html=True)

weather = st.selectbox(
    "오늘 날씨를 선택하세요",
    list(menus.keys())
)

if st.button("🍀 메뉴 추천받기"):

    menu = random.choice(menus[weather])

    st.markdown(
        f"""
        <div class="menu-card">
        <h2 style='text-align:center;color:#ff5c8d'>{menu['name']}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.image(menu["image"], use_container_width=True)

    col1,col2 = st.columns(2)

    with col1:
        st.metric("🔥 칼로리", f"{menu['kcal']} kcal")

    with col2:
        st.metric("💪 단백질", menu["protein"])

    st.markdown("---")

    c1,c2 = st.columns(2)

    with c1:
        st.info(f"🍚 탄수화물\n\n{menu['carb']}")

    with c2:
        st.success(f"🥑 지방\n\n{menu['fat']}")

    st.balloons()
