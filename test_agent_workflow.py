#!/usr/bin/env python3
"""
Test script for the enhanced CyberSec Agent with LangChain agent at the end
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.agent.cybersec_agent import CyberSecAgent

def test_agent():
    print("="*70)
    print("Testing Enhanced CyberSec Agent with LangChain ReAct Agent")
    print("="*70)
    
    # Test log
    test_log = """
    2024-01-30 14:23:45 CRITICAL: Multiple failed SSH login attempts detected
    2024-01-30 14:23:46 Failed password for admin from 203.0.113.42 port 55892 ssh2
    2024-01-30 14:23:47 Failed password for admin from 203.0.113.42 port 55893 ssh2
    2024-01-30 14:23:48 Failed password for admin from 203.0.113.42 port 55894 ssh2
    2024-01-30 14:23:49 Failed password for root from 203.0.113.42 port 55895 ssh2
    2024-01-30 14:23:50 Failed password for root from 203.0.113.42 port 55896 ssh2
    2024-01-30 14:23:51 WARNING: Potential brute force attack from 203.0.113.42
    """
    
    print(f"\nTest Log:\n{test_log}\n")
    
    # Initialize agent
    print("Initializing CyberSec Agent...")
    agent = CyberSecAgent(verbose=True)
    
    # Run analysis
    print("\n" + "="*70)
    print("Starting Analysis")
    print("="*70)
    
    result = agent.analyze_log(test_log, use_brave_search=True)
    
    # Display results
    print("\n" + "="*70)
    print("ANALYSIS RESULTS")
    print("="*70)
    
    print(f"\n🎯 Threat Type: {result['threat_type']}")
    print(f"⚠️  Severity: {result['severity']}")
    print(f"📊 Confidence: {result['confidence_score']:.2f}")
    
    if result.get('bert_data'):
        print(f"\n🤖 BERT Detection:")
        print(f"   Anomaly Score: {result['bert_data']['anomaly_score']:.3f}")
        print(f"   Is Anomaly: {result['bert_data']['is_anomaly']}")
        print(f"   Confidence: {result['bert_data']['confidence']:.1f}%")
    
    if result.get('search_query'):
        print(f"\n🔍 Search Query: {result['search_query']}")
    
    if result.get('search_sources'):
        print(f"\n🌐 Found {len(result['search_sources'])} threat intelligence sources")
    
    print(f"\n📝 Explanation:\n{result['explanation']}")
    
    if result.get('recommended_actions'):
        print(f"\n✅ Recommended Actions:")
        for i, action in enumerate(result['recommended_actions'], 1):
            print(f"   {i}. {action}")
    
    # NEW: Display agent summary and actions
    if result.get('agent_summary'):
        print("\n" + "="*70)
        print("🎯 LANGCHAIN AGENT SUMMARY")
        print("="*70)
        print(f"\n{result['agent_summary']}")
    
    if result.get('agent_actions'):
        print(f"\n🔧 Agent made {len(result['agent_actions'])} additional tool call(s):")
        for i, action in enumerate(result['agent_actions'], 1):
            print(f"\n   {i}. Tool: {action['tool']}")
            print(f"      Input: {action['tool_input'][:100]}...")
            print(f"      Observation: {action['observation'][:150]}...")
    
    print("\n" + "="*70)
    print("Test completed successfully!")
    print("="*70)

if __name__ == "__main__":
    try:
        test_agent()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
