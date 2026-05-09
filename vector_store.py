"""
向量存储模块 - 使用 travel_texts.txt 数据的问答检索
"""
import json
import re
import os
from pathlib import Path

# ===================== 修复：自动获取项目路径，适配公网部署 =====================
# 获取当前文件所在目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRAVEL_TEXTS_PATH = Path(BASE_DIR) / "travel_data" / "travel_texts.txt"

class QAIndex:
    """优化的问答索引"""
    
    def __init__(self):
        self.raw_data = []      # 原始数据
        self.city_index = {}    # 城市索引
        self._load_data()
    
    def _load_data(self):
        """加载 travel_texts.txt 数据"""
        if not TRAVEL_TEXTS_PATH.exists():
            print(f"Warning: {TRAVEL_TEXTS_PATH} not found")
            return
        
        with open(TRAVEL_TEXTS_PATH, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 解析 "城市：北京 | 景点：故宫 | 描述：..." 格式
            item = self._parse_line(line)
            if item:
                self.raw_data.append(item)
                
                # 构建城市索引
                city = item.get('城市', '')
                if city not in self.city_index:
                    self.city_index[city] = []
                self.city_index[city].append(item)
        
        print(f"加载旅游数据: {len(self.raw_data)} 条, {len(self.city_index)} 个城市")
    
    def _parse_line(self, line):
        """解析单行数据"""
        item = {'原始文本': line}
        
        # 按 | 分割
        parts = line.split('|')
        for part in parts:
            part = part.strip()
            if '：' in part:
                key, value = part.split('：', 1)
                item[key.strip()] = value.strip()
            elif ':' in part:
                key, value = part.split(':', 1)
                item[key.strip()] = value.strip()
        
        # 确定类型
        if '景点' in item:
            item['类型'] = '景点'
        elif '美食' in item:
            item['类型'] = '美食'
        elif '旅行贴士' in item:
            item['类型'] = '贴士'
        else:
            item['类型'] = '其他'
        
        return item
    
    def _extract_keywords(self, text):
        """提取关键词"""
        # 移除标点，分词
        text = re.sub(r'[^\w\s]', ' ', str(text))
        words = text.split()
        # 过滤停用词
        stopwords = {'的', '了', '是', '在', '和', '有', '去', '到', '要', '吗', '呢', '吧', '啊', '好', '吗', '这', '那', '个', '些', '什么', '怎么', '如何'}
        return [w for w in words if len(w) >= 2 and w not in stopwords]
    
    def _calculate_score(self, item, query, target_city, target_type):
        """计算匹配分数"""
        score = 0
        query_lower = query.lower()
        query_keywords = self._extract_keywords(query)
        
        # 1. 类型匹配 (+50分)
        if target_type and item.get('类型') == target_type:
            score += 50
        
        # 2. 城市匹配 (+30分)
        if target_city and item.get('城市') == target_city:
            score += 30
        
        # 3. 查询关键词与所有字段匹配
        for key, value in item.items():
            if key == '原始文本':
                continue
            value_keywords = self._extract_keywords(value)
            # 精确匹配
            if query_lower in str(value).lower():
                score += 20
            # 关键词重叠
            overlap = len(set(query_keywords) & set(value_keywords))
            score += overlap * 5
        
        # 4. 景点/美食名称匹配 (+40分)
        name_key = '景点' if item.get('类型') == '景点' else ('美食' if item.get('类型') == '美食' else None)
        if name_key and name_key in item:
            name = item[name_key].lower()
            if query_lower in name or name in query_lower:
                score += 40
        
        return score
    
    def search(self, query, top_k=5, target_city=None, target_type=None):
        """
        搜索旅游数据
        
        Args:
            query: 搜索查询
            top_k: 返回数量
            target_city: 目标城市（可选）
            target_type: 类型筛选（景点/美食/贴士）
        """
        results = []
        
        # 确定搜索范围
        if target_city and target_city in self.city_index:
            candidates = self.city_index[target_city]
        else:
            candidates = self.raw_data
        
        # 评分
        for item in candidates:
            score = self._calculate_score(item, query, target_city, target_type)
            if score > 0:
                results.append((score, item))
        
        # 排序
        results.sort(key=lambda x: -x[0])
        return [r[1] for r in results[:top_k]]
    
    def search_by_city(self, city, data_type=None):
        """
        按城市获取数据
        
        Args:
            city: 城市名
            data_type: 类型筛选（景点/美食/贴士）
        """
        if city not in self.city_index:
            return []
        
        items = self.city_index[city]
        if data_type:
            items = [item for item in items if item.get('类型') == data_type]
        return items


# 全局索引实例
_qa_index = None

def get_qa_index():
    """获取问答索引实例"""
    global _qa_index
    if _qa_index is None:
        _qa_index = QAIndex()
    return _qa_index

def search_travel_data(query, top_k=5, target_city=None, target_type=None):
    """
    搜索旅游数据
    
    Args:
        query: 搜索查询
        top_k: 返回数量
        target_city: 目标城市
        target_type: 类型（景点/美食/贴士）
    """
    index = get_qa_index()
    return index.search(query, top_k, target_city, target_type)

def get_city_data(city, data_type=None):
    """获取指定城市的数据"""
    index = get_qa_index()
    return index.search_by_city(city, data_type)

# 保持向后兼容
def get_vector_store():
    return get_qa_index()