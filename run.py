"""
File chạy chính ứng dụng Desktop Local App - Marketing AI Campaign Manager.
Khởi tạo cấu hình, kiểm tra file .env, khởi tạo DB PostgreSQL và khởi chạy Streamlit web UI.
"""

import os
import sys
import subprocess
import webbrowser

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Kiểm tra file .env
    env_path = os.path.join(base_dir, ".env")
    env_example_path = os.path.join(base_dir, ".env.example")
    
    if not os.path.exists(env_path):
        if os.path.exists(env_example_path):
            with open(env_example_path, "r", encoding="utf-8") as f_src:
                content = f_src.read()
            with open(env_path, "w", encoding="utf-8") as f_dst:
                f_dst.write(content)
            print("[INFO] Da tao file .env tu file .env.example mẫu.")
        else:
            print("[WARNING] Khong tim thấy file .env.example.")
            
    print("[INFO] Dang khoi chay he thong Marketing AI Campaign Manager...")
    
    # 2. Chạy Streamlit App
    app_path = os.path.join(base_dir, "ui", "app.py")
    cmd = [sys.executable, "-m", "streamlit", "run", app_path, "--server.port", "8501"]
    
    try:
        print("[INFO] Dang mo trinh duyêt tai http://localhost:8501")
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n[INFO] Da dung ung dung.")

if __name__ == "__main__":
    main()
