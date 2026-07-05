def tag(product):
    title = product.get("title", "")

    t = title.lower()

    # 美式街头 / streetwear
    if any(k in t for k in ["street", "streetwear", "oversize", "hoodie", "sweatshirt", "cargo", "denim", "vintage", "washed", "hiphop", "skater"]):
        return "美式街头风"

    # 基础款 / essentials
    if any(k in t for k in ["basic", "basics", "essential", "plain", "simple", "基础", "纯色", "t恤", "tee"]):
        return "基础百搭"

    # 通勤 / 简约
    if any(k in t for k in ["minimal", "simple", "clean", "workwear", "通勤"]):
        return "极简通勤"

    # 休闲运动
    if any(k in t for k in ["sport", "sports", "jogger", "casual", "休闲"]):
        return "休闲运动"

    # 韩系（保留兼容）
    if any(k in t for k in ["korean", "韩", "韩系"]):
        return "韩系风"

    return "其他风格"