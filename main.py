import streamlit as st

# 设置页面的配置项

st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="🤖",
    # 布局
    layout="wide",
    # 控制的是侧边栏的状态
    initial_sidebar_state="expanded",
    menu_items={}
)

st.title("AI智能伴侣")

st.logo("img/img.png")

# 消息输入框
message = st.chat_input("请输入你要问的题：")
if message:
    st.write("你的问题：", message)
    st.write("AI的回复：", "这是AI的回复")
