"""Entry point cho Marketing AI web app."""

import os
import sys
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


def main():
    env_path = os.path.join(BASE_DIR, ".env")
    env_example_path = os.path.join(BASE_DIR, ".env.example")

    if not os.path.exists(env_path):
        if os.path.exists(env_example_path):
            with open(env_example_path, "r", encoding="utf-8") as f_src:
                content = f_src.read()
            with open(env_path, "w", encoding="utf-8") as f_dst:
                f_dst.write(content)
            print("[INFO] Đã tạo file .env từ mẫu .env.example.")
        else:
            print("[WARNING] Không tìm thấy file .env.example.")

    app_path = os.path.join(BASE_DIR, "ui", "app.py")
    print("[INFO] Đang khởi chạy Marketing AI web app...")

    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", app_path, "--server.headless", "false"],
            cwd=BASE_DIR,
            check=True,
        )
    except Exception as exc:
        print(f"[ERROR] Không thể khởi chạy web app: {exc}")
        raise


if __name__ == "__main__":
    main()
