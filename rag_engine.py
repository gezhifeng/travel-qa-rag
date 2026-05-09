"""
RAG问答引擎 - 使用 travel_texts.txt 数据
1. 千问API分析用户意图
2. 从本地数据检索
3. 格式化返回
"""
import json
import re
from vector_store import search_travel_data, get_city_data

# 支持的城市列表（从travel_texts.txt获取）
SUPPORTED_CITIES = [
    "北京", "上海", "成都", "杭州", "西安", "重庆", "广州", "深圳",
    "南京", "苏州", "武汉", "厦门", "青岛", "大连", "昆明", "丽江",
    "东京", "京都", "首尔", "曼谷", "新加坡", "巴黎", "伦敦", "罗马"
]

# 类型配置
TYPE_CONFIG = {
    "景点": {"icon": "🏛️", "label": "景点推荐"},
    "美食": {"icon": "🍜", "label": "美食推荐"},
    "贴士": {"icon": "💡", "label": "旅行贴士"},
}

# 千问API配置（从config读取）
try:
    from config import QWEN_CONFIG
    QWEN_API_KEY = QWEN_CONFIG.get("api_key", "")
    QWEN_BASE_URL = QWEN_CONFIG.get("base_url", "https://dashscope.aliyuncs.com/compatible-mode/v1")
    QWEN_MODEL = QWEN_CONFIG.get("model", "qwen-plus")
except:
    QWEN_API_KEY = ""
    QWEN_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    QWEN_MODEL = "qwen-plus"


class TravelRAGEngine:
    """旅游问答引擎"""
    
    def __init__(self):
        self.using_api = bool(QWEN_API_KEY)
        
        if self.using_api:
            try:
                import openai
                self.client = openai.OpenAI(
                    api_key=QWEN_API_KEY,
                    base_url=QWEN_BASE_URL
                )
            except Exception as e:
                print(f"OpenAI client init failed: {e}")
                self.client = None
        else:
            self.client = None
        
        # 分析问题的系统提示
        city_list = "、".join(SUPPORTED_CITIES)
        self.analyze_prompt = f"""你是一个旅游问题分析专家。分析用户问题，提取关键信息。

## 支持的城市：
{city_list}

## 分析规则：
1. 从问题中识别城市名（只识别上面列出的城市）
2. 识别问题类型：
   - 景点相关：景点、玩、好玩、好去处、值得去、必去、观光、游览
   - 美食相关：美食、好吃、吃什么、吃啥、餐厅、小吃、特色菜、夜宵
   - 贴士相关：贴士、注意、建议、攻略、季节、最佳时间
3. 如果问综合性问题（如"有什么好玩的"），返回多种类型

## 输出格式（只输出JSON）：
{{
    "city": "城市名" 或 null,
    "types": ["景点", "美食", "贴士"] 或 ["景点"] 或 ["美食"] 等,
    "search_terms": ["检索词1", "检索词2"],
    "question_summary": "问题的简短总结"
}}

## 示例：
用户：杭州住宿建议
输出：{{"city": "杭州", "types": ["贴士"], "search_terms": ["住宿", "酒店"], "question_summary": "杭州住宿推荐"}}

用户：成都美食攻略
输出：{{"city": "成都", "types": ["美食"], "search_terms": ["美食", "小吃", "火锅", "串串"], "question_summary": "成都美食推荐"}}

用户：北京有什么好玩的
输出：{{"city": "北京", "types": ["景点"], "search_terms": ["景点", "好玩"], "question_summary": "北京景点推荐"}}

用户：上海3日游怎么安排
输出：{{"city": "上海", "types": ["景点", "贴士"], "search_terms": ["景点", "行程", "攻略"], "question_summary": "上海旅游攻略"}}

现在分析："""
    
    def analyze_question(self, user_input):
        """使用千问分析用户问题"""
        # 如果没有API配置，使用本地分析
        if not self.client:
            return self._local_analyze(user_input)
        
        try:
            response = self.client.chat.completions.create(
                model=QWEN_MODEL,
                messages=[
                    {"role": "system", "content": self.analyze_prompt},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=300,
                temperature=0.3
            )
            result = response.choices[0].message.content.strip()
            
            # 解析JSON
            try:
                if "```json" in result:
                    result = result.split("```json")[1].split("```")[0]
                elif "```" in result:
                    result = result.split("```")[1].split("```")[0]
                
                analysis = json.loads(result.strip())
                
                # 验证城市
                city = analysis.get('city')
                if city and city not in SUPPORTED_CITIES:
                    analysis['city'] = self._extract_city(user_input)
                
                return analysis
                
            except json.JSONDecodeError:
                return self._local_analyze(user_input)
                
        except Exception as e:
            print(f"API调用失败: {e}")
            return self._local_analyze(user_input)
    
    def _local_analyze(self, user_input):
        """本地分析（无API时使用）"""
        city = self._extract_city(user_input)
        
        # 检测类型
        types = []
        search_terms = []
        
        food_keywords = ['美食', '好吃', '吃什么', '吃啥', '餐厅', '小吃', '特色菜', '夜宵', '火锅', '串串']
        attraction_keywords = ['景点', '玩', '好玩', '好去处', '值得去', '必去', '观光', '游览', '观光']
        tips_keywords = ['贴士', '注意', '建议', '攻略', '季节', '最佳', '安排']
        
        if any(kw in user_input for kw in food_keywords):
            types.append('美食')
            search_terms.extend(['美食', '小吃'])
        if any(kw in user_input for kw in attraction_keywords):
            types.append('景点')
            search_terms.extend(['景点', '好玩'])
        if any(kw in user_input for kw in tips_keywords):
            types.append('贴士')
            search_terms.append('贴士')
        
        if not types:
            types = ['景点']  # 默认景点
        
        return {
            "city": city,
            "types": types,
            "search_terms": list(set(search_terms)) if search_terms else [user_input.replace(city or '', '').strip()],
            "question_summary": user_input
        }
    
    def _extract_city(self, text):
        """提取城市名"""
        for city in SUPPORTED_CITIES:
            if city in text:
                return city
        return None
    
    def search_local_knowledge(self, target_city, types, search_terms, top_k=5):
        """从本地知识库检索"""
        if not target_city:
            return {}
        
        results_by_type = {}
        seen = set()
        
        # 按类型检索
        for data_type in types:
            type_results = []
            
            # 1. 先按类型+城市搜索
            query = f"{target_city} {data_type}"
            results = search_travel_data(query, top_k=top_k * 2, target_city=target_city)
            for r in results:
                if r.get('类型') == data_type and r.get('原始文本') not in seen:
                    seen.add(r.get('原始文本'))
                    type_results.append(r)
            
            # 2. 直接获取该城市的该类型数据
            city_data = get_city_data(target_city, data_type)
            for r in city_data:
                if r.get('原始文本') not in seen:
                    seen.add(r.get('原始文本'))
                    type_results.append(r)
            
            # 3. 用搜索词搜索
            for term in search_terms:
                results = search_travel_data(term, top_k=top_k, target_city=target_city)
                for r in results:
                    if r.get('原始文本') not in seen:
                        seen.add(r.get('原始文本'))
                        type_results.append(r)
            
            results_by_type[data_type] = type_results[:top_k]
        
        return results_by_type
    
    def chat(self, user_input):
        """问答流程"""
        # 1. 分析问题
        analysis = self.analyze_question(user_input)
        city = analysis.get('city')
        types = analysis.get('types', ['景点'])
        search_terms = analysis.get('search_terms', [])
        
        if not city:
            return {
                "answer": self._not_supported_message(),
                "analysis": analysis,
                "sources": [],
                "found": False
            }
        
        # 2. 检索本地数据
        retrieved = self.search_local_knowledge(city, types, search_terms)
        
        # 3. 格式化结果
        if any(retrieved.get(t) for t in types):
            return {
                "answer": self._format_results(city, retrieved),
                "analysis": analysis,
                "sources": [r.get('原始文本') for t in retrieved.values() for r in t],
                "found": True
            }
        else:
            return {
                "answer": self._no_data_message(city),
                "analysis": analysis,
                "sources": [],
                "found": False
            }
    
    def _not_supported_message(self):
        """返回不支持城市的提示"""
        popular = ["北京", "上海", "成都", "杭州", "西安", "重庆", "广州", "深圳"]
        return f"""抱歉，我目前只支持查询部分城市的信息：

📍 **支持的部分热门城市：**
{"、".join(popular)}...

💡 请选择以上城市进行咨询，例如：
• "北京有什么好玩的"
• "上海有什么好吃的"
• "成都景点推荐"
"""
    
    def _no_data_message(self, city):
        """返回无数据的提示"""
        return f"""抱歉，暂未收录 {city} 的详细信息。

💡 您可以换个问题试试：
• "{city}景点推荐"
• "{city}美食攻略"
• "{city}旅行贴士"
"""
    
    def _format_results(self, city, results_by_type):
        """格式化检索结果"""
        parts = []
        
        for data_type in ['景点', '美食', '贴士']:
            items = results_by_type.get(data_type, [])
            if not items:
                continue
            
            config = TYPE_CONFIG.get(data_type, {"icon": "📋", "label": ""})
            icon = config["icon"]
            label = config["label"]
            
            section = f"### {icon} {label}\n\n"
            
            for item in items:
                text = item.get('原始文本', '')
                # 格式化文本，去掉"城市："前缀
                text = re.sub(r'^城市：[^|]+\|\s*', '', text)
                section += f"- {text}\n"
            
            parts.append(section)
        
        return "\n".join(parts)


# 全局实例
rag_engine = None

def get_rag_engine():
    global rag_engine
    if rag_engine is None:
        rag_engine = TravelRAGEngine()
    return rag_engine

def chat_rag(user_input):
    """主要问答函数"""
    engine = get_rag_engine()
    result = engine.chat(user_input)
    return result["answer"]


if __name__ == "__main__":
    # 测试
    engine = TravelRAGEngine()
    
    test_questions = [
        "北京好吃的有什么",
        "成都景点推荐",
        "杭州旅行贴士",
        "上海3日游攻略",
        "西安美食",
    ]
    
    for q in test_questions:
        print(f"\n{'='*60}")
        print(f"问题：{q}")
        result = engine.chat(q)
        print(f"分析：{result['analysis']}")
        print(f"找到数据：{result['found']}")
        print(f"回答：\n{result['answer']}")
