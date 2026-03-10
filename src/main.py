import time
import re
from agent.llm_client import LLMClient
from agent.memory import Memory
from tools.vision import capture_screen_base64
from tools.controller import click, type_text, press_key, scroll
from tools.commander import run_command

def parse_action(action_str: str):
    """
    Parses a string formatted like `ACTION(args)`
    Raises ValueError if format is incorrect.
    """
    match = re.search(r"([A-Z_]+)\((.*?)\)", action_str)
    if not match:
        raise ValueError(f"Could not parse action format: {action_str}")
    
    cmd = match.group(1).upper()
    args = match.group(2)
    return cmd, args

def execute_action(action: str, args: str, memory: Memory):
    """
    Routes the parsed action to the appropriate tool.
    """
    if action == "CLICK":
        x, y = map(int, [arg.strip() for arg in args.split(",")])
        return click(x, y)
    elif action == "TYPE":
        return type_text(args)
    elif action == "PRESS":
        return press_key(args)
    elif action == "SCROLL":
        return scroll(int(args))
    elif action == "CMD":
        print(f"⚠️ Security Warning: Running command `{args}`")
        # In a real MVP, wait for user confirmation here
        return run_command(args)
    elif action == "MEM_SAVE":
        parts = args.split(",", 1)
        if len(parts) == 2:
            return memory.save_memory(parts[0].strip(), parts[1].strip())
        else:
            return memory.save_memory("general_note", args)
    elif action == "DONE":
        return f"Task accomplished: {args}"
    else:
        raise ValueError(f"Unknown tool action: {action}")

def run_agent_loop(goal: str, max_steps: int = 15):
    """
    Main execution loop checking the screen and sending to LLM.
    """
    print(f"🚀 Starting NaiveClaw with Goal: '{goal}'")
    client = LLMClient()
    memory = Memory()
    history = [] # Optional: Can be passed to context to retain memory
    
    for step in range(1, max_steps + 1):
        print(f"\n--- Step {step} ---")
        try:
            # 1. Capture screen
            img_b64 = capture_screen_base64()
            print("[1] Screen captured.")
            
            # 2. Get LLM recommendation
            print("[2] Analyzing screen, memory, and history with LLM...")
            current_memory = memory.get_all()
            action_raw = client.get_action(img_b64, goal, history, current_memory)
            print(f"    🧠 LLM decided: {action_raw}")
            
            # 3. Parse action string
            action_type, args = parse_action(action_raw)
            if action_type == "DONE":
                print(f"✅ Goal achieved: {args}")
                break

            # 4. Execute action
            print(f"[3] Executing action {action_type} with parameters '{args}'...")
            result = execute_action(action_type, args, memory)
            print(f"    🔧 Tool result: {result}")
            
            # (Optional) Update history context
            history.append({"role": "assistant", "content": action_raw})
            history.append({"role": "user", "content": f"Action result: {result}"})
            
            # 5. Wait
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ Error during step {step}: {e}")
            break

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="NaiveClaw Agent run loop")
    parser.add_argument("--goal", type=str, required=True, help="What do you want the agent to do?")
    parser.add_argument("--steps", type=int, default=15, help="Maximum number of steps the agent can take")
    
    args = parser.parse_args()
    
    run_agent_loop(args.goal, max_steps=args.steps)
