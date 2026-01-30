import React from 'react';

const getSeverityIcon = (severity) => {
  switch (severity) {
    case 'CRITICAL':
      return '🔴';
    case 'HIGH':
      return '🟠';
    case 'MEDIUM':
      return '🟡';
    case 'LOW':
      return '🟢';
    case 'INFO':
      return '🔵';
    default:
      return '⚪';
  }
};

const ResultViewer = ({ result, isLoading, error }) => {
  if (isLoading) {
    return (
      <div className="card results-section">
        <h2>📊 Analysis Results</h2>
        <div className="loading-spinner">
          <svg viewBox="0 0 50 50">
            <circle
              cx="25"
              cy="25"
              r="20"
              fill="none"
              stroke="currentColor"
              strokeWidth="4"
              strokeDasharray="80, 200"
            />
          </svg>
          <p>Analyzing log with AI agent...</p>
          <p style={{ fontSize: '0.9rem', marginTop: '0.5rem', opacity: 0.7 }}>
            Running BERT anomaly detection and threat intelligence search...
          </p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card results-section">
        <h2>📊 Analysis Results</h2>
        <div className="error-message">
          <span style={{ fontSize: '1.5rem' }}>⚠️</span>
          <div>
            <strong>Error:</strong>
            <p style={{ marginTop: '0.5rem' }}>{error}</p>
          </div>
        </div>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="card results-section">
        <h2>📊 Analysis Results</h2>
        <div className="empty-state">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <p>No analysis yet</p>
          <p style={{ fontSize: '0.9rem', marginTop: '0.5rem' }}>
            Enter a log and click "Analyze Log" to get started
          </p>
        </div>
      </div>
    );
  }

  const confidencePercent = (result.confidence_score * 100).toFixed(1);

  return (
    <div className="card results-section">
      <h2>📊 Analysis Results</h2>

      <div className="result-card">
        <div className="result-header">
          <div className={`severity-badge severity-${result.severity}`}>
            <span>{getSeverityIcon(result.severity)}</span>
            <span>{result.severity}</span>
          </div>
          
          <h3>{result.threat_type}</h3>
          
          <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
            Confidence: {confidencePercent}%
          </div>
          <div className="confidence-bar">
            <div 
              className="confidence-fill" 
              style={{ width: `${confidencePercent}%` }}
            />
          </div>
        </div>

        {result.explanation && (
          <div className="result-section">
            <h4>🔍 Detailed Explanation</h4>
            <p>{result.explanation}</p>
          </div>
        )}

        {result.bert_data && (
          <div className="result-section">
            <h4>🤖 BERT Anomaly Detection</h4>
            <div style={{ 
              background: 'rgba(0,0,0,0.2)', 
              padding: '1rem', 
              borderRadius: '8px',
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
              gap: '1rem'
            }}>
              <div>
                <div style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>Anomaly Score</div>
                <div style={{ fontSize: '1.3rem', fontWeight: 'bold', color: result.bert_data.is_anomaly ? '#f87171' : '#86efac' }}>
                  {result.bert_data.anomaly_score.toFixed(2)}
                </div>
              </div>
              <div>
                <div style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>Threshold</div>
                <div style={{ fontSize: '1.3rem', fontWeight: 'bold' }}>
                  {result.bert_data.threshold.toFixed(2)}
                </div>
              </div>
              <div>
                <div style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>Status</div>
                <div style={{ fontSize: '1.1rem', fontWeight: 'bold', color: result.bert_data.is_anomaly ? '#f87171' : '#86efac' }}>
                  {result.bert_data.is_anomaly ? '⚠️ Anomalous' : '✓ Normal'}
                </div>
              </div>
              <div>
                <div style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>Confidence</div>
                <div style={{ fontSize: '1.3rem', fontWeight: 'bold' }}>
                  {result.bert_data.confidence.toFixed(1)}%
                </div>
              </div>
            </div>
          </div>
        )}

        {result.search_sources && result.search_sources.length > 0 && (
          <div className="result-section">
            <h4>🌐 Threat Intelligence Sources</h4>
            {result.search_query && (
              <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '0.75rem' }}>
                Search query: <em>"{result.search_query}"</em>
              </p>
            )}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {result.search_sources.map((source, index) => (
                <div key={index} style={{
                  background: 'rgba(0,0,0,0.2)',
                  padding: '0.75rem',
                  borderRadius: '8px',
                  borderLeft: '3px solid var(--primary-color)'
                }}>
                  <div style={{ 
                    fontSize: '0.95rem', 
                    fontWeight: 'bold',
                    marginBottom: '0.25rem'
                  }}>
                    {index + 1}. <a 
                      href={source.url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      style={{ 
                        color: 'var(--primary-color)', 
                        textDecoration: 'none',
                        wordBreak: 'break-word'
                      }}
                      onMouseOver={(e) => e.target.style.textDecoration = 'underline'}
                      onMouseOut={(e) => e.target.style.textDecoration = 'none'}
                    >
                      {source.title}
                    </a>
                  </div>
                  <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '0.25rem' }}>
                    🔗 {source.url}
                  </div>
                  <div style={{ fontSize: '0.9rem' }}>
                    {source.snippet}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {result.indicators_of_compromise && result.indicators_of_compromise.length > 0 && (
          <div className="result-section">
            <h4>🎯 Indicators of Compromise</h4>
            <ul className="ioc-list">
              {result.indicators_of_compromise.map((ioc, index) => (
                <li key={index} className="ioc-item">
                  {ioc}
                </li>
              ))}
            </ul>
          </div>
        )}

        {result.recommended_actions && result.recommended_actions.length > 0 && (
          <div className="result-section">
            <h4>✅ Recommended Actions</h4>
            <ul className="action-list">
              {result.recommended_actions.map((action, index) => (
                <li key={index} className="action-item">
                  {index + 1}. {action}
                </li>
              ))}
            </ul>
          </div>
        )}

        {result.agent_summary && (
          <div className="result-section">
            <h4>🎯 Executive Summary (LangChain Agent)</h4>
            <div style={{
              background: 'linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(139, 92, 246, 0.1))',
              padding: '1rem',
              borderRadius: '8px',
              borderLeft: '4px solid var(--primary-color)'
            }}>
              <p style={{ margin: 0 }}>{result.agent_summary}</p>
            </div>

            {result.agent_actions && result.agent_actions.length > 0 && (
              <div style={{ marginTop: '1rem' }}>
                <div style={{ 
                  fontSize: '0.9rem', 
                  fontWeight: 'bold', 
                  color: 'var(--text-secondary)',
                  marginBottom: '0.5rem'
                }}>
                  🔧 Agent made {result.agent_actions.length} additional tool call{result.agent_actions.length > 1 ? 's' : ''}:
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  {result.agent_actions.map((action, index) => (
                    <div key={index} style={{
                      background: 'rgba(0,0,0,0.2)',
                      padding: '0.75rem',
                      borderRadius: '6px',
                      fontSize: '0.9rem'
                    }}>
                      <div style={{ fontWeight: 'bold', marginBottom: '0.25rem' }}>
                        {index + 1}. Used tool: <span style={{ color: 'var(--primary-color)' }}>{action.tool}</span>
                      </div>
                      <div style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
                        Input: {action.tool_input.substring(0, 100)}{action.tool_input.length > 100 ? '...' : ''}
                      </div>
                      <details style={{ marginTop: '0.25rem' }}>
                        <summary style={{ cursor: 'pointer', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                          View observation
                        </summary>
                        <div style={{ 
                          marginTop: '0.5rem', 
                          padding: '0.5rem', 
                          background: 'rgba(0,0,0,0.3)', 
                          borderRadius: '4px',
                          fontSize: '0.8rem',
                          whiteSpace: 'pre-wrap'
                        }}>
                          {action.observation}
                        </div>
                      </details>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {result.raw_analysis && (
          <details style={{ marginTop: '1rem' }}>
            <summary style={{ cursor: 'pointer', color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
              View Raw Analysis
            </summary>
            <pre style={{ 
              marginTop: '0.5rem', 
              padding: '1rem', 
              background: 'rgba(0,0,0,0.3)', 
              borderRadius: '4px',
              overflow: 'auto',
              fontSize: '0.85rem',
              whiteSpace: 'pre-wrap'
            }}>
              {result.raw_analysis}
            </pre>
          </details>
        )}
      </div>
    </div>
  );
};

export default ResultViewer;
