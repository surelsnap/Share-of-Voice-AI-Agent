# Main file to run the SoV analysis agent
# This is my first AI agent project for Atomberg internship

import sys
import config as cfg
from sov_agent import SoVAgent

def main():
    # try to run the agent
    try:
        print("Starting the agent...")
        agent = SoVAgent(cfg)
        
        # run the analysis
        results = agent.run()
        
        print("\nDone! Check output folder for results")
        return 0
        
    except KeyboardInterrupt:
        print("\n\nStopped by user")
        return 1
    except Exception as e:
        print(f"\n\nError happened: {e}")
        # print full error for debugging
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())

