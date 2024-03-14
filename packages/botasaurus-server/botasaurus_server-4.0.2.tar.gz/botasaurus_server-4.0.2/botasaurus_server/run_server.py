import subprocess
import os
from threading import Thread
import sys
from .app import run_backend

def run_frontend():
    # Change to frontend directory
    frontend_dir = os.path.join(os.getcwd(), "frontend")
    # Run frontend server
    subprocess.check_call("npm run start", shell=True, cwd=frontend_dir)
    # subprocess.check_call("npm run dev", shell=True, cwd=frontend_dir)

def install():
    from concurrent.futures import ThreadPoolExecutor

    def install_scraping_dependencies():
        print("Installing scraping dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

    def install_frontend_dependencies():
        print("Installing frontend dependencies...")
        frontend_dir = os.path.join(os.getcwd(), 'frontend')
        subprocess.check_call("npm install && npm run build", shell=True, cwd=frontend_dir)


    def install_dependencies():
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [
                executor.submit(install_scraping_dependencies),
                executor.submit(install_frontend_dependencies),
            ]
            for future in futures:
                # Wait for each future to complete
                future.result()
        print("All dependencies installed successfully.")
    install_dependencies()

def run_server():
    if len(sys.argv) == 1:
        # No arguments provided, run both backend and frontend
        Thread(target=run_backend, daemon=True).start()
        run_frontend()
    elif sys.argv[1] == "backend":
        # Argument "backend" provided, run only backend
        run_backend()
    elif sys.argv[1] == "lint":
        # Checks Import Only
        pass
    elif sys.argv[1] == "install":
        install()
    elif sys.argv[1] == "prod:backend":
        # Argument "prod:backend" provided, run only backend
        run_backend()
    elif sys.argv[1] == "prod":
        # Argument "prod" provided, run only backend
        run_backend()
    else:
        # Unknown argument provided, raise an exception with the argument
        raise Exception(f"Unknown argument: {sys.argv[1]}")

if __name__ == "__main__":
    run_server()
