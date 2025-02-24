import json
import datetime
import random
import tkinter as tk
from tkinter import messagebox

class MyApp():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("单词记忆系统")
        self.root.geometry("1000x800")
        self.qbtn = tk.Button(self.root, text="查询单词", command=self.query)
        self.qbtn.pack(pady=5)
        self.abtn = tk.Button(self.root, text="添加单词", command=self.add)
        self.abtn.pack(pady=5)
        self.rbtn = tk.Button(self.root, text="复习单词", command=self.review)
        self.rbtn.pack(pady=5)
        self.read_dict()
        self.root.mainloop()


    def query(self):
        self.qwin = tk.Toplevel(self.root)
        self.qwin.title("查询单词")
        self.qwin.geometry("600x700")
        self.qwin.transient(self.root)

        self.lable = tk.Label(self.qwin, text="请输入要查询的单词：")
        self.lable.pack(pady=5)
        self.q_word_entry = tk.Entry(self.qwin)
        self.q_word_entry.pack(pady=5)
        self.qbtn = tk.Button(self.qwin, text="查询", command=self.query_word_result)
        self.qbtn.pack(pady=5)

    def query_word_result(self):
        word = self.q_word_entry.get()
        if word in self.word_dict:
            messagebox.showinfo("查询结果", f"单词：{word}\n释义：{self.word_dict[word]['meaning']}\n时间：{self.word_dict[word]['time']}\n标记：{self.is_marked(word)}")
        else:
            messagebox.showerror("错误", "单词不存在")

    def is_marked(self, word):
        if self.word_dict[word]['mark'] == 1:
            return '已标记'
        else:
            return '未标记'

    def query_mark(self):
        result_list = []
        for word, info in self.word_dict.items():
            if info['mark'] == 1:
                result_list.append(word)


    def add(self):  # awin是add窗口
        self.awin = tk.Toplevel(self.root)
        self.awin.title("添加单词")
        self.awin.geometry("600x700")
        self.awin.transient(self.root)

        lable = tk.Label(self.awin, text="请输入单词及释义：")
        lable.pack(pady=5)
        frame = tk.Frame(self.awin)
        frame.pack(pady=5)
        lable_word = tk.Label(frame, text="单词：")
        lable_word.grid(row=0, column=0)
        self.entry_word = tk.Entry(frame)
        self.entry_word.grid(row=0, column=1)
        label_meaning = tk.Label(frame, text="释义：")
        label_meaning.grid(row=1, column=0)
        self.entry_meaning = tk.Entry(frame)
        self.entry_meaning.grid(row=1, column=1)
        self.abtn = tk.Button(self.awin, text="添加", command=self.add_word)
        self.abtn.pack(pady=5)

    def add_word(self):
        word = self.entry_word.get()
        meaning = self.entry_meaning.get()
        time = datetime.datetime.now().strftime("%Y-%m-%d")

        if len(word) and len(meaning) != 0:
            if word in self.word_dict:
                messagebox.showerror("错误", "单词已存在")
            else:
                self.word_dict[word] = {'meaning': meaning,"time": time, "mark": 0}
                with open("word_dict.json", "w") as f:
                    json.dump(self.word_dict, f)
                messagebox.showinfo("提示", "单词添加成功")
        else:
            messagebox.showerror("错误", "输入不能为空")


    def review(self):
        self.rwin = tk.Toplevel(self.root)
        self.rwin.title("复习单词")
        self.rwin.geometry("600x700")
        self.rwin.transient(self.root)

        self.re_label = tk.Label(self.rwin, text="请选择复习方式：")
        self.re_label.pack(pady=5)
        self.rbtn_1 = tk.Button(self.rwin, text="乱序复习", command=self.review_random)
        self.rbtn_1.pack(pady=5)
        self.rbtn_2 = tk.Button(self.rwin, text="复习已标记的单词", command=self.review_mark)
        self.rbtn_2.pack(pady=5)
        self.rbtn_3 = tk.Button(self.rwin, text='艾宾浩斯记忆法复习', command=self.review_ebbinghaus)
        self.rbtn_3.pack(pady=5)

    def review_random(self):
        messagebox.showinfo('提示', '即将开始乱序复习，复习单词个数上限为20个')

        review_list = list(self.word_dict.keys())
        random.shuffle(review_list)
        self.next_word(review_list=review_list, i=0)

    def review_mark(self):
        for widgets in self.rwin.winfo_children():
            widgets.destroy()

        messagebox.showinfo('提示', '即将开始复习已标记的单词')

    def review_ebbinghaus(self):
        for widgets in self.rwin.winfo_children():
            widgets.destroy()

        messagebox.showinfo('提示', '正在开发中，敬请期待！')


    def next_word(self, review_list, i):
        for widgets in self.rwin.winfo_children():
            widgets.destroy()

        try:
            word = review_list[i]
        except IndexError:
            messagebox.showinfo('提示', '复习结束')
            self.rwin.destroy()

        label = tk.Label(self.rwin, text=word)
        label.pack(pady=5)
        self.re_entry = tk.Entry(self.rwin)
        self.re_entry.pack(pady=5)
        button = tk.Button(self.rwin, text='提交', command=lambda: self.check(word=word, review_list=review_list, i=i))
        button.pack(pady=5)


    def check(self, word, review_list, i):
        if self.word_dict[word]['meaning'] == self.re_entry.get():
            messagebox.showinfo('提示', '回答正确')
            self.next_word(review_list, i = i+1)
            
        else:
            messagebox.showerror('错误', f'回答错误，单词{word}的释义是{self.word_dict[word]["meaning"]}')
            self.mark_win = tk.Toplevel(self.rwin)
            self.mark_win.title('标记单词')
            self.mark_win.geometry('500x400')
            self.mark_win.transient(self.rwin)
            label = tk.Label(self.mark_win, text='是否标记该单词？')
            label.pack(pady=5)
            yes_btn = tk.Button(self.mark_win, text='是', command=lambda: self.mark_word(word, review_list, i))
            yes_btn.pack(pady=5)
            no_btn = tk.Button(self.mark_win, text='否', command=lambda: self.next_word(review_list, i=i+1))
            no_btn.pack(pady=5)

    def mark_word(self, word, review_list, i):
        self.word_dict[word]['mark'] = 1
        with open('word_dict.json', 'w') as f:
            json.dump(self.word_dict, f)
        messagebox.showinfo('提示', '单词已标记')
        self.mark_win.destroy()
        self.next_word(review_list, i=i+1)

    def read_dict(self):
        try:
            with open("word_dict.json", "r") as f:
                self.word_dict = json.load(f)
        except:
            self.word_dict = {}


if __name__ == "__main__":
    app = MyApp()
