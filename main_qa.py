"""
交互式旅游问答系统
基于RAG的智能旅游助手
"""
import streamlit as st
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="智能旅游问答助手",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 导入RAG引擎（使用千问API分析 + 本地数据检索）
from rag_engine import chat_rag, get_rag_engine

# 初始化RAG引擎
@st.cache_resource
def init_rag_engine():
    """初始化RAG引擎"""
    return get_rag_engine()

engine = init_rag_engine()

# CSS样式
st.markdown("""
<style>
/* 全局背景 */
.stApp {
    background: linear-gradient(135deg, #f0f9ff 0%, #e6f7ff 50%, #f0f9ff 100%);
    background-attachment: fixed;
}

/* 主容器卡片 */
.main-container {
    background: #ffffff;
    border-radius: 20px;
    padding: 28px;
    margin: 16px;
    box-shadow: 0 8px 30px rgba(0, 123, 255, 0.08);
    border: 1px solid rgba(0, 123, 255, 0.1);
}

/* 顶部 Banner */
.banner {
    background: linear-gradient(135deg, #007bff, #00aaff);
    border-radius: 16px;
    padding: 36px;
    text-align: center;
    color: white;
    margin-bottom: 28px;
    box-shadow: 0 6px 20px rgba(0, 123, 255, 0.25);
}
.banner h1 {
    font-size: 2.4rem;
    margin: 0;
    font-weight: 700;
}
.banner p {
    margin-top: 10px;
    opacity: 0.95;
    font-size: 1.05rem;
}

/* 输入框 */
.stTextInput > div > div > input {
    border-radius: 14px;
    padding: 14px 18px;
    font-size: 1rem;
    border: 1px solid #d1e7ff;
    transition: all 0.25s ease;
}
.stTextInput > div > div > input:focus {
    border-color: #007bff;
    box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.15);
}

/* 按钮 */
.stButton > button {
    background: linear-gradient(135deg, #007bff, #00aaff);
    color: white;
    border: none;
    border-radius: 14px;
    padding: 14px 24px;
    font-size: 1rem;
    font-weight: 600;
    transition: all 0.25s ease;
    box-shadow: 0 4px 12px rgba(0, 123, 255, 0.2);
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(0, 123, 255, 0.28);
}

/* 快捷按钮 */
.quick-btn {
    background: #ffffff;
    border: 1px solid #d1e7ff;
    border-radius: 12px;
    padding: 10px 16px;
    transition: all 0.2s;
}
.quick-btn:hover {
    border-color: #007bff;
    background: #e6f7ff;
}

/* 对话气泡 */
.chat-message {
    padding: 18px;
    border-radius: 16px;
    margin: 12px 0;
    line-height: 1.6;
}
/* 用户气泡 */
.chat-user {
    background: linear-gradient(135deg, #e6f7ff, #f0f9ff);
    border-left: 4px solid #007bff;
}
/* 助手气泡 */
.chat-assistant {
    background: #ffffff;
    border: 1px solid #e6f7ff;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

/* 信息卡片 */
.info-card {
    background: #f8fcff;
    border-radius: 12px;
    padding: 16px;
    margin: 10px 0;
    border: 1px solid #d1e7ff;
}

/* 分割线 */
hr {
    border: none;
    height: 1px;
    background-color: #e6f7ff;
    margin: 24px 0;
}
</style>""", unsafe_allow_html=True)

# 主界面
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Banner
st.markdown("""
<div class="banner">
    <h1>🌍 智能旅游问答助手</h1>
    <p>千问API智能分析 + 本地数据精准检索</p>
</div>
""", unsafe_allow_html=True)

# 初始化session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "current_question" not in st.session_state:
    st.session_state.current_question = ""

# 快捷问题
st.markdown("### 💬 快捷问题")
quick_questions = [
    ("北京景点推荐", "🏛️"),
    ("成都美食攻略", "🍜"),
    ("上海3日游", "🗼"),
    ("杭州住宿建议", "🏨"),
    ("西安美食推荐", "🏺"),
    ("重庆景点", "🌁"),
]

cols = st.columns(3)
for i, (q, icon) in enumerate(quick_questions):
    with cols[i % 3]:
        if st.button(f"{icon} {q}", key=f"quick_{i}", use_container_width=True):
            st.session_state.current_question = q

# 当前问题
current_question = st.session_state.get("current_question", "")

# 输入框
st.markdown("### 🔍 问我任何旅游问题")
user_input = st.text_input(
    "",
    placeholder="例如：北京有什么好吃的？上海三日游怎么安排？成都景点推荐...",
    label_visibility="collapsed",
    key="main_input"
)

# 处理输入
if user_input:
    st.session_state.current_question = user_input

# 显示当前问题
if st.session_state.current_question:
    question = st.session_state.current_question
    
    # 添加用户消息
    st.session_state.messages.append({"role": "user", "content": question})
    st.session_state.chat_history.append({"role": "user", "content": question, "time": datetime.now().strftime("%H:%M")})
    
    # 显示用户问题
    st.markdown(f"""
    <div class="chat-message chat-user">
        <strong>🙋 您的问题：</strong><br>
        {question}
    </div>
    """, unsafe_allow_html=True)
    
    # 生成回答（使用千问API分析 + 本地数据检索）
    with st.spinner("正在分析您的问题..."):
        try:
            answer = chat_rag(question)
        except Exception as e:
            answer = f"抱歉，服务暂时不可用。请稍后重试。\n\n错误信息：{str(e)}"
    
    # 添加助手消息
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.session_state.chat_history.append({"role": "assistant", "content": answer, "time": datetime.now().strftime("%H:%M")})
    
    # 显示回答
    st.markdown(f"""
    <div class="chat-message chat-assistant">
        <strong>🤖 智能回答：</strong><br><br>
        {answer.replace(chr(10), '<br>')}
    </div>
    """, unsafe_allow_html=True)
    
    # 清空当前问题
    st.session_state.current_question = ""

# 历史记录
st.markdown("---")
st.markdown("### 📜 对话历史")

if st.session_state.chat_history:
    for i, msg in enumerate(st.session_state.chat_history[-10:]):
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="chat-message chat-user">
                <span style="color:#667eea;">🙋 您：</span> {msg['content'][:50]}...
                <span style="float:right;font-size:0.8rem;color:#999;">{msg['time']}</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.expander(f"🤖 回答 ({msg['time']})", expanded=False):
                st.markdown(msg["content"])
else:
    st.info("暂无对话历史，开始提问吧！")

st.markdown('</div>', unsafe_allow_html=True)

# 侧边栏 - 功能介绍
with st.sidebar:
    st.markdown("### 📖 工作原理")
    st.markdown("""
    <div class="info-card">
        <strong>智能问答流程：</strong>
        <ol>
            <li>千问API分析您的问题</li>
            <li>识别城市和意图类型</li>
            <li>从本地数据检索相关内容</li>
            <li>整理后返回给您</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🌍 支持城市")
    cities = ["北京", "上海", "成都", "杭州", "西安", "重庆", "广州", "深圳", 
              "东京", "京都", "首尔", "曼谷", "巴黎", "伦敦", "罗马"]
    
    city_str = "、".join(cities)
    st.markdown(f"<div class='info-card'>{city_str}</div>", unsafe_allow_html=True)
    
    st.markdown("### 💡 示例问题")
    examples = [
        "北京三日游怎么安排？",
        "上海有什么好吃的？",
        "成都景点门票多少？",
        "杭州住宿推荐",
        "西安旅行贴士"
    ]
    for ex in examples:
        st.markdown(f"- {ex}")
    
    if st.button("🗑️ 清除历史", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()

if __name__ == "__main__":
    pass