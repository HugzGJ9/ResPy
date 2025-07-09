import os
from dotenv import load_dotenv

def load_env_from_project_root(target_folder="ResPy", dotenv_name=".env"):

    original_dir = os.getcwd()
    max_attempts = 20
    for _ in range(max_attempts):
        if os.path.basename(os.getcwd()) == target_folder:
            break
        os.chdir("..")
    else:
        raise RuntimeError(f"Could not find target folder '{target_folder}' from {original_dir}")

    dotenv_path = os.path.join(os.getcwd(), dotenv_name)
    if not os.path.exists(dotenv_path):
        raise FileNotFoundError(f".env file not found at {dotenv_path}")

    load_dotenv(dotenv_path)