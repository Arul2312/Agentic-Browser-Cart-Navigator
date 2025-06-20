import asyncio
import sys
from src.agents.agent_factory import AgentFactory
from src.core.page_graph import AmazonGraphBuilder
from config.settings import config

async def main():
    print("Loaded config from", config.config_path)
    print("Config type:", type(config._config))
    print("Config keys:", list(config._config.keys()) if isinstance(config._config, dict) else 'Not a dict')
    
    print("INFO     [telemetry] Anonymized telemetry enabled. See https://docs.browser-use.com/development/telemetry for more information.")
    print("Starting Modular Graph-based Browser Navigation System")
    
    # Build page graph
    print("Building Amazon page graph...")
    graph = AmazonGraphBuilder.build()
    print(f"Page graph built with {len(graph.pages)} pages")
    
    # Get configuration from updated YAML structure
    agent_mode = config._config.get('agent_mode', 'browser_use')  # Top-level agent_mode
    llm_provider = config._config.get('llm_provider', 'openai')   # Top-level llm_provider
    price_threshold = config._config.get('price_threshold', 100.0)  # Top-level price_threshold
    
    print(f"\nConfiguration:")
    print(f"   Agent Mode: {agent_mode}")
    print(f"   LLM Provider: {llm_provider}")
    print(f"   Price Threshold: ${price_threshold:.2f}")
    
    # Create agent based on agent_mode
    print(f"\nInitializing {agent_mode} agent...")
    
    try:
        agent = AgentFactory.create_agent(agent_mode, graph)
        await agent.start()
        
        if agent_mode == "manual":
            print("Manual mode ready - follow the instructions below")
        else:
            print("Browser Use agent ready")
        
        print(f"\nExecuting task with ${price_threshold:.2f} threshold...")
        
        # Execute task with proper parameter based on agent type
        if hasattr(agent, 'execute_task'):
            if agent_mode == 'browser_use':
                # For browser_use agent, pass price_threshold parameter
                result = await agent.execute_task(price_threshold=price_threshold)
            elif agent_mode == 'manual':
                # For manual agent, pass goal parameter with threshold info
                goal = f"Navigate to Amazon cart and check if total exceeds ${price_threshold:.2f}. If below threshold, proceed to checkout and stop when personal info is requested."
                result = await agent.execute_task(goal)
            else:
                # Fallback for any other agent types
                result = await agent.execute_task(price_threshold=price_threshold)
        else:
            raise AttributeError(f"Agent {agent_mode} does not have execute_task method")
        
        await agent.close()
        
        print("\nCleaning up...")
        print("Done!")
        
        # Display results based on agent mode
        print("\n" + "="*60)
        print("TASK EXECUTION RESULTS")
        print("="*60)
        print(f"Status: {'SUCCESS' if result.success else 'FAILED'}")
        print(f"Agent Mode: {agent_mode}")
        print(f"LLM Provider: {llm_provider}")
        
        if result.success:
            print(f"Message: {result.message}")
            if result.data:
                print(f"\nDetailed Results:")
                
                # Display mode-specific details
                if agent_mode == 'browser_use':
                    print(f"   Action: {result.data.get('action_taken', 'completed')}")
                    print(f"   Cart Total: ${result.data.get('cart_total', 0.0):.2f}")
                    print(f"   Threshold Status: {result.data.get('threshold_status', 'Unknown')}")
                    print(f"   Checkout Reached: {result.data.get('checkout_reached', False)}")
                    print(f"   Behavior Correct: {result.data.get('behavior_correct', 'Unknown')}")
                elif agent_mode == 'manual':
                    print(f"   Manual Navigation: {result.data.get('navigation_status', 'Completed')}")
                    print(f"   User Input: {result.data.get('user_input', 'Not recorded')}")
                
                # Common details
                if 'result' in result.data:
                    print(f"   Full Result: {result.data['result'][:100]}..." if len(str(result.data['result'])) > 100 else f"   Full Result: {result.data['result']}")
        else:
            print(f"Error: {result.message}")
            print(f"\nTroubleshooting for {agent_mode} mode:")
            
            if agent_mode == 'browser_use':
                if llm_provider == 'openai':
                    print("   1. Make sure OpenAI API key is set: export OPENAI_API_KEY='your-key'")
                    print("   2. Check if OpenAI API is accessible")
                    print("   3. Verify account has credits")
                elif llm_provider == 'gemini-1.5-flash':
                    print("   1. Make sure Gemini API key is set")
                    print("   2. Check Gemini API access")
                print("   4. Try manual mode if automation fails")
            elif agent_mode == 'manual':
                print("   1. Follow the step-by-step instructions carefully")
                print("   2. Make sure to complete all required fields")
                print("   3. Check your internet connection to Amazon")
        
        # Mode-specific final messages
        if agent_mode == 'manual':
            print(f"\n Manual Mode Completed")
            print(f"   You navigated Amazon manually with ${price_threshold:.2f} threshold")
        elif agent_mode == 'browser_use':
            print(f"\n Browser Use Mode Completed")
            print(f"   Automated navigation using {llm_provider} with ${price_threshold:.2f} threshold")
        
        print("="*60)
        
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        print(f"Agent Mode: {agent_mode}")
        print(f"LLM Provider: {llm_provider}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())