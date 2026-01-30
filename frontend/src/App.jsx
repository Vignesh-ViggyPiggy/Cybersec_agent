import React, { useState, useEffect } from 'react';
import LogInput from './components/LogInput';
import ResultViewer from './components/ResultViewer';
import { analyzeLog, checkHealth } from './api';
import './App.css';

function App() {
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [apiStatus, setApiStatus] = useState(null);

  useEffect(() => {
    // Check API health on mount
    checkHealth()
      .then(data => setApiStatus(data))
      .catch(() => setApiStatus({ status: 'unavailable' }));
  }, []);

  const handleAnalyze = async (logText, useBraveSearch) => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const analysisResult = await analyzeLog(logText, useBraveSearch);
      setResult(analysisResult);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>🛡️ CyberSec Agent</h1>
        <p>AI-Powered Security Log Analysis System</p>
        {apiStatus && (
          <div style={{ 
            marginTop: '1rem', 
            fontSize: '0.85rem',
            color: apiStatus.status === 'healthy' ? '#86efac' : '#fca5a5'
          }}>
            API Status: {apiStatus.status === 'healthy' ? '✓ Online' : '✗ Offline'}
            {apiStatus.bert_healthy !== undefined && (
              <span style={{ marginLeft: '1rem' }}>
                BERT: {apiStatus.bert_healthy ? '✓' : '✗'}
              </span>
            )}
            {apiStatus.search_provider && (
              <span style={{ marginLeft: '1rem', color: '#94a3b8' }}>
                | Search: {apiStatus.search_provider === 'duckduckgo' ? '🦆 DuckDuckGo (Free)' : '🔍 Brave'}
              </span>
            )}
          </div>
        )}
      </header>

      <div className="main-container">
        <LogInput onAnalyze={handleAnalyze} isLoading={isLoading} />
        <ResultViewer result={result} isLoading={isLoading} error={error} />
      </div>

      <footer className="footer">
        <p>
          Powered by LangChain, BERT Anomaly Detection, and DuckDuckGo/Brave Search
        </p>
        <p style={{ marginTop: '0.5rem', fontSize: '0.85rem', opacity: 0.8 }}>
          🔍 Free threat intelligence via DuckDuckGo (no API key required)
        </p>
        <p style={{ marginTop: '0.5rem', fontSize: '0.85rem' }}>
          <a href="http://localhost:8080/docs" target="_blank" rel="noopener noreferrer">
            API Documentation
          </a>
        </p>
      </footer>
    </div>
  );
}

export default App;
