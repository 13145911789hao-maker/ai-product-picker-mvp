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


# ========== 2.0 新增：风格趋势映射 ==========
STYLE_TREND_MAP = {
    "streetwear_us": ["oversize", "graphic", "washed", "cargo", "hoodie", "boxy"],
    "deconstruction": ["deconstruction", "asymmetric", "patchwork", "raw edge", "irregular", "解构", "拼接", "不规则"],
    "commuter_basic": ["plain", "basic", "essential", "clean", "shirt", "tee", "通勤", "基础"],
    "utility_workwear": ["utility", "workwear", "cargo", "pocket", "carpenter", "工装", "多口袋"],
    "vintage_washed": ["vintage", "washed", "distressed", "faded", "复古", "水洗", "做旧"]
}


def _trend_score(t, style_group):
    """根据风格组做轻量趋势匹配，不改变原有评分体系，只做加权补充。"""
    if not style_group:
        return 0

    keywords = STYLE_TREND_MAP.get(style_group, [])
    return _keyword_score(t, keywords, points_per_hit=2, max_score=8)


def score_breakdown(product):
    """
    HermitCreate 多维度选款评分模型 V2 → V2.1

    upgrade:
    - 增加 trend_score（风格趋势匹配度）
    - 保持原有评分结构稳定
    """
    title = product.get("title", "")
    t = title.lower()
    price = product.get("price", 0)
    category = product.get("category", "")
    style_group = product.get("style_group", "")

    # 1. 外观风格识别度
    appearance_keywords = [
        "oversize", "boxy", "washed", "vintage", "distressed", "acid wash",
        "cargo", "utility", "deconstruction", "deconstructed", "asymmetric",
        "patchwork", "panel", "layered", "raw edge", "sun faded",
        "graphic", "stripe", "flannel", "rugby", "moto", "racing",
        "做旧", "水洗", "复古", "工装", "解构", "不规则", "拼接", "分割",
        "层次", "廓形", "破坏", "毛边", "褪色", "机车", "赛车"
    ]
    appearance_score = _keyword_score(t, appearance_keywords, points_per_hit=4, max_score=22)

    # 2. 细节设计
    detail_keywords = [
        "double zip", "zip", "pocket", "multi pocket", "double knee", "carpenter",
        "rib", "waffle", "heavyweight", "premium", "mesh", "nylon", "shell",
        "hoodie", "vest", "jacket", "straight", "loose", "wide", "cropped",
        "拉链", "多口袋", "双膝", "木匠", "重磅", "高克重", "华夫格",
        "网眼", "尼龙", "直筒", "宽松", "短宽", "马甲", "夹克"
    ]
    detail_score = _keyword_score(t, detail_keywords, points_per_hit=4, max_score=18)

    # 3. 实用性
    utility_keywords = [
        "basic", "plain", "essential", "clean", "minimal", "easy care", "relaxed",
        "straight", "tee", "long sleeve", "shirt", "chinos", "cardigan", "polo",
        "基础", "纯色", "百搭", "口粮", "舒适", "通勤", "免烫", "直筒", "衬衫", "针织"
    ]
    utility_score = _keyword_score(t, utility_keywords, points_per_hit=4, max_score=20)

    # 4. 成本
    cost_score = _price_cost_score(price)

    # 5. 市场数据
    market_sales_score = max(0, min(product.get("market_sales_score", 12), 20))
    style_feedback_score = max(0, min(product.get("style_feedback_score", 10), 15))
    similar_reaction_score = max(0, min(product.get("similar_reaction_score", 5), 10))

    # 6. 2.0新增：趋势匹配
    trend_score = _trend_score(t, style_group)

    total = (
        appearance_score
        + detail_score
        + utility_score
        + cost_score
        + market_sales_score
        + style_feedback_score
        + similar_reaction_score
        + trend_score
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
        "trend_score": trend_score,
    }


def score(product):
    return score_breakdown(product)["total"]