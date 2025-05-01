import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import time
import threading
import pyautogui

stop_flag = False  # 控制打字是否停止

def type_text(text, delay):
    global stop_flag
    stop_flag = False  # 每次启动都重置

    total_chars = len(text)
    progress_bar["maximum"] = total_chars
    progress_bar["value"] = 0

    time.sleep(5)  # 给你5秒切换到Word
    for i, char in enumerate(text):
        if stop_flag:
            break
        pyautogui.write(char)
        time.sleep(delay)
        progress_bar["value"] = i + 1  # 更新进度条
        root.update_idletasks()  # 刷新界面

def start_typing():
    global stop_flag
    text = text_input.get("1.0", tk.END).strip()
    try:
        delay = float(delay_input.get())
    except ValueError:
        messagebox.showerror("错误", "请输入合法的延迟时间（数字）")
        return

    if not text:
        messagebox.showerror("错误", "请输入要打的内容")
        return

    stop_flag = False  # 每次开始时清除停止标志
    threading.Thread(target=type_text, args=(text, delay), daemon=True).start()
    messagebox.showinfo("提示", "将在5秒后开始模拟打字，请将光标切换到 Word 或其他软件")

def stop_typing():
    global stop_flag
    stop_flag = True

# 创建窗口
root = tk.Tk()
root.title("模拟打字器")

tk.Label(root, text="输入内容：").pack()
text_input = tk.Text(root, height=10, width=50)
text_input.pack()

tk.Label(root, text="每个字符的延迟（秒）：").pack()
delay_input = tk.Entry(root)
delay_input.insert(0, "0.1")
delay_input.pack()

# 按钮区域
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="开始打字", command=start_typing).pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="停止打字", command=stop_typing).pack(side=tk.LEFT, padx=10)

# 添加进度条
progress_bar = ttk.Progressbar(root, length=400, mode="determinate")
progress_bar.pack(pady=10)

root.mainloop()
