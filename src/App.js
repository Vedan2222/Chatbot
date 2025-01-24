import React, { useState } from "react";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [responses, setResponses] = useState([]);
  const [error, setError] = useState(null);

  const handleQuery = async () => {
    try {
      const response = await fetch("http://localhost:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      // Handle non-2xx responses
      if (!response.ok) {
        throw new Error("Server responded with an error");
      }

      const data = await response.json();
      setResponses([...responses, { query, response: data.response }]);
      setQuery("");
      setError(null);  // Reset any previous error state
    } catch (err) {
      console.error("Error:", err);
      setError("Failed to fetch from the server. Please try again.");
    }
  };

  return (
    <div className="app">
      <h1>Chatbot</h1>
      {error && <div className="error">{error}</div>} {/* Display error if any */}
      <div className="chat-container">
        {responses.map((item, index) => (
          <div key={index}>
            <p><strong>You:</strong> {item.query}</p>
            <p><strong>Bot:</strong> {item.response}</p>
          </div>
        ))}
      </div>
      <div className="input-container">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask something..."
        />
        <button onClick={handleQuery}>Send</button>
      </div>
    </div>
  );
}

export default App;
