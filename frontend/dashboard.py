import streamlit as st
import json
import os
from PIL import Image
import requests
from io import BytesIO

st.set_page_config(page_title="AI Product Picker Dashboard", layout="wide")

st.title("🧠 HermitCreate 可视化选款系统")

DATA_PATH = "output.json"
PRODUCT_PATH = "products.json"

@st.cache_data
def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

products = load_json(PRODUCT_PATH)
results = load_json(DATA_PATH)

st.sidebar.header("控制面板")
min_score = st.sidebar.slider("最低评分过滤", 0, 100, 60)


def load_image(url):
    try:
        r = requests.get(url, timeout=5)
        return Image.open(BytesIO(r.content))
    except:
        return None

filtered = [p for p in products if p.get("total_score", 0) >= min_score]

cols = st.columns(3)

for i, p in enumerate(filtered):
    with cols[i % 3]:
        st.subheader(p.get("title", "Unknown"))
        st.write(f"ID: {p.get('product_id')}")
        st.write(f"Score: {p.get('total_score')}")
        st.write(f"Category: {p.get('category')}")

        img_url = p.get("image")
        if img_url:
            img = load_image(img_url)
            if img:
                st.image(img, use_column_width=True)
            else:
                st.text("图片加载失败")

        st.markdown("---")
