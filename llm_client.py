import dashscope
from dashscope import Generation
from rag_engine import retrieve

# 你的千问API KEY
DASHSCOPE_API_KEY = "sk-6937850a78b34ac5acb8bd6920bfd2d1"
dashscope.api_key = DASHSCOPE_API_KEY

def chat_rag(query):
    context = retrieve(query)
    
    prompt = f"""
    你是专业旅行顾问，根据提供的真实资料回答问题。
    不要编造信息，回答实用、清晰、有条理。

    真实参考资料：
    {context}

    用户问题：{query}
    """

    response = Generation.call(
        model="qwen-turbo",
        messages=[{"role": "user", "content": prompt}],
        result_format="message"
    )
    return response.output.choices[0].message.content