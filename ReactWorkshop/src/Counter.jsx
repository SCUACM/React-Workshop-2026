import { useState } from "react";

export default function Counter({ showHistory, showControls }) {
  const [count, setCount] = useState(0);
  const [history, setHistory] = useState([]);

  const increment = () => {
    const next = count + 1;
    setCount(next);
    setHistory([...history, next]);
  };

  const decrement = () => {
    const next = count - 1;
    setCount(next);
    setHistory([...history, next])
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


      {showHistory && (
        <p>
          {history.join(" → ") || "No clicks yet"}
        </p>
      )}
    </div>
  );
}