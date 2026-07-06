import json
from datetime import datetime
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


def build_risk_note(item):
    """生成买手能看懂的风险提示。"""
    breakdown = item["score_breakdown"]
    risks = []

    if breakdown.get("appearance_score", 0) <= 6:
        risks.append("外观识别度偏弱，更适合作为基础盘而不是形象款")
    if breakdown.get("detail_score", 0) <= 6:
        risks.append("设计细节偏少，需要靠版型、面料或价格取胜")
    if breakdown.get("cost_score", 0) <= 12:
        risks.append("开发成本或价格带需要重点核算")
    if breakdown.get("market_sales_score", 0) <= 10:
        risks.append("历史类似款销量数据偏弱，需要小批量测试")

    if not risks:
        return "暂无明显高风险，建议进入下一步选款评审。"

    return "；".join(risks) + "。"


def image_block(item):
    """在 Markdown 报告里显示图片。真实图片链接可显示，测试链接会显示为占位/失效图。"""
    image_url = item.get("image", "")
    title = item.get("title", "商品图片")

    if not image_url:
        return "> 暂无商品图片。"

    return f'<img src="{image_url}" alt="{title}" width="260">'


def generate_markdown_report(items):
    """生成给人看的 Markdown 图片选款报告。"""
    lines = []
    lines.append("# HermitCreate 每日选款评分报告")
    lines.append("")
    lines.append(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("## 一、报告说明")
    lines.append("")
    lines.append("本报告根据 HermitCreate 当前的测试商品库和多维度评分模型自动生成。")
    lines.append("评分不是判断某个风格天然更好，而是判断每个款式在自己所属风格赛道里是否具备开发价值。")
    lines.append("")
    lines.append("> 注意：当前 products.json 里的图片多为测试链接。等你把 image 字段换成真实商品图链接后，报告里会自动显示真实图片。")
    lines.append("")
    lines.append("当前主要参考维度：")
    lines.append("")
    lines.append("- 外观风格识别度")
    lines.append("- 设计细节")
    lines.append("- 实穿性 / 搭配性")
    lines.append("- 开发成本可控性")
    lines.append("- 历史类似款销量表现")
    lines.append("- 所属风格历史反馈")
    lines.append("- 类似款市场反应")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 二、Top 选款清单")
    lines.append("")
    lines.append("| 排名 | 图片 | 商品ID | 款式 | 风格组 | 类目 | 总分 | 建议 |")
    lines.append("|---|---|---|---|---|---|---:|---|")

    for index, item in enumerate(items, start=1):
        thumb = f'<img src="{item.get("image", "")}" width="80">' if item.get("image") else "暂无图片"
        lines.append(
            f"| {index} | {thumb} | {item['product_id']} | {item['title']} | {item['style_group']} | "
            f"{item['category']} | {item['total_score']} | {item['recommendation']} |"
        )

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 三、详细分析")
    lines.append("")

    for index, item in enumerate(items, start=1):
        breakdown = item["score_breakdown"]
        lines.append(f"### {index}. {item['title']}")
        lines.append("")
        lines.append(image_block(item))
        lines.append("")
        lines.append(f"- 商品ID：{item['product_id']}")
        lines.append(f"- 风格组：{item['style_group']}")
        lines.append(f"- 类目：{item['category']}")
        lines.append(f"- 价格：{item['price']}")
        lines.append(f"- 总分：{item['total_score']}")
        lines.append(f"- 开发建议：**{item['recommendation']}**")
        lines.append(f"- 推荐理由：{item['reason']}")
        lines.append(f"- 风险提示：{build_risk_note(item)}")
        lines.append("")
        lines.append("分项评分：")
        lines.append("")
        lines.append(f"- 外观识别度：{breakdown.get('appearance_score', 0)}")
        lines.append(f"- 设计细节：{breakdown.get('detail_score', 0)}")
        lines.append(f"- 实穿搭配：{breakdown.get('utility_score', 0)}")
        lines.append(f"- 成本可控：{breakdown.get('cost_score', 0)}")
        lines.append(f"- 历史销量：{breakdown.get('market_sales_score', 0)}")
        lines.append(f"- 风格反馈：{breakdown.get('style_feedback_score', 0)}")
        lines.append(f"- 类似款反应：{breakdown.get('similar_reaction_score', 0)}")
        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


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

with open("report.md", "w", encoding="utf-8") as f:
    f.write(generate_markdown_report(top_100))

print("✔ HermitCreate 选款评分完成")
print("输出数量:", len(top_100))
print("最高分:", top_100[0]["total_score"] if top_100 else 0)
print("结果文件: output.json")
print("图片报告: report.md")
