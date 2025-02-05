import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup

class App():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('600x800')
        self.root.title('Music Score Spider')
        self.intialize()
        self.root.mainloop()

    def intialize(self):
        #  半初始化，点击返回按钮执行
        for widget in self.root.winfo_children():
            widget.destroy()

        self.label = tk.Label(self.root, text='请输入乐谱名：', font=('黑体', 20))
        self.label.pack(pady=5)
        self.entry = tk.Entry(self.root)
        self.entry.pack(pady=5)
        self.cfm_btn = tk.Button(self.root, text='确认' ,command=self.crawl)
        self.cfm_btn.pack(pady=10)

    def crawl(self):
        self.cfm_btn.destroy()
        self.label.config(text='搜索到以下内容', font=('黑体', 20))
        self.frame_list = tk.Frame(self.root)
        self.frame_list.pack(pady=5)
        self.scrollbar = tk.Scrollbar(self.frame_list)
        self.scrollbar.grid(row=0, column=1, sticky=(tk.S, tk.N))
        self.listbox = tk.Listbox(self.frame_list, yscrollcommand=self.scrollbar.set)
        self.listbox.grid(row=0, column=1)
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)
        self.download_btn = tk.Button(self.frame, text='开始下载', command=self.download)
        self.download_btn.grid(row=0, column=0)
        self.back_btn = tk.Button(self.frame, text='返回', command=self.intialize)
        self.back_btn.grid(row=0, column=1)

        name = self.entry.get()
        self.result_dic = {}
        url = f'https://www.everyonepiano.cn/Music-search/?come=web&p=1&canshu=cn_edittime&word={name}&author=&jianpu=&paixu=desc'
        resp_0 = requests.get(url)
        domain_0 = BeautifulSoup(resp_0.text, 'html.parser')
        result_num = domain_0.find('div', class_='col-xs-4 col-sm-4 col-md-5 EOPPageNo')
        result_num = result_num.find('span')
        result_num = int(result_num.text)
        page_num = int(result_num/10+1)

        for i in range(1, page_num+1):
            url = f'https://www.everyonepiano.cn/Music-search/?come=web&p={i}&canshu=cn_edittime&word={name}&author=&jianpu=&paixu=desc'
            resp = requests.get(url=url)
            domain = BeautifulSoup(resp.text, 'html.parser')
            result_page_list = domain.find_all('div', class_="MITitle")

            for single_result in result_page_list:
                a = single_result.find('a')
                href = str(a.get('href'))
                href = href.replace('Music', 'Stave') # 替换成stave后就是五线谱界面
                title = a.get('title')
                child_page = f'https://www.everyonepiano.cn{href}'
                self.result_dic[title] = child_page
        
            if len(self.result_dic) != 0:
                for title in self.result_dic.keys():
                    self.listbox.insert(tk.END, title)
            else:
                messagebox.showerror('Error', '没有内容，请再次尝试或检查输入')
        
    def download(self):
        index = self.listbox.curselection()[0]
        title = self.listbox.get(index)
        url = self.result_dic[title]
        resp = requests.get(url)
        final_page = BeautifulSoup(resp.text, 'html.parser')
        img_list = final_page.find_all('img', class_='img-responsive DownMusicPNG')

        for i in img_list:
            img_id = i.get('src')
            img_name = img_id.split('/')[-1]
            img_url = f'https://www.everyonepiano.cn/{img_id}'
            img_resp = requests.get(img_url)

            with open(rf'Scores/{img_name}', mode='wb') as file:
                file.write(img_resp.content)

            img_resp.close()

        resp.close()
        messagebox.showinfo('Success', '下载成功！')

if __name__ == '__main__':
    app = App()
