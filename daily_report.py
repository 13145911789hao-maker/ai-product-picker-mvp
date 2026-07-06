import json
from datetime import datetime
from collections import defaultdict

DATA_PATH = "output.json"
REPORT_PATH = "daily_report.md"


def load_data():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def build_report(data):
    if not data:
        return "No data available"

    # sort by score
    data_sorted = sorted(data, key=lambda x: x.get("total_score", 0), reverse=True)

    top_10 = data_sorted[:10]

    # trend summary
    trend = defaultdict(list)
    for item in data:
        style = item.get("style_group", "unknown")
        trend[style].append(item.get("total_score", 0))

    trend_avg = {k: sum(v)/len(v) for k, v in trend.items() if v}

    report = []
    report.append(f"# HermitCreate Daily Report - {datetime.now().strftime('%Y-%m-%d')}")
    report.append("")

    report.append("## 🔥 Top 10 Recommended Products")

    for i, p in enumerate(top_10, 1):
        report.append(f"### {i}. {p.get('title')} (Score: {p.get('total_score')})")
        report.append(f"- Style: {p.get('style_group')}")
        report.append(f"- Price: {p.get('price')}")
        if p.get('image_url'):
            report.append(f"![img]({p.get('image_url')})")
        report.append("")

    report.append("## 📊 Trend Overview")
    for k, v in sorted(trend_avg.items(), key=lambda x: x[1], reverse=True):
        report.append(f"- {k}: {v:.2f}")

    report.append("")
    report.append("## 🧠 Insight")
    report.append("- Focus on high-trend + mid-cost products")
    report.append("- Prioritize streetwear_us + deconstruction clusters")

    return "\n".join(report)


def run():
    data = load_data()
    report = build_report(data)

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report)

    print("Daily report generated.")


if __name__ == "__main__":
    run()