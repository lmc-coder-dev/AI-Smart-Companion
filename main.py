import streamlit as st
import os
from openai import OpenAI
from datetime import datetime
import json


# 生成会话标识函数
def generate_session_name():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def save_session():
    # 1. 保存当前会话信息
    if st.session_state.current_session:
        # 构建新的会话对象
        session_data = {
            "nick_name": st.session_state.nick_name,
            "nature": st.session_state.nature,
            "current_session": st.session_state.current_session,
            "messages": st.session_state.messages
        }

        # 如果 sessions 目录不存在，则创建
        if not os.path.exists("sessions"):
            os.mkdir("sessions")

    # 保存会话数据
    with open(f"sessions/{st.session_state.current_session}.json", "w", encoding="utf-8") as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)


# 加载所有的会话列表信息
def load_sessions():
    session_list = []

    # 加载sessions目录下的文件
    if os.path.exists("sessions"):
        file_list = os.listdir("sessions")
        for filename in file_list:
            if filename.endswith(".json"):
                session_list.append(filename[:-5])

    return session_list

# 初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = []

# 昵称
if "nick_name" not in st.session_state:
    st.session_state.nick_name = "小甜甜"

# 性格
if "nature" not in st.session_state:
    st.session_state.nature = "活泼开朗的广东姑娘"
# 会话标识
if "current_session" not in st.session_state:
    st.session_state.current_session = generate_session_name()

# 加载指定的会话信息
def load_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            # 读取会话数据
            with open(f"sessions/{session_name}.json", "r", encoding="utf-8") as f:
                session_data = json.load(f)
                st.session_state.messages = session_data["messages"]
                st.session_state.nick_name = session_data["nick_name"]
                st.session_state.nature = session_data["nature"]
                st.session_state.current_session = session_name
    except Exception:
        st.error("加载会话失败！")

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
system_prompt = """你叫%s，现在是用户的真实伴侣，请完全代入伴侣角色。：
                    规则：
                    1. 每次只回1条消息
                    2. 禁止任何场景或状态描述性文字
                    3. 匹配用户的语言
                    4. 回复简短，像微信聊天一样
                    5. 有需要的话可以用❤️🌸等emoji表情
                    6. 用符合伴侣性格的方式对话
                    7. 回复的内容，要充分体现伴侣的性格特征
                    伴侣性格：
                    - %s
                    你必须严格遵守上述规则来回复用户。
                """

st.title("AI智能伴侣")

st.logo("👩‍🏫")

# 左边的侧边栏
with st.sidebar:
    # 会话信息
    st.subheader("AI会话面板")

    if st.button("新建会话", width="stretch", icon="📝"):
        # 2. 创建新的会话
        if st.session_state.messages:
            save_session()
        st.session_state.messages = []
        st.session_state.current_session = generate_session_name()
        st.rerun()

    # 会话历史
    st.text("会话历史")
    session_list = load_sessions()
    for session in session_list:
        col1, col2 = st.columns([4, 1])
        with col1:
            # 加载会话信息
            if st.button(session, width="stretch", icon="📄", key=f"load_{session}" ,type="primary" if session == st.session_state.current_session else "secondary",):
                load_session(session)
                st.rerun()
        with col2:
            # 删除会话信息
            if st.button("", width="stretch", icon="❌", key=f"delete_{session}"):
                pass

    st.subheader("伴侣信息")
    # 昵称输入框
    nickname = st.text_input("昵称：",placeholder="请输入昵称",value=st.session_state.nick_name)
    if nickname:
        st.session_state.nick_name = nickname
    # 性格输入框
    nature = st.text_area('性格', placeholder="请输入伴侣性格", value=st.session_state.nature)
    if nature:
        st.session_state.nature = nature

# 创建与AI大模型交互的客户端对象（DEEPSEEK_API_KEY 环境变量的名字，值就是DeepSeek的API_KEY）
client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    timeout=30.0,    # 请求超时30秒
    max_retries=2    # SDK自动重试2次网络错误
)

# 展示聊天信息
st.text(f"会话名称：{st.session_state.current_session}")
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
            {"role": "system", "content": system_prompt % (st.session_state.nick_name, st.session_state.nature)},
            *st.session_state.messages
        ],
        stream=True
    )

    response_message = st.empty()
    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            full_response += chunk.choices[0].delta.content
            response_message.chat_message("assistant").write(full_response)
    # 保存AI大模型的回复
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    #保存会话
    save_session()
    load_session(st.session_state.current_session)
    st.rerun()
