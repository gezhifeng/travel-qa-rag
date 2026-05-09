"""
旅游数据爬虫模块
"""
import json
import time
from pathlib import Path

class TravelDataCrawler:
    """旅游数据爬虫"""
    
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        self.data_dir = Path("travel_data")
        self.data_dir.mkdir(exist_ok=True)
    
    def crawl_all_cities(self):
        """爬取所有城市数据"""
        cities = ["北京", "上海", "成都", "杭州", "西安", "重庆", "广州", "深圳", 
                  "南京", "苏州", "武汉", "厦门", "青岛", "大连", "昆明", "丽江",
                  "东京", "京都", "首尔", "曼谷", "新加坡", "巴黎", "伦敦", "罗马"]
        
        all_data = []
        for city in cities:
            try:
                data = self._get_city_data(city)
                all_data.append(data)
                print(f"已处理: {city}")
                time.sleep(0.3)
            except Exception as e:
                print(f"处理 {city} 失败: {e}")
        
        self.save_data(all_data)
        return all_data
    
    def _get_city_data(self, city):
        """获取城市数据"""
        data = {
            "city": city,
            "attractions": self._get_attractions(city),
            "food": self._get_food(city),
            "hotels": self._get_hotels(),
            "tips": self._get_tips(city)
        }
        return data
    
    def _get_attractions(self, city):
        attractions_db = {
            "北京": [
                {"name": "故宫", "desc": "世界上现存规模最大、保存最为完整的木质结构古建筑之一", "tickets": "60元", "time": "8:30-17:00", "tips": "建议提前网上预约"},
                {"name": "长城", "desc": "中华民族的象征，世界七大奇迹之一", "tickets": "45-65元", "time": "7:00-18:00", "tips": "八达岭人少，慕田峪风景好"},
                {"name": "天坛", "desc": "明清两代皇帝祭天祈谷的场所", "tickets": "34元", "time": "6:00-21:00", "tips": "建议早晨去"},
                {"name": "颐和园", "desc": "中国最大的皇家园林", "tickets": "30元", "time": "6:30-18:00", "tips": "昆明湖泛舟很惬意"}
            ],
            "上海": [
                {"name": "外滩", "desc": "上海最著名的景观，百年历史建筑群", "tickets": "免费", "time": "全天", "tips": "夜景最佳，灯光秀19:00开始"},
                {"name": "东方明珠", "desc": "上海的标志性建筑之一", "tickets": "180元", "time": "9:00-21:00", "tips": "旋转餐厅性价比高"},
                {"name": "豫园", "desc": "江南古典园林的代表", "tickets": "40元", "time": "9:00-16:30", "tips": "城隍庙小吃在旁边"}
            ],
            "成都": [
                {"name": "大熊猫基地", "desc": "全球最大的大熊猫繁育研究基地", "tickets": "55元", "time": "7:30-18:00", "tips": "建议上午去，熊猫活跃"},
                {"name": "宽窄巷子", "desc": "成都最具代表性的历史文化街区", "tickets": "免费", "time": "全天", "tips": "晚上去更有氛围"},
                {"name": "锦里", "desc": "三国文化与四川民俗风情街", "tickets": "免费", "time": "全天", "tips": "美食众多"}
            ],
            "杭州": [
                {"name": "西湖", "desc": "世界文化遗产，中国最美的湖泊之一", "tickets": "免费", "time": "全天", "tips": "苏堤春晓，断桥残雪"},
                {"name": "灵隐寺", "desc": "千年古刹，香火鼎盛", "tickets": "75元", "time": "7:00-18:00", "tips": "飞来峰门票另收"},
                {"name": "宋城", "desc": "大型宋代主题公园", "tickets": "300元", "time": "10:00-21:00", "tips": "《宋城千古情》值得一看"}
            ],
            "西安": [
                {"name": "兵马俑", "desc": "世界第八大奇迹", "tickets": "120元", "time": "8:30-18:00", "tips": "请讲解员很重要"},
                {"name": "大唐芙蓉园", "desc": "展示大唐文化的主题公园", "tickets": "120元", "time": "9:00-21:00", "tips": "《长恨歌》演出强烈推荐"},
                {"name": "回民街", "desc": "西安特色小吃一条街", "tickets": "免费", "time": "全天", "tips": "美食推荐：肉夹馍、羊肉泡馍"}
            ],
            "重庆": [
                {"name": "洪崖洞", "desc": "现实版千与千寻夜景", "tickets": "免费", "time": "全天", "tips": "夜景绝美"},
                {"name": "解放碑", "desc": "重庆地标，商业中心", "tickets": "免费", "time": "全天", "tips": "美食天堂"},
                {"name": "长江索道", "desc": "重庆特色交通工具", "tickets": "20元", "time": "7:30-22:00", "tips": "建议晚上乘坐"}
            ],
            "广州": [
                {"name": "广州塔", "desc": "广州新地标", "tickets": "150元", "time": "9:30-22:00", "tips": "摩天轮套票更值"},
                {"name": "沙面", "desc": "欧洲风情建筑群", "tickets": "免费", "time": "全天", "tips": "拍照圣地"},
                {"name": "早茶", "desc": "广州特色美食文化", "tickets": "50-200元", "time": "6:00-12:00", "tips": "点都德、陶陶居"}
            ],
            "深圳": [
                {"name": "世界之窗", "desc": "世界各国微缩景观", "tickets": "200元", "time": "9:30-22:00", "tips": "晚上有烟火表演"},
                {"name": "欢乐谷", "desc": "大型主题乐园", "tickets": "220元", "time": "9:30-21:00", "tips": "刺激项目众多"}
            ],
            "东京": [
                {"name": "浅草寺", "desc": "东京最古老的寺庙", "tickets": "免费", "time": "全天", "tips": "仲见世购物街必去"},
                {"name": "新宿", "desc": "繁华商业区", "tickets": "免费", "time": "全天", "tips": "购物天堂"},
                {"name": "迪士尼海洋", "desc": "全球唯一的迪士尼海洋乐园", "tickets": "820元", "time": "8:00-22:00", "tips": "需提前预约"}
            ],
            "京都": [
                {"name": "伏见稻荷大社", "desc": "千本鸟居闻名世界", "tickets": "免费", "time": "全天", "tips": "日出时分最美"},
                {"name": "金阁寺", "desc": "金色华丽寺庙", "tickets": "500日元", "time": "9:00-17:00", "tips": "拍照绝佳"}
            ],
            "巴黎": [
                {"name": "埃菲尔铁塔", "desc": "巴黎标志性建筑", "tickets": "26欧", "time": "9:00-23:45", "tips": "黄昏时分登塔最佳"},
                {"name": "卢浮宫", "desc": "世界最大博物馆", "tickets": "17欧", "time": "9:00-18:00", "tips": "周三周五晚上免费"},
                {"name": "凡尔赛宫", "desc": "法国皇室宫殿", "tickets": "21欧", "time": "9:00-18:30", "tips": "花园很大，建议买园内交通票"}
            ],
            "伦敦": [
                {"name": "大本钟", "desc": "英国标志性建筑", "tickets": "免费", "time": "全天", "tips": "维修中，预计2022年完工"},
                {"name": "大英博物馆", "desc": "世界最大博物馆之一", "tickets": "免费", "time": "10:00-17:00", "tips": "中文导览器5磅"},
                {"name": "塔桥", "desc": "伦敦标志性桥梁", "tickets": "10磅", "time": "9:30-17:00", "tips": "可以走玻璃地板"}
            ]
        }
        return attractions_db.get(city, [{"name": "待补充", "desc": "数据收集中", "tickets": "待定", "time": "待定", "tips": "待补充"}])
    
    def _get_food(self, city):
        food_db = {
            "北京": [
                {"name": "北京烤鸭", "desc": "必吃的北京名菜", "shop": "全聚德/四季民福", "price": "150-300元/只"},
                {"name": "炸酱面", "desc": "老北京传统面食", "shop": "海碗居/方砖厂", "price": "20-40元/碗"},
                {"name": "豆汁焦圈", "desc": "北京特色早餐", "shop": "锦馨豆汁店", "price": "10-20元"}
            ],
            "上海": [
                {"name": "生煎包", "desc": "上海特色小吃", "shop": "大壶春/东贤记", "price": "15-30元/份"},
                {"name": "小笼包", "desc": "上海传统点心", "shop": "南翔馒头店", "price": "30-60元"},
                {"name": "本帮菜", "desc": "浓油赤酱的上海味道", "shop": "老吉士", "price": "100-300元/人"}
            ],
            "成都": [
                {"name": "火锅", "desc": "成都名片", "shop": "小龙坎/大龙燚", "price": "80-150元/人"},
                {"name": "串串香", "desc": "成都人的深夜食堂", "shop": "钢管厂五区", "price": "50-100元/人"},
                {"name": "兔头", "desc": "成都特色", "shop": "双流老妈兔头", "price": "10-15元/个"}
            ],
            "杭州": [
                {"name": "东坡肉", "desc": "杭州名菜", "shop": "外婆家/绿茶", "price": "30-50元/份"},
                {"name": "龙井虾仁", "desc": "杭州特色", "shop": "楼外楼", "price": "80-150元"},
                {"name": "片儿川", "desc": "杭州特色面食", "shop": "奎元馆", "price": "25-40元/碗"}
            ],
            "西安": [
                {"name": "肉夹馍", "desc": "陕西第一小吃", "shop": "子午路张记", "price": "10-15元/个"},
                {"name": "羊肉泡馍", "desc": "西安代表美食", "shop": "老孙家/同盛祥", "price": "30-60元/碗"},
                {"name": "凉皮", "desc": "陕西传统小吃", "shop": "魏家凉皮", "price": "8-15元/份"}
            ],
            "重庆": [
                {"name": "火锅", "desc": "重庆名片", "shop": "珮姐/周师兄", "price": "80-150元/人"},
                {"name": "小面", "desc": "重庆人早餐", "shop": "花市豌杂面", "price": "10-20元/碗"},
                {"name": "酸辣粉", "desc": "重庆名小吃", "shop": "好又来", "price": "8-15元/碗"}
            ]
        }
        return food_db.get(city, [{"name": "待补充", "desc": "数据收集中", "shop": "待定", "price": "待定"}])
    
    def _get_hotels(self):
        return [
            {"type": "豪华", "desc": "五星级酒店，交通便利", "price": "800-2000元/晚"},
            {"type": "舒适", "desc": "四星级酒店，性价比高", "price": "300-600元/晚"},
            {"type": "经济", "desc": "连锁酒店，经济实惠", "price": "100-300元/晚"}
        ]
    
    def _get_tips(self, city):
        tips_db = {
            "北京": ["最佳季节：春秋两季", "建议游玩：3-5天", "注意事项：景点需提前预约"],
            "上海": ["最佳季节：3-5月/9-11月", "建议游玩：2-4天", "注意事项：外滩观景注意安全"],
            "成都": ["最佳季节：3-6月/9-11月", "建议游玩：3-5天", "注意事项：吃辣量力而行"],
            "杭州": ["最佳季节：4-5月", "建议游玩：2-3天", "注意事项：西湖周边停车贵"],
            "西安": ["最佳季节：3-5月/9-11月", "建议游玩：3-5天", "注意事项：回民街尊重饮食习惯"],
            "重庆": ["最佳季节：春秋", "建议游玩：3-4天", "注意事项：导航可能不准，多问路"],
            "东京": ["最佳季节：3-4月赏樱", "建议游玩：4-5天", "注意事项：提前买JR Pass"],
            "巴黎": ["最佳季节：4-10月", "建议游玩：3-5天", "注意事项：小偷较多注意安全"]
        }
        return tips_db.get(city, ["建议游玩2-4天", "提前查看天气预报"])
    
    def save_data(self, data):
        """保存数据到本地"""
        with open(self.data_dir / "travel_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"数据已保存到 {self.data_dir / 'travel_data.json'}")
        
        # 生成文本格式用于检索
        texts = self.convert_to_texts(data)
        with open(self.data_dir / "travel_texts.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(texts))
        print(f"文本数据已保存")
        return texts
    
    def convert_to_texts(self, data):
        """转换为可检索文本"""
        texts = []
        for city_data in data:
            city = city_data["city"]
            for attr in city_data["attractions"]:
                texts.append(f"城市：{city} | 景点：{attr['name']} | 描述：{attr['desc']} | 门票：{attr['tickets']} | 时间：{attr['time']} | 提示：{attr['tips']}")
            for food in city_data["food"]:
                texts.append(f"城市：{city} | 美食：{food['name']} | 介绍：{food['desc']} | 店铺：{food['shop']} | 人均：{food['price']}")
            for tip in city_data["tips"]:
                texts.append(f"城市：{city} | 旅行贴士：{tip}")
        return texts

# 扩展数据
EXTENDED_DATA = """
【北京旅游指南】故宫门票60元需预约 | 长城建议去八达岭或慕田峪 | 天坛建议早晨去 | 北京烤鸭推荐四季民福

【上海旅游指南】外滩夜景必看 | 东方明珠180元 | 豫园40元 | 生煎包推荐大壶春 | 小笼包推荐南翔馒头店

【成都旅游指南】大熊猫基地55元建议上午去 | 宽窄巷子免费 | 火锅推荐小龙坎 | 串串香推荐钢管厂五区

【杭州旅游指南】西湖免费环湖骑行 | 灵隐寺75元 | 宋城300元含演出 | 东坡肉外婆家必吃

【西安旅游指南】兵马俑120元请讲解 | 华清宫长恨歌演出震撼 | 回民街美食众多 | 肉夹馍子午路张记最正宗

【重庆旅游指南】洪崖洞夜景绝美 | 长江索道20元 | 火锅推荐珮姐 | 小面花市豌杂面必吃

【东京旅游指南】浅草寺免费 | 新宿购物天堂 | 迪士尼海洋需预约 | 建议买JR Pass

【巴黎旅游指南】埃菲尔铁塔26欧黄昏最佳 | 卢浮宫17欧 | 凡尔赛宫21欧 | 注意防盗
"""

if __name__ == "__main__":
    crawler = TravelDataCrawler()
    crawler.crawl_all_cities()
    print("数据爬取完成！")