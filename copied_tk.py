import tkinter as tk
import threading
import queue
import time
from tkinter.tix import MAIN
import pyperclip
import re


class Toast:
    def __init__(self, master, message, duration=2000):
        self.master = master
        self.message = message
        self.duration = duration
        self.top = None
        self.timer_id = None

    def show(self):
        # 创建顶层窗口对象并设置样式和内容
        # self.top = tk.Toplevel(self.master)
        self.top = tk.Toplevel()
        self.top.overrideredirect(True)
        self.top.attributes('-alpha', 0.8)
        self.top.attributes('-topmost', True)
        self.top.geometry("400x40+{}+{}".format(self.master.winfo_screenwidth() -
                          400 - 10, self.master.winfo_screenheight() - 40 - 40))
        label = tk.Label(self.top, text=self.message,
                         bg="#444444", fg="white", font=("Microsoft YaHei", 17), anchor="w", justify="center")
        label.place(x=0, y=0, width=400, height=40)
        # label.pack(pady=0, padx=0)

        # 设置窗口自动关闭定时器
        self.timer_id = self.top.after(self.duration, self.close)

    def close(self):
        # 取消定时器并销毁窗口
        if self.timer_id is not None:
            self.top.after_cancel(self.timer_id)
            self.top.destroy()


class ToastManager:
    def __init__(self):
        self.toasts = []
        self.queue = queue.Queue()
        self.thread = threading.Thread(target=self._process_queue)
        self.thread.daemon = True
        self.thread.start()

    def _process_queue(self):
        while True:
            try:
                message, duration = self.queue.get(block=True, timeout=None)
                toast = Toast(self.master, message, duration)
                self.toasts.append(toast)
                toast.show()
            except queue.Empty:
                pass

    def add_toast(self, message, duration=2000):
        self.queue.put((message, duration))

    def remove_toast(self, toast):
        # 从列表中移除指定的 Toast 对象
        if toast in self.toasts:
            self.toasts.remove(toast)

        # 手动关闭并销毁 Toast 窗口
        toast.close()

    def close_all_toasts(self):
        # 关闭和销毁所有的 Toast 窗口
        for toast in self.toasts:
            toast.close()
        self.toasts.clear()


def trim_str(s: str):
    s_new = re.sub(r"\s+", " ", s)
    return s_new
    pass


# 在主线程中监听剪贴板的变化并显示弹窗
def clipboard_monitor():

    last_text = pyperclip.paste()
    text = pyperclip.paste()
    toast_manager.add_toast('copied 已启动')
    while True:
        # 读取当前剪贴板中的文本内容
        text = pyperclip.paste()

        # 如果剪贴板中的文本内容发生了变化，则显示 Toast 弹窗
        if text != last_text:
            last_text = text
            toast_manager.add_toast("复制成功：" + trim_str(text.strip()), 3000)

        # 等待一段时间后再次检查剪贴板内容
        time.sleep(0.5)


# 在应用程序退出时关闭和销毁所有的 Toast 弹窗
def on_exit():
    toast_manager.close_all_toasts()
    root.destroy()


if __name__ == "__main__":
    toast_manager = ToastManager()

    # 创建主窗口并启动 Tkinter 的事件循环
    root = tk.Tk()
    root.withdraw()
    toast_manager.master = root

    # 启动剪贴板监视器和应用程序退出操作
    threading.Thread(target=clipboard_monitor, daemon=True).start()
    root.protocol('WM_DELETE_WINDOW', on_exit)
    root.mainloop()
    pass
