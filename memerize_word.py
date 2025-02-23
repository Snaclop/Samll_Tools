import json
import time
import tkinter as tk
from tkinter import messagebox

class MyApp():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("单词记忆系统")
        self.root.geometry("500x300")
        self.inititialize()
        self.root.mainloop()
    
    def inititialize(self):
        self.qbtn = tk.Button(self.root, text="查询单词", command=self.query)
        self.qbtn.pack(pady=5)
        self.abtn = tk.Button(self.root, text="添加单词", command=self.add)
        self.abtn.pack(pady=5)
        self.rbtn = tk.Button(self.root, text="复习单词", command=self.review)
        self.rbtn.pack(pady=5)

    def query(self):
        self.qwin = tk.Toplevel(self.root)
        self.qwin.title("查询单词")
        self.qwin.geometry("300x200")
        self.qwin.transient(self.root)
        self.qwin.grab_set()
        self.qwin.focus_set()
        self.qwin.resizable(False, False)
        self.lable = tk.Label(self.qwin, text="请选择查询方式：")
        self.lable.pack(pady=5)
        self.qbtn1 = tk.Button(self.qwin, text="按单词查询", command=self.query_word)
        self.qbtn1.pack(pady=5)
        self.qbtn2 = tk.Button(self.qwin, text="按时间查询", command=self.query_time)
        self.qbtn2.pack(pady=5)
        self.qbtn3 = tk.Button(self.qwin, text="按标记查询", command=self.query_mark)
        self.qbtn3.pack(pady=5)

    def query_word(self):
        pass

    def query_time(self):
        pass

    def query_mark(self):
        pass

    def  add(self):
        self.awin = tk.Toplevel(self.root)
        self.awin.title("添加单词")
        self.awin.geometry("300x200")
        self.awin.transient(self.root)
        self.awin.grab_set()
        self.awin.focus_set()
        self.awin.resizable(False, False)
        self.lable = tk.Label(self.awin, text="请输入单词：")
        self.lable.pack(pady=5)
        self.entry = tk.Entry(self.awin)
        self.entry.pack(pady=5)
        self.abtn = tk.Button(self.awin, text="添加", command=self.add_word)
        self.abtn.pack(pady=5)

    def add_word(self):
        pass

    def review(self):
        pass

    def read_dict(self):
        with open("word_dict.json", "r") as f:
            self.word_dict = json.load(f)

if __name__ == "__main__":
    app = MyApp()
