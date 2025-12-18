import streamlit as st
from openai import OpenAI
import base64

# 1. 网页头部美化 (US Style)
st.set_page_config(page_title="FixHouse AI - Pro Home Repair", page_icon="🏠")

st.markdown("""
    <style>
    .main { background-color: #fcfcfc; }
    h1 { color: #1a365d; font-family: 'Arial'; }
    .stButton>button { background-color: #2b6cb0; color: white; border-radius: 8px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏠 FixHouse")
st.subheader("Your Personal US Home Contractor")
st.write("Snap a photo to diagnose issues and get a US-standard repair plan.")

# 2. 侧边栏设置 (API Key)
with st.sidebar:
    st.header("Settings")
    # 这里输入你在 xAI 申请的 Key
    grok_api_key = st.text_input("Enter Grok API Key", type="password")
    st.info("Powered by Grok-2-Vision")

# 3. 拍照/上传组件
uploaded_file = st.file_uploader("Upload a photo of the house problem", type=["jpg", "jpeg", "png"])

# 4. 核心逻辑
if uploaded_file:
    # 显示图片
    st.image(uploaded_file, caption="Inspecting this issue...", use_container_width=True)
    
    if st.button("Generate Repair Plan"):
        if not grok_api_key:
            st.error("Please enter your Grok API Key in the sidebar!")
        else:
            try:
                # 配置 Grok API (xAI 官方地址)
                client = OpenAI(
                    api_key=grok_api_key,
                    base_url="https://api.x.ai/v1",
                )
                
                # 将图片转为 Base64 编码
                base64_image = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

                with st.spinner('Grok is analyzing the damage...'):
                    # 5. 调用 Grok-2-Vision 模型
                    response = client.chat.completions.create(
                        model="grok-2-vision-1212", # 2025年最新视觉模型
                        messages=[
                            {
                                "role": "system",
                                "content": """You are an expert US Residential General Contractor. 
                                Analyze the photo and provide:
                                1. Diagnosis: What is the issue? (Use US terms like Drywall, HVAC, etc.)
                                2. Severity: Scale 1-10.
                                3. DIY vs Pro: Can the user fix it or need a Licensed Pro? 
                                4. Permit: Is a City Permit required for this fix?
                                5. Est. Cost: USD range.
                                6. Shopping List: Items from Home Depot or Lowe's.
                                7. Steps: Clear instructions in Imperial units (inches, feet).
                                Always include a Disclaimer that this is AI advice."""
                            },
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": "Analyze this home issue and provide a fix plan."},
                                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                                ]
                            }
                        ]
                    )
                    
                    # 输出结果
                    st.success("Analysis Complete!")
                    st.markdown("---")
                    st.markdown(response.choices[0].message.content)

            except Exception as e:
                st.error(f"Something went wrong: {e}")
