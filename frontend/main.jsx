import React, { useEffect, useState } from "react";
import ReactDOM from "react-dom/client";

function App() {
  const [products, setProducts] = useState([]);
  const [trends, setTrends] = useState({});

  useEffect(() => {
    fetch("http://localhost:8000/top-products")
      .then((res) => res.json())
      .then(setProducts);

    fetch("http://localhost:8000/trend-summary")
      .then((res) => res.json())
      .then((data) => setTrends(data.trend_score_by_style || {}));
  }, []);

  return (
    <div style={{ display: "flex", gap: 20, padding: 20 }}>
      <div style={{ flex: 2 }}>
        <h2>Top Products</h2>
        {products.map((p, i) => (
          <div key={i} style={{ padding: 10, borderBottom: "1px solid #333" }}>
            <div><b>{p.title}</b></div>
            <div>Score: {p.total_score}</div>
            <div>Style: {p.style_group}</div>
          </div>
        ))}
      </div>

      <div style={{ flex: 1 }}>
        <h2>Trend</h2>
        {Object.entries(trends).map(([k, v]) => (
          <div key={k} style={{ marginBottom: 8 }}>
            {k}: {v.toFixed(2)}
          </div>
        ))}
      </div>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);