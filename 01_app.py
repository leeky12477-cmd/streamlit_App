import streamlit as st
import requests
import random

st.set_page_config(
    page_title="오늘 뭐 먹지?",
    page_icon="🍽️",
    layout="centered"
)

# ----------------------
# 귀여운 CSS
# ----------------------
st.markdown("""
<style>
.stApp{
background:linear-gradient(to bottom,#FFF7F3,#FFE6F2);
}

.title{
font-size:45px;
font-weight:bold;
text-align:center;
color:#ff5b8a;
}

.sub{
text-align:center;
font-size:18px;
color:gray;
}

.card{
background:white;
padding:20px;
border-radius:20px;
box-shadow:0px 5px 15px rgba(0,0,0,.15);
margin-top:20px;
}

.stButton>button{
background:#ff7eb3;
color:white;
border-radius:15px;
font-size:20px;
height:50px;
width:100%;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🍴 오늘 뭐 먹지?</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">서울의 현재 날씨를 확인해서 메뉴를 추천해드려요!</div>', unsafe_allow_html=True)

# ----------------------
# 메뉴 데이터
# ----------------------

menus = {

"Clear":[
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

"Rain":[
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

"Snow":[
{
"name":"떡국",
"image":"https://images.unsplash.com/photo-1512058564366-18510be2db19",
"kcal":540,
"protein":"21g",
"carb":"65g",
"fat":"16g"
}
],

"Clouds":[
{
"name":"우동",
"image":"https://images.unsplash.com/photo-1612929633738-8fe44f7ec841",
"kcal":530,
"protein":"17g",
"carb":"78g",
"fat":"12g"
}
]
}

# ----------------------
# 날씨 가져오기
# ----------------------

API_KEY = st.secrets["OPENWEATHER_API_KEY"]

url = f"https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={API_KEY}&units=metric"

response = requests.get(url)

data = response.json()

weather = data["weather"][0]["main"]

temp = data["main"]["temp"]

emoji = {
"Clear":"☀️",
"Clouds":"☁️",
"Rain":"🌧️",
"Snow":"❄️",
"Thunderstorm":"⛈️",
"Drizzle":"🌦️",
"Mist":"🌫️"
}

st.info(f"현재 서울 날씨 : {emoji.get(weather,'🌤️')} {weather} / {temp:.1f}℃")

# ----------------------
# 추천
# ----------------------

if weather not in menus:
    weather = "Clear"

if st.button("🍀 메뉴 추천"):

    menu = random.choice(menus[weather])

    st.markdown(f"""
    <div class="card">
    <h2 align="center">{menu['name']}</h2>
    </div>
    """, unsafe_allow_html=True)

    st.image(menu["image"], use_container_width=True)

    c1,c2 = st.columns(2)

    c1.metric("🔥 칼로리", f"{menu['kcal']} kcal")
    c2.metric("💪 단백질", menu["protein"])

    c3,c4 = st.columns(2)

    c3.metric("🍚 탄수화물", menu["carb"])
    c4.metric("🥑 지방", menu["fat"])

    st.success("맛있게 드세요! 😋")
    st.balloons()
