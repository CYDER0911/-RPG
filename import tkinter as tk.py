import tkinter as tk

def type_text(widget, text, delay=100, chunk_size=5):
    """
    Type text into the widget as if it is being typed in real-time, 
    clearing the text every chunk_size sentences.

    :param widget: The widget to update.
    :param text: The text to display.
    :param delay: Delay in milliseconds between each character.
    :param chunk_size: Number of sentences before clearing the widget.
    """
    sentences = text.split('\n\n')
    total_chunks = (len(sentences) + chunk_size - 1) // chunk_size  # Calculate number of chunks

    def update_label(chunk_idx, idx):
        if chunk_idx < total_chunks:
            if idx == 0:
                current_text.set("")  # Clear text at the start of each chunk
                window.after(1000)  # Pause before the next chunk

            start_idx = chunk_idx * chunk_size
            end_idx = min((chunk_idx + 1) * chunk_size, len(sentences))
            chunk_text = '\n\n'.join(sentences[start_idx:end_idx])

            if idx < len(chunk_text):
                current_text.set(chunk_text[:idx+1])
                window.after(delay, update_label, chunk_idx, idx+1)
            else:
                window.after(1000, update_label, chunk_idx + 1, 0)  # Pause before next chunk
        else:
            show_button()  # Show the button after typing is done

    update_label(0, 0)

def show_button():
    mybutton.pack()  # Set the button position

def button_event():
    mybutton['text'] = 'hello world'

# Create the main window
window = tk.Tk()
window.title('PBC')  # Set the title of the window
window.geometry('600x400')  # Set the size of the window

# StringVar to update the label text
current_text = tk.StringVar()
label = tk.Label(window, textvariable=current_text, font=('Helvetica', 12), wraplength=550, justify='left')
label.pack(pady=20)  # Add some padding to center the label

# Create a button but don't display it yet
mybutton = tk.Button(window, text='button', command=button_event)

# Dialogue
dialogue = (
    "旁白：菲利爾，30歲男，月入25K的上班族，性格內向孤僻，從小到大被父母情緒勒索，做決定受父母控制、支配，不敢表達心中真實想法。"
    "可憐的菲利爾只能羨慕他人的自由，但同時懦弱的隱藏自己。這一天，菲利爾來到高中同學會。\n\n"
    "菲利爾：哈…囉。\n\n"
    "愛德華：嗯？誰在說話…..哎呀，20年不見，多虧了這次同學會，終於有機會跟大家聚在一起了。大家，是不是都跟我過得一樣fantastic啊？\n\n"
    "李奇：告訴你啊，幸好當初選擇了創業，最近公司的市值真的是一翻再翻啊......每天數錢數到手軟啊。（用錢搧風）\n\n"
    "愛德華：哼，你們還記得我大學釣到的那個boyfriend嗎？我的life有了他真的好幸福！一下帶我去Japan，一下帶我去America，還有那個杜拜！我真的是very happy啊！（動作：喝一口飲料）\n\n"
    "菲利爾：是….. 我在說話……（另外兩人安靜地看著菲利爾）\n\n"
    "愛德華：你是誰啊？你是...你是...你是…那個菲、菲、菲力、菲力牛排？！\n\n"
    "李奇：菲力牛排？我才不屑吃呢。他是那個跟失敗同名的菲利爾吧。\n\n"
    "愛德華：欸？那個...菲利爾！我想起來了！啊...那個你高中的時候，唯一的friend，那個誰啊...（皺眉）啊蓋瑞，他怎麼沒有來。好久沒聽聞他的消息了。\n\n"
    "菲利爾：他、她、、他、我我、、、我……\n\n"
    "李奇：他就是前幾年那個輕生的那個同學啊。哎，不要提這種不吉利的事情，害我賠錢的話你們負擔得起嗎？\n\n"
    "（菲利爾不發一語，看起來快崩潰）\n\n"
    "愛德華：欸？那個金髮，那個古銅色肌膚，還有六塊肌，最近還投資房地產賺了六億美金的那個肯尼竟然來了！\n\n"
    "李奇：什麼！六億美金？？？？快我們去找他敬酒！\n\n"
    "愛德華：什麼！\n\n"
    "李奇：六億欸！"
)

# Start typing the text
type_text(label, dialogue)

# Run the main loop to display the window
window.mainloop()
