import json
from scorer import score
from tagger import tag

# 读取商品数据
with open("products.json", "r", encoding="utf-8") as f:
    products = json.load(f)

results = []

# 打分 + 标签
for p in products:
    p["score"] = score(p)
    p["tag"] = tag(p)
    results.append(p)

# 排序
results = sorted(results, key=lambda x: x["score"], reverse=True)

# 取前100个（MVP阶段可能不足100）
top_100 = results[:100]

# 输出
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(top_100, f, ensure_ascii=False, indent=2)

print("✔ 选款完成，输出数量:", len(top_100))