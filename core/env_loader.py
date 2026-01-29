import os

ENV_PATH = "/home/divyanshu/logan/.env"

def load_env():
    if not os.path.isfile(ENV_PATH):
        print("ENV LOADER: .env file not found at", ENV_PATH)
        return

    with open(ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                os.environ[key] = value
