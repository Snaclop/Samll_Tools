import itertools
import tkinter as tk
from tkinter import ttk, messagebox

# 计算函数
def calculate(a, op, b):
    try:
        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '*':
            return a * b
        elif op == '/':
            if b == 0:
                return None
            return a / b
    except:
        return None

# 获取所有排列组合
def get_all_permutations(numbers):
    perms = itertools.permutations(numbers)
    return list(set(perms))  # 去除重复排列

# 解24点函数
def solve_24(numbers):
    solutions = set()
    ops = ['+', '-', '*', '/']
    permutations = get_all_permutations(numbers)
    
    for nums in permutations:
        a, b, c, d = nums
        for op1, op2, op3 in itertools.product(ops, repeat=3):
            # 结构1: ((a op1 b) op2 c) op3 d
            step1 = calculate(a, op1, b)
            if step1 is not None:
                step2 = calculate(step1, op2, c)
                if step2 is not None:
                    step3 = calculate(step2, op3, d)
                    if step3 is not None and abs(step3 - 24) < 1e-6:
                        expr = f"(({a}{op1}{b}){op2}{c}){op3}{d}"
                        solutions.add(f"{expr}=24")
            
            # 结构2: (a op1 (b op2 c)) op3 d
            step1 = calculate(b, op2, c)
            if step1 is not None:
                step2 = calculate(a, op1, step1)
                if step2 is not None:
                    step3 = calculate(step2, op3, d)
                    if step3 is not None and abs(step3 - 24) < 1e-6:
                        expr = f"({a}{op1}({b}{op2}{c})){op3}{d}"
                        solutions.add(f"{expr}=24")
            
            # 结构3: a op1 ((b op2 c) op3 d)
            step1 = calculate(b, op2, c)
            if step1 is not None:
                step2 = calculate(step1, op3, d)
                if step2 is not None:
                    step3 = calculate(a, op1, step2)
                    if step3 is not None and abs(step3 - 24) < 1e-6:
                        expr = f"{a}{op1}(({b}{op2}{c}){op3}{d})"
                        solutions.add(f"{expr}=24")
            
            # 结构4: a op1 (b op2 (c op3 d))
            step1 = calculate(c, op3, d)
            if step1 is not None:
                step2 = calculate(b, op2, step1)
                if step2 is not None:
                    step3 = calculate(a, op1, step2)
                    if step3 is not None and abs(step3 - 24) < 1e-6:
                        expr = f"{a}{op1}({b}{op2}({c}{op3}{d}))"
                        solutions.add(f"{expr}=24")
            
            # 结构5: (a op1 b) op3 (c op2 d)
            step1 = calculate(a, op1, b)
            step2 = calculate(c, op2, d)
            if step1 is not None and step2 is not None:
                step3 = calculate(step1, op3, step2)
                if step3 is not None and abs(step3 - 24) < 1e-6:
                    expr = f"({a}{op1}{b}){op3}({c}{op2}{d})"
                    solutions.add(f"{expr}=24")
    
    return solutions

# GUI应用类
class TwentyFourGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("24点计算器")
        self.root.geometry("1040x1000")
        
        # 创建输入框和标签
        self.entries = []
        for i in range(4):
            label = ttk.Label(root, text=f"数字{i+1}:")
            label.grid(row=i, column=0, padx=5, pady=5)
            entry = ttk.Entry(root, width=10)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entry.bind('<Return>', lambda e, index=i: self.on_return(index))
            self.entries.append(entry)
        self.entries[0].focus_set()
        
        # 创建计算按钮
        self.calculate_btn = ttk.Button(root, text="计算", command=self.calculate)
        self.calculate_btn.grid(row=0, column=8, padx=5, pady=5)
        
        # 创建输出框
        self.output = tk.Text(root, height=20, width=60)
        self.output.grid(row=5, column=0, columnspan=9, padx=5, pady=5)
    
    # 处理回车事件
    def on_return(self, current_index):
        if current_index < 3:
            self.entries[current_index + 1].focus_set()
        else:
            self.calculate()
    
    # 计算逻辑
    def calculate(self):
        try:
            numbers = [int(entry.get()) for entry in self.entries]
            if len(numbers) !=4 or any(num < 1 or num > 13 for num in numbers):
                messagebox.showerror("错误", "请输入四个1-13的整数！")
            solutions = solve_24(numbers)
            self.output.delete(1.0, tk.END)
            if solutions:
                for expr in sorted(solutions):
                    self.output.insert(tk.END, f"{expr}\n")
            else:
                self.output.insert(tk.END, "无解")
        except:
            messagebox.showerror("错误", "请输入四个1-13的整数！")


if __name__ == "__main__":
    root = tk.Tk()
    app = TwentyFourGameApp(root)
    root.mainloop()