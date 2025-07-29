#!/usr/bin/env python3
"""
Script to start Magentic-UI Web Interface with OpenRouter API key.
"""
import os
import sys
import subprocess

def main():
    """Start Magentic-UI Web Interface with proper environment setup."""

    # Set OpenRouter API key
    openrouter_key = "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"

    print("🚀 Starting Magentic-UI Web Interface...")
    print(f"✅ OpenRouter API Key configured")
    print(f"🌐 Will be available at: http://localhost:8081")
    print("=" * 50)

    # Set up environment variables
    env = os.environ.copy()
    env["OPENAI_API_KEY"] = openrouter_key
    # For OpenRouter, we might need to set the base URL
    # env["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"

    try:
        # Use subprocess to start Magentic-UI with Docker (full features)
        cmd = [
            "magentic-ui",
            "--host", "127.0.0.1",
            "--port", "8081"
            # Remove --run-without-docker to enable full features
        ]

        print("🐳 Starting with Docker for full functionality...")
        process = subprocess.run(cmd, env=env, check=True)
        return process.returncode

    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting Magentic-UI: {e}")
        print("\n🔧 Trying without Docker...")

        try:
            # Fallback to without Docker
            cmd_fallback = [
                "magentic-ui",
                "--host", "127.0.0.1",
                "--port", "8081",
                "--run-without-docker"
            ]
            process = subprocess.run(cmd_fallback, env=env, check=True)
            return process.returncode
        except subprocess.CalledProcessError as e2:
            print(f"❌ Error starting Magentic-UI without Docker: {e2}")
            return 1

    except KeyboardInterrupt:
        print("\n👋 Magentic-UI stopped by user")
        return 0
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure magentic-ui is installed: pip install magentic-ui")
        print("2. Check if port 8081 is available")
        print("3. Make sure Docker is running for full functionality")
        return 1

if __name__ == "__main__":
    sys.exit(main())
