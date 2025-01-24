from src.connections.brain_connection import BrainConnection
from dotenv import load_dotenv
load_dotenv()

def test_brain():
    config = {
        "llm_provider": "openai",
        "model": "gpt-3.5-turbo",
        "plugins": [
            {
                "name": "coingecko",
                "args": {"api_key": "CG-12BeZ64iSajBLPPz8mfX4uao"}
            },
            {
                "name": "erc20",
                "args": {
                    "tokens": ["goat_plugins.erc20.token.PEPE"]
                }
            }
        ]
    }

    brain = BrainConnection(config)
    if not brain.configure():
        print("Failed to configure brain")
        return

    # Test commands
    commands = [
        "What's the price of Bitcoin?",
        "Show me trending coins",
        "Get my PEPE balance"
    ]

    for cmd in commands:
        print(f"\nTesting: {cmd}")
        result = brain.process_command(cmd)
        print(f"Result: {result}")

if __name__ == "__main__":
    test_brain()