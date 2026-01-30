# Command-Line Interface for CyberSec Agent
import sys
import os
from pathlib import Path
from loguru import logger

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.agent.cybersec_agent import CyberSecAgent
from src.config import settings


def print_banner():
    """Print application banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    CyberSec Agent CLI                        ║
║          AI-Powered Security Log Analysis System             ║
╚══════════════════════════════════════════════════════════════╝

Configuration:
  LLM: {llm_url} ({llm_model})
  BERT API: {bert_url}
  Brave Search: {brave_status}

""".format(
        llm_url=settings.llm_base_url,
        llm_model=settings.llm_model,
        bert_url=settings.bert_api_url,
        brave_status="✓ Enabled" if settings.brave_api_key and settings.brave_api_key != "your_brave_api_key_here" else "✗ Not configured"
    )
    print(banner)


def print_separator():
    """Print separator line"""
    print("=" * 70)


def format_result(result: dict):
    """Format and print analysis result"""
    print_separator()
    print("ANALYSIS RESULTS")
    print_separator()
    
    # Threat Type
    print(f"\n🎯 THREAT TYPE: {result.get('threat_type', 'Unknown')}")
    
    # Severity with color coding (using ANSI colors)
    severity = result.get('severity', 'UNKNOWN')
    severity_colors = {
        'CRITICAL': '\033[91m',  # Red
        'HIGH': '\033[93m',      # Yellow
        'MEDIUM': '\033[94m',    # Blue
        'LOW': '\033[92m',       # Green
        'INFO': '\033[96m'       # Cyan
    }
    color = severity_colors.get(severity, '\033[0m')
    reset = '\033[0m'
    print(f"⚠️  SEVERITY: {color}{severity}{reset}")
    
    # Confidence
    confidence = result.get('confidence_score', 0.0)
    confidence_pct = confidence * 100
    print(f"📊 CONFIDENCE: {confidence_pct:.1f}%")
    
    # Explanation
    print(f"\n📝 DETAILED EXPLANATION:")
    print("-" * 70)
    explanation = result.get('explanation', 'No explanation available')
    print(explanation)
    
    # Indicators of Compromise
    iocs = result.get('indicators_of_compromise', [])
    if iocs:
        print(f"\n🔍 INDICATORS OF COMPROMISE:")
        print("-" * 70)
        for i, ioc in enumerate(iocs, 1):
            print(f"  {i}. {ioc}")
    
    # Recommended Actions
    actions = result.get('recommended_actions', [])
    if actions:
        print(f"\n✅ RECOMMENDED ACTIONS:")
        print("-" * 70)
        for i, action in enumerate(actions, 1):
            print(f"  {i}. {action}")
    
    print_separator()


def interactive_mode(agent: CyberSecAgent):
    """Run interactive mode"""
    print("\nInteractive Mode")
    print("Enter log text to analyze (type 'quit' or 'exit' to quit)")
    print("Type 'file <path>' to analyze a log file")
    print("Type 'help' for more commands\n")
    
    while True:
        try:
            # Get input
            user_input = input("\n🔐 Log> ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye!")
                break
            
            elif user_input.lower() == 'help':
                print("""
Available commands:
  help              - Show this help message
  file <path>       - Analyze a log file
  quit/exit/q       - Exit the application
  
  Or simply enter log text to analyze it directly.
                """)
                continue
            
            elif user_input.lower().startswith('file '):
                # Analyze file
                file_path = user_input[5:].strip()
                
                if not os.path.exists(file_path):
                    print(f"❌ Error: File not found: {file_path}")
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        log_text = f.read()
                    
                    print(f"\n📄 Analyzing file: {file_path}")
                    print(f"   Size: {len(log_text)} characters")
                    
                    # Analyze
                    result = agent.analyze_log(log_text)
                    format_result(result)
                    
                except Exception as e:
                    print(f"❌ Error reading file: {e}")
                continue
            
            else:
                # Analyze log text
                log_text = user_input
                
                print(f"\n🔍 Analyzing log...")
                result = agent.analyze_log(log_text)
                format_result(result)
        
        except KeyboardInterrupt:
            print("\n\nInterrupted. Type 'quit' to exit.")
        
        except Exception as e:
            print(f"\n❌ Error: {e}")
            logger.exception("Error in interactive mode")


def analyze_file(agent: CyberSecAgent, file_path: str):
    """Analyze a log file"""
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found: {file_path}")
        sys.exit(1)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            log_text = f.read()
        
        print(f"📄 Analyzing file: {file_path}")
        print(f"   Size: {len(log_text)} characters\n")
        
        result = agent.analyze_log(log_text)
        format_result(result)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        logger.exception("Error analyzing file")
        sys.exit(1)


def analyze_text(agent: CyberSecAgent, log_text: str):
    """Analyze log text"""
    print(f"🔍 Analyzing log text ({len(log_text)} characters)...\n")
    
    try:
        result = agent.analyze_log(log_text)
        format_result(result)
    except Exception as e:
        print(f"❌ Error: {e}")
        logger.exception("Error analyzing text")
        sys.exit(1)


def main():
    """Main CLI entry point"""
    # Configure logger for CLI
    logger.remove()
    logger.add(
        sys.stderr,
        level="WARNING",  # Only show warnings and errors in CLI
        format="<level>{level}</level>: {message}"
    )
    
    # Print banner
    print_banner()
    
    # Initialize agent
    print("Initializing agent...")
    try:
        agent = CyberSecAgent(verbose=False)
        print("✓ Agent initialized successfully\n")
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        sys.exit(1)
    
    # Parse arguments
    if len(sys.argv) == 1:
        # No arguments - interactive mode
        interactive_mode(agent)
    
    elif sys.argv[1] in ['-h', '--help']:
        print("""
Usage:
  python -m src.cli.main                    # Interactive mode
  python -m src.cli.main <log_text>         # Analyze log text
  python -m src.cli.main -f <file>          # Analyze log file
  python -m src.cli.main --file <file>      # Analyze log file
  python -m src.cli.main -h, --help         # Show this help

Examples:
  python -m src.cli.main "Failed login from 192.168.1.1"
  python -m src.cli.main -f /var/log/auth.log
  python -m src.cli.main --file suspicious.log
        """)
    
    elif sys.argv[1] in ['-f', '--file']:
        # File mode
        if len(sys.argv) < 3:
            print("❌ Error: Please specify a file path")
            sys.exit(1)
        
        file_path = sys.argv[2]
        analyze_file(agent, file_path)
    
    else:
        # Direct text mode
        log_text = ' '.join(sys.argv[1:])
        analyze_text(agent, log_text)


if __name__ == "__main__":
    main()
