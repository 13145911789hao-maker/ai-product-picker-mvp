import React, { useEffect, useState } from "react";

export default function App() {
  const [products, setProducts] = useState([]);
  const [trends, setTrends] = useState({});
  const [activeStyle, setActiveStyle] = useState("all");

  useEffect(() => {
    fetch("http://localhost:8000/top-products")
      .then((res) => res.json())
      .then(setProducts);

    fetch("http://localhost:8000/trend-summary")
      .then((res) => res.json())
      .then((data) => setTrends(data.trend_score_by_style || {}));
  }, []);

  const filtered =
    activeStyle === "all"
      ? products
      : products.filter((p) => p.style_group === activeStyle);

  return (
    <div style={{ display: "flex", height: "100vh", background: "#0f0f10", color: "#fff" }}>
      {/* Sidebar */}
      <div style={{ width: 260, padding: 20, background: "#141416" }}>
        <h2>HermitCreate 3.2</h2>
        <p style={{ opacity: 0.6 }}>AI Buying Studio</p>

        <hr style={{ margin: "16px 0" }} />

        <button onClick={() => setActiveStyle("all")} style={btnStyle}>All</button>

        {Object.keys(trends).map((style) => (
          <button
            key={style}
            onClick={() => setActiveStyle(style)}
            style={btnStyle}
          >
            {style}
          </button>
        ))}
      </div>

      {/* Main */}
      <div style={{ flex: 1, padding: 20, overflowY: "auto" }}>
        <h1>Product Explorer</h1>
        <p>Smart AI-curated selection for HermitCreate</p>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 16 }}>
          {filtered.map((p, i) => (
            <div key={i} style={cardStyle}>
              <div style={{ fontWeight: "bold" }}>{p.title}</div>
              <div>Score: {p.total_score}</div>
              <div style={{ fontSize: 12, opacity: 0.7 }}>{p.style_group}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

const btnStyle = {
  display: "block",
  width: "100%",
  marginBottom: 8,
  padding: 10,
  background: "#2b2b30",
  border: "none",
  color: "white",
  borderRadius: 8,
  cursor: "pointer"
};

const cardStyle = {
  background: "#1c1c1f",
  padding: 12,
  borderRadius: 12
};