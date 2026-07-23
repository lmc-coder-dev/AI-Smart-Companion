import streamlit as st
import os
from openai import OpenAI

# 初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = []

# 设置页面的配置项
st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="img/img.png",
    # 布局
    layout="wide",
    # 控制的是侧边栏的状态
    initial_sidebar_state="expanded",
    menu_items={}
)

# 系统提示词
system_prompt = "你是一名非常可爱的AI助理，你的名字叫小甜甜，请你使用温柔可爱的语气回答用户的问题"

st.title("AI智能伴侣")

st.logo("👩‍🏫")

# 创建与AI大模型交互的客户端对象（DEEPSEEK_API_KEY 环境变量的名字，值就是DeepSeek的API_KEY）
client = OpenAI(api_key=os.environ.get("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

# 遍历会话状态中的消息
for message in st.session_state.messages:
  st.chat_message(message["role"]).write(message["content"])



# 消息输入框
message = st.chat_input("请输入你要问的题：")
if message:
    st.chat_message("user").write(message)
    # 保存用户的提示词
    st.session_state.messages.append({"role": "user", "content": message})

    # 调用AI大模型
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            *st.session_state.messages
        ],
        stream=False
    )

    st.chat_message("assistant").write(response.choices[0].message.content)
    # 保存AI大模型的回复
    st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})
