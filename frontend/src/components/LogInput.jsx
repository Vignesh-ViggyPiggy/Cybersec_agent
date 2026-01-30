import React, { useState } from 'react';

const SAMPLE_LOGS = [
  {
    label: 'SSH Brute Force',
    text: 'Failed password for admin from 203.0.113.42 port 55892 ssh2'
  },
  {
    label: 'SQL Injection',
    text: 'apache: GET /admin/config.php?id=1\' OR \'1\'=\'1 HTTP/1.1'
  },
  {
    label: 'Port Scan',
    text: 'firewall: BLOCKED: SRC=198.51.100.50 DST=192.168.1.150 PROTO=TCP DPT=445'
  },
  {
    label: 'Ransomware',
    text: 'antivirus: ALERT: Suspicious file detected: ransomware.exe - Quarantined'
  },
  {
    label: 'Privilege Escalation',
    text: 'system: CRITICAL: Unauthorized privilege escalation attempt by user guest to root'
  }
];

const LogInput = ({ onAnalyze, isLoading }) => {
  const [logText, setLogText] = useState('');
  const [useBraveSearch, setUseBraveSearch] = useState(true);

  const handleSubmit = () => {
    if (logText.trim()) {
      onAnalyze(logText, useBraveSearch);
    }
  };

  const handleClear = () => {
    setLogText('');
  };

  const handleSampleClick = (sampleText) => {
    setLogText(sampleText);
  };

  const handleKeyPress = (e) => {
    if (e.ctrlKey && e.key === 'Enter') {
      handleSubmit();
    }
  };

  return (
    <div className="card input-section">
      <h2>📝 Log Input</h2>
      
      <div className="textarea-container">
        <textarea
          className="log-input"
          placeholder="Paste your security log here...&#10;&#10;Examples:&#10;- Failed password for admin from 203.0.113.42&#10;- SQL injection attempt detected&#10;- Suspicious network traffic on port 445&#10;&#10;Tip: Press Ctrl+Enter to analyze"
          value={logText}
          onChange={(e) => setLogText(e.target.value)}
          onKeyDown={handleKeyPress}
          disabled={isLoading}
        />
        <div className="char-count">
          {logText.length} / 50,000 characters
        </div>
      </div>

      <div className="options">
        <label className="checkbox-label">
          <input
            type="checkbox"
            checked={useBraveSearch}
            onChange={(e) => setUseBraveSearch(e.target.checked)}
            disabled={isLoading}
          />
          <span>Enable threat intelligence search (DuckDuckGo - Free)</span>
        </label>
        <p style={{ fontSize: '0.85rem', color: '#94a3b8', marginTop: '0.5rem', marginLeft: '1.5rem' }}>
          💡 Uses DuckDuckGo (no API key) or Brave Search if configured
        </p>
      </div>

      <div className="button-group">
        <button
          className={`btn btn-primary ${isLoading ? 'loading' : ''}`}
          onClick={handleSubmit}
          disabled={!logText.trim() || isLoading}
        >
          {isLoading ? 'Analyzing...' : '🔍 Analyze Log'}
        </button>
        <button
          className="btn btn-secondary"
          onClick={handleClear}
          disabled={!logText || isLoading}
        >
          Clear
        </button>
      </div>

      <div className="sample-logs">
        <h3>Quick Samples</h3>
        <div className="sample-buttons">
          {SAMPLE_LOGS.map((sample, index) => (
            <button
              key={index}
              className="sample-btn"
              onClick={() => handleSampleClick(sample.text)}
              disabled={isLoading}
            >
              {sample.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default LogInput;
