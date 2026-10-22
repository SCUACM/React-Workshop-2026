import { useState, useEffect } from "react";

export default function Counter({ showHistory, showControls }) {
  const [count, setCount] = useState(0);
  const [history, setHistory] = useState([]);

  const increment = () => {
    const next = count + 1;
    setCount(next);
    setHistory([...history, next]);
    fetch("http://127.0.0.1:8080/firebase/set", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        current_value: next,
        history: [...history, next],
      }),
    }).catch((err) => console.error("Failed to update firebase data:", err));
  };

  const decrement = () => {
    const next = count - 1;
    setCount(next);
    setHistory([...history, next]);
    fetch("http://127.0.0.1:8080/firebase/set", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        current_value: next,
        history: [...history, next],
      }),
    }).catch((err) => console.error("Failed to update firebase data:", err));
  };

  return (
    <div>
      <h1>Click Counter</h1>

      <h2>{count}</h2>

      {showControls && (
        <div>
          <button onClick={decrement}>-1</button>
          <button onClick={increment}>+1</button>
        </div>
      )}

      {showHistory && <p>{history.join(" → ") || "No clicks yet"}</p>}
    </div>
  );
}
