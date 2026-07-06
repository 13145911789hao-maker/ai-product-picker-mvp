import subprocess
import sys
import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def run_cmd(cmd, cwd=None):
    return subprocess.Popen(cmd, cwd=cwd, shell=True)


def main():
    print("🚀 HermitCreate One-Click Starter Starting...")

    # Start backend
    print("📦 Starting backend (FastAPI)...")
    backend = run_cmd(
        "uvicorn dashboard:app --reload --port 8000",
        cwd=BASE_DIR
    )

    time.sleep(2)

    # Start frontend
    frontend_path = os.path.join(BASE_DIR, "frontend")

    print("💻 Starting frontend (React/Vite)...")
    frontend = run_cmd(
        "npm run dev",
        cwd=frontend_path
    )

    print("\n✅ System started successfully!")
    print("👉 Backend: http://localhost:8000")
    print("👉 Frontend: http://localhost:5173")

    try:
        backend.wait()
        frontend.wait()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        backend.terminate()
        frontend.terminate()


if __name__ == "__main__":
    main()
