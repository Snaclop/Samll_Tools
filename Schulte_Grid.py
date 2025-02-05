import tkinter as tk
from tkinter import messagebox
import random
import time
import os

if os.name == 'nt':
    import winreg

class SchulteGridApp:
    def __init__(self, root):
        self.root = root
        self.root.title("舒尔特方格注意力测试")
        self.root.geometry("900x900")

        self.grid_size = 5  # 默认5x5
        self.current_number = 1
        self.start_time = None
        self.buttons = []

        # 检测系统主题并设置
        self.set_theme()

        # 创建控件
        self.create_widgets()

    def set_theme(self):
        try:
            # 检测系统主题
            is_dark_mode = self.is_dark_mode()
            if is_dark_mode:
                self.root.tk_setPalette(background='#2e2e2e', foreground='#ffffff', activeBackground='#3e3e3e', activeForeground='#ffffff')
            else:
                self.root.tk_setPalette(background='#ffffff', foreground='#000000', activeBackground='#e0e0e0', activeForeground='#000000')
        except Exception as e:
            print(f"无法设置主题: {e}")

    def is_dark_mode(self):
        try:
            if os.name == 'nt':  # Windows
                registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
                key = winreg.OpenKey(registry, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize')
                value, _ = winreg.QueryValueEx(key, 'AppsUseLightTheme')
                return value == 0  # 0 means dark mode, 1 means light mode
            else:  # Linux
                dark_mode = os.popen('gsettings get org.gnome.desktop.interface gtk-theme').read().strip()
                return 'dark' in dark_mode.lower()
        except Exception as e:
            print(f"无法检测系统主题: {e}")
            return False

    def create_widgets(self):
        # 顶部菜单
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(pady=10)

        self.size_label = tk.Label(self.menu_frame, text="选择方格大小：")
        self.size_label.pack(side=tk.LEFT, padx=5)

        self.size_var = tk.IntVar(value=5)
        self.size_scale = tk.Scale(self.menu_frame, from_=5, to=10, orient=tk.HORIZONTAL, variable=self.size_var, command=self.update_grid_size)
        self.size_scale.pack(side=tk.LEFT, padx=5)

        self.start_button = tk.Button(self.menu_frame, text="开始测试", command=self.start_test)
        self.start_button.pack(side=tk.LEFT, padx=5)

        # 方格区域
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack()

    def update_grid_size(self, value):
        self.grid_size = int(value)

    def clear_grid(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        self.buttons = []

    def create_grid(self):
        numbers = list(range(1, self.grid_size * self.grid_size + 1))
        random.shuffle(numbers)

        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                number = numbers.pop()
                button = tk.Button(self.grid_frame, text=str(number), width=5, height=2,
                                   command=lambda n=number: self.check_number(n))
                button.grid(row=i, column=j, padx=2, pady=2)
                row.append(button)
            self.buttons.append(row)

    def start_test(self):
        self.clear_grid()
        self.create_grid()
        self.current_number = 1
        self.start_time = time.time()

    def check_number(self, number):
        if number == self.current_number:
            self.current_number += 1
            for row in self.buttons:
                for button in row:
                    if button['text'] == str(number):
                        button.config(text='√', state=tk.DISABLED, bg="lightgreen")
                        break
            if self.current_number > self.grid_size * self.grid_size:
                self.show_result()
        else:
            messagebox.showerror("错误", "点击的数字不正确！")

    def show_result(self):
        elapsed_time = time.time() - self.start_time
        messagebox.showinfo("测试完成", f"恭喜完成测试！\n用时：{elapsed_time:.2f}秒")
        self.start_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = SchulteGridApp(root)
    root.mainloop()
