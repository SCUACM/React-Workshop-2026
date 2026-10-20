import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Counter from "./Counter";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={
            <>
              <Counter showHistory={false} showControls={true}/>
              <Link to="/history">
                View History →
              </Link>
            </>
          }
        />
        <Route
          path="/history"
          element={
            <>
              <Counter showHistory={true} showControls={false}/>
              <Link to="/">
                ← Back
              </Link>
            </>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}