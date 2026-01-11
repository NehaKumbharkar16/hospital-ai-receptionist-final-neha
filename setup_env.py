#!/usr/bin/env python3
"""
Environment Setup Script for Hospital AI Agent
Helps configure environment variables for both backend and frontend
"""

import os
import shutil
from pathlib import Path

def setup_backend_env():
    """Set up backend environment file"""
    template_path = Path("backend/env.template")
    env_path = Path("backend/.env")

    if not template_path.exists():
        print("[ERROR] Backend env.template not found!")
        return False

    if env_path.exists():
        response = input("Backend .env already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Skipping backend .env creation")
            return True

    try:
        shutil.copy(template_path, env_path)
        print("[SUCCESS] Created backend/.env")
        print("   Please edit it with your actual Supabase credentials")
        return True
    except Exception as e:
        print(f"[ERROR] Error creating backend .env: {e}")
        return False

def setup_frontend_env():
    """Set up frontend environment file"""
    template_path = Path("frontend/env.template")
    env_path = Path("frontend/.env.local")

    if not template_path.exists():
        print("[ERROR] Frontend env.template not found!")
        return False

    if env_path.exists():
        response = input("Frontend .env.local already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Skipping frontend .env.local creation")
            return True

    try:
        shutil.copy(template_path, env_path)
        print("[SUCCESS] Created frontend/.env.local")
        return True
    except Exception as e:
        print(f"[ERROR] Error creating frontend .env.local: {e}")
        return False

def main():
    print("Hospital AI Agent - Environment Setup")
    print("=" * 50)

    backend_success = setup_backend_env()
    print()
    frontend_success = setup_frontend_env()

    print("\n" + "=" * 50)

    if backend_success and frontend_success:
        print("[SUCCESS] Environment setup completed!")
        print("\nNext steps:")
        print("1. Edit backend/.env with your Supabase credentials")
        print("2. Edit frontend/.env.local if needed")
        print("3. Run the backend: cd backend && uvicorn main:app --reload")
        print("4. Run the frontend: cd frontend && npm run dev")
    else:
        print("[ERROR] Environment setup had issues. Please check the errors above.")

if __name__ == "__main__":
    main()