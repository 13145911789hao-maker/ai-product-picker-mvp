def score(product):
    title = product.get("title", "")
    price = product.get("price", 0)

    score = 0

    # 💰 价格偏好（HermitCreate偏中低价快时尚）
    if price < 80:
        score += 35
    elif price < 150:
        score += 25
    else:
        score += 10

    # 🧥 美式街头核心权重
    street_keywords = [
        "oversize", "hoodie", "sweatshirt", "cargo", "denim",
        "vintage", "washed", "street", "streetwear", "hiphop",
        "skater", "grunge"
    ]

    # 👕 基础款
    basic_keywords = [
        "basic", "plain", "essential", "tee", "tshirt", "基础",
        "纯色", "百搭", "简约"
    ]

    # 🧠 通勤/极简
    minimal_keywords = [
        "minimal", "clean", "workwear", "通勤", "简约"
    ]

    t = title.lower()

    if any(k in t for k in street_keywords):
        score += 40

    if any(k in t for k in basic_keywords):
        score += 25

    if any(k in t for k in minimal_keywords):
        score += 15

    # 🔥 品牌增强：HermitCreate偏“街头+基础”
    if any(k in t for k in ["oversize", "cargo", "denim"]):
        score += 10

    return score