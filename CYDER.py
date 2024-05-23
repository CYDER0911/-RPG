
import tkinter as tk

window = tk.Tk()
window.title('PBC') # 設定PBC的標題
window.geometry('50x50') # 設定像素大小
def button_event():
# 按按鈕後的行為
    mybutton['text'] = 'hello world'
mybutton = tk.Button(window, text='button', command=button_event) # 宣告一個按鈕
mybutton.pack() # 設定按鈕位置
window.mainloop() # 主視窗用迴圈的方式一直顯示
