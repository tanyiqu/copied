import time
import pyperclip
from pynput.keyboard import Key, Controller

keyboard = Controller()

def on_clipboard_change():
    text_content = pyperclip.paste()
    # 处理剪贴板文本内容
    print(text_content)
    # 发送键盘事件
    keyboard.press(Key.cmd)
    keyboard.press('v')
    keyboard.release('v')
    keyboard.release(Key.cmd)

# 监听剪贴板变化
previous_content = pyperclip.paste()
while True:
    current_content = pyperclip.paste()
    if current_content != previous_content:
        on_clipboard_change()
        previous_content = current_content
    time.sleep(0.5)
