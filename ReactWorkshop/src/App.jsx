import { useState } from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Counter from "./Counter";

export default function App() {
  const [count, setCount] = useState(0);
  const [history, setHistory] = useState([]);

  const change = (delta) => {
    const next = count + delta;
    setCount(next);
    setHistory([...history, next]);
  };

  const shared = {
    count,
    history,
    onIncrement: () => change(1),
    onDecrement: () => change(-1),
  };

  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={
            <>
              <Counter {...shared} showHistory={false} showControls={true} />
              <Link to="/history">View History →</Link>
            </>
          }
        />
        <Route
          path="/history"
          element={
            <>
              <Counter {...shared} showHistory={true} showControls={false} />
              <Link to="/">← Back</Link>
            </>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}