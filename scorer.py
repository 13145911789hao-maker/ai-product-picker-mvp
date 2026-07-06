def _keyword_score(text, keywords, points_per_hit=5, max_score=25):
    """按照关键词命中数量打分，避免某一种风格天然高分。"""
    hits = [k for k in keywords if k in text]
    return min(len(hits) * points_per_hit, max_score)


def _price_cost_score(price):
    """开发成本/价格带评分：不是越便宜越好，而是看是否适合测试开发。"""
    if price <= 0:
        return 8
    if 49 <= price <= 159:
        return 18
    if 160 <= price <= 229:
        return 14
    if price < 49:
        return 12
    return 8


def score_breakdown(product):
    """
    HermitCreate 多维度选款评分模型 V2。

    核心原则：
    - 风格之间没有天然高低之分。
    - 每个款式是在自己所属风格里，依据外观、细节、实用性、成本、历史市场反馈等维度综合评分。
    - 目前MVP阶段使用标题/价格/测试字段模拟判断；后续可以接入真实销量、点击率、收藏率、退货率、加购率等数据。
    """
    title = product.get("title", "")
    t = title.lower()
    price = product.get("price", 0)
    category = product.get("category", "")
    style_group = product.get("style_group", "")

    # 1. 外观风格识别度：这个款是否有明确的视觉风格，而不是模糊款
    appearance_keywords = [
        "oversize", "boxy", "washed", "vintage", "distressed", "acid wash",
        "cargo", "utility", "deconstruction", "deconstructed", "asymmetric",
        "patchwork", "panel", "layered", "raw edge", "sun faded",
        "graphic", "stripe", "flannel", "rugby", "moto", "racing",
        "做旧", "水洗", "复古", "工装", "解构", "不规则", "拼接", "分割",
        "层次", "廓形", "破坏", "毛边", "褪色", "机车", "赛车"
    ]
    appearance_score = _keyword_score(t, appearance_keywords, points_per_hit=4, max_score=22)

    # 2. 细节设计：有没有可被消费者感知的卖点细节
    detail_keywords = [
        "double zip", "zip", "pocket", "multi pocket", "double knee", "carpenter",
        "rib", "waffle", "heavyweight", "premium", "mesh", "nylon", "shell",
        "hoodie", "vest", "jacket", "straight", "loose", "wide", "cropped",
        "拉链", "多口袋", "双膝", "木匠", "重磅", "高克重", "华夫格",
        "网眼", "尼龙", "直筒", "宽松", "短宽", "马甲", "夹克"
    ]
    detail_score = _keyword_score(t, detail_keywords, points_per_hit=4, max_score=18)

    # 3. 实用性/搭配性：是否适合日常穿、复购、做基础盘
    utility_keywords = [
        "basic", "plain", "essential", "clean", "minimal", "easy care", "relaxed",
        "straight", "tee", "long sleeve", "shirt", "chinos", "cardigan", "polo",
        "基础", "纯色", "百搭", "口粮", "舒适", "通勤", "免烫", "直筒", "衬衫", "针织"
    ]
    utility_score = _keyword_score(t, utility_keywords, points_per_hit=4, max_score=20)

    # 4. 开发成本/可落地性：先用价格模拟，后续可替换为供应商报价、面料难度、打样周期、起订量
    cost_score = _price_cost_score(price)

    # 5. 历史市场销量情况：MVP允许产品数据里手动填 market_sales_score；没有则用中性分
    market_sales_score = product.get("market_sales_score", 12)
    market_sales_score = max(0, min(market_sales_score, 20))

    # 6. 历史风格市场反馈：MVP允许产品数据里手动填 style_feedback_score；没有则用中性分
    style_feedback_score = product.get("style_feedback_score", 10)
    style_feedback_score = max(0, min(style_feedback_score, 15))

    # 7. 类似款市场反应：MVP允许产品数据里手动填 similar_reaction_score；没有则用中性分
    similar_reaction_score = product.get("similar_reaction_score", 5)
    similar_reaction_score = max(0, min(similar_reaction_score, 10))

    total = (
        appearance_score
        + detail_score
        + utility_score
        + cost_score
        + market_sales_score
        + style_feedback_score
        + similar_reaction_score
    )

    return {
        "total": total,
        "style_group": style_group,
        "category": category,
        "appearance_score": appearance_score,
        "detail_score": detail_score,
        "utility_score": utility_score,
        "cost_score": cost_score,
        "market_sales_score": market_sales_score,
        "style_feedback_score": style_feedback_score,
        "similar_reaction_score": similar_reaction_score,
    }


def score(product):
    """保持 main.py 兼容：返回最终总分。"""
    return score_breakdown(product)["total"]
