import json
from scorer import score_breakdown
from tagger import tag


def get_recommendation(total_score):
    """根据总分给出开发建议。"""
    if total_score >= 85:
        return "强烈建议开发"
    if total_score >= 75:
        return "建议开发"
    if total_score >= 65:
        return "可小批量测试"
    return "暂缓开发"


def build_reason(breakdown):
    """根据分项分数生成简单推荐理由。"""
    reasons = []

    if breakdown.get("appearance_score", 0) >= 16:
        reasons.append("外观识别度高")
    if breakdown.get("detail_score", 0) >= 14:
        reasons.append("设计细节较强")
    if breakdown.get("utility_score", 0) >= 16:
        reasons.append("实穿性和搭配性好")
    if breakdown.get("cost_score", 0) >= 16:
        reasons.append("开发成本相对可控")
    if breakdown.get("market_sales_score", 0) >= 15:
        reasons.append("历史类似款销量表现较好")
    if breakdown.get("style_feedback_score", 0) >= 12:
        reasons.append("所属风格历史反馈较好")
    if breakdown.get("similar_reaction_score", 0) >= 8:
        reasons.append("类似款市场反应积极")

    if not reasons:
        reasons.append("当前数据表现中性，建议补充更多市场反馈后再判断")

    return "，".join(reasons) + "。"


# 读取商品数据
with open("products.json", "r", encoding="utf-8") as f:
    products = json.load(f)

results = []

for product in products:
    breakdown = score_breakdown(product)
    total_score = breakdown["total"]

    result = {
        "product_id": product.get("product_id", ""),
        "title": product.get("title", ""),
        "category": product.get("category", ""),
        "style_group": product.get("style_group", ""),
        "tag": tag(product),
        "price": product.get("price", 0),
        "image": product.get("image", ""),
        "total_score": total_score,
        "recommendation": get_recommendation(total_score),
        "reason": build_reason(breakdown),
        "score_breakdown": {
            "appearance_score": breakdown.get("appearance_score", 0),
            "detail_score": breakdown.get("detail_score", 0),
            "utility_score": breakdown.get("utility_score", 0),
            "cost_score": breakdown.get("cost_score", 0),
            "market_sales_score": breakdown.get("market_sales_score", 0),
            "style_feedback_score": breakdown.get("style_feedback_score", 0),
            "similar_reaction_score": breakdown.get("similar_reaction_score", 0),
        },
        "raw_product_data": product,
    }

    results.append(result)

# 按总分从高到低排序
results = sorted(results, key=lambda x: x["total_score"], reverse=True)

# 输出 Top 100
top_100 = results[:100]

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(top_100, f, ensure_ascii=False, indent=2)

print("✔ HermitCreate 选款评分完成")
print("输出数量:", len(top_100))
print("最高分:", top_100[0]["total_score"] if top_100 else 0)
print("结果文件: output.json")
