import tkinter as tk
from tkinter import ttk
import threading
import pyautogui
import time

class TypingSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("模拟打字软件")

        # ✅ 最大化 + 禁止调整大小
        self.root.attributes("-zoomed", True)  # Windows专用最大化
        self.root.resizable(False, False)

        # ✅ 文本框
        self.text_to_type = tk.Text(root, height=10, width=50, font=("Arial", 14))
        self.text_to_type.pack(pady=20, anchor='w', padx=20)

        # ✅ 进度条
        self.progress = ttk.Progressbar(root, orient="horizontal", length=600, mode="determinate")
        self.progress.pack(pady=10, anchor='w', padx=20)

        # ✅ 打字设置 + 信息展示区域（左对齐）
        control_frame = tk.Frame(root)
        control_frame.pack(anchor='w', padx=20)

        self.speed_label = tk.Label(control_frame, text="打字间隔(ms)：", font=("Arial", 12))
        self.speed_label.grid(row=0, column=0, sticky='w')
        self.speed_entry = tk.Entry(control_frame, width=8, font=("Arial", 12))
        self.speed_entry.insert(0, "100")
        self.speed_entry.grid(row=0, column=1, padx=(5, 20))

        self.info_label = tk.Label(control_frame, text="预估时间：0秒    剩余字数：0", font=("Arial", 12))
        self.info_label.grid(row=0, column=2, sticky='w')

        # ✅ 按钮区域
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=20, anchor='w', padx=20)

        self.start_button = tk.Button(btn_frame, text="开始打字", command=self.start_typing, font=("Arial", 12))
        self.start_button.pack(side=tk.LEFT, padx=20)

        self.stop_button = tk.Button(btn_frame, text="停止", command=self.stop_typing, font=("Arial", 12))
        self.stop_button.pack(side=tk.LEFT, padx=20)

        # ✅ 状态变量
        self.stop_flag = False
        self.total_chars = 0

    def start_typing(self):
        self.stop_flag = False
        text = self.text_to_type.get("1.0", tk.END).strip()
        self.total_chars = len(text)

        try:
            delay_ms = int(self.speed_entry.get())
        except ValueError:
            delay_ms = 100
        delay = delay_ms / 1000

        estimated_time = round(delay * self.total_chars, 1)
        self.info_label.config(text=f"预估时间：{estimated_time}秒    剩余字数：{self.total_chars}")

        threading.Thread(target=self.countdown_and_type, args=(text, delay), daemon=True).start()

    def stop_typing(self):
        self.stop_flag = True
        self.progress["value"] = 0
        self.info_label.config(text="已停止")

    def countdown_and_type(self, text, delay):
        # 倒计时阶段（倒走）
        self.progress["maximum"] = 3
        for i in range(3):
            if self.stop_flag:
                return
            self.progress["value"] = 3 - i
            time.sleep(1)

        # 打字阶段（正走）
        self.progress["maximum"] = len(text)
        self.progress["value"] = 0

        for i, char in enumerate(text):
            if self.stop_flag:
                break
            pyautogui.typewrite(char)
            self.progress["value"] = i + 1
            remaining = self.total_chars - (i + 1)
            self.info_label.config(text=f"预估时间：~    剩余字数：{remaining}")
            time.sleep(delay)

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSimulator(root)
    root.mainloop()
