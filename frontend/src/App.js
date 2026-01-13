import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('Loading...');
  const [timestamp, setTimestamp] = useState('');
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchMessage();
  }, []);

  const fetchMessage = async () => {
    try {
      const response = await fetch('/api/hello');
      if (!response.ok) {
        throw new Error('Failed to fetch from backend');
      }
      const data = await response.json();
      setMessage(data.message);
      setTimestamp(data.timestamp);
      setError(null);
    } catch (err) {
      setError('Could not connect to backend. Using mock data.');
      setMessage('Hello from React Frontend!');
      setTimestamp(new Date().toISOString());
    }
  };

  return (
    <div className="App">
      <div className="container">
        <h1>🚀 DORA Metrics Demo</h1>
        <div className="card">
          <h2>Backend Status</h2>
          <p className="message">{message}</p>
          <p className="timestamp">Last updated: {timestamp}</p>
          {error && <p className="error">{error}</p>}
        </div>
        
        <div className="card">
          <h2>📊 Features</h2>
          <ul>
            <li>✅ Spring Boot Backend</li>
            <li>✅ React Frontend</li>
            <li>✅ Docker Containers</li>
            <li>✅ GitHub Actions CI/CD</li>
            <li>✅ DORA Metrics Tracking</li>
            <li>✅ Power BI Integration</li>
          </ul>
        </div>

        <button onClick={fetchMessage} className="refresh-btn">
          🔄 Refresh Data
        </button>
      </div>
    </div>
  );
}

export default App;
