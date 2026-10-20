export default function Counter({
  count,
  history,
  onIncrement,
  onDecrement,
  showHistory,
  showControls,
}) {
  return (
    <div>
      <h1>Click Counter</h1>

      <h2>{count}</h2>

      {showControls && (
        <div>
          <button onClick={onDecrement}>-1</button>
          <button onClick={onIncrement}>+1</button>
        </div>
      )}

      {showHistory && (
        <p>{history.join(" → ") || "No clicks yet"}</p>
      )}
    </div>
  );
}