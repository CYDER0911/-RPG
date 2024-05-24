import tkinter as tk
import tkinter.font as tkFont
import subprocess

def type_text(widget, text, delay=60, chunk_size=6):
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

    def update_text(chunk_idx, idx):
        if chunk_idx < total_chunks:
            if idx == 0:
                widget.delete('1.0', tk.END)  # Clear text at the start of each chunk
                window.after(700)  # Pause before the next chunk

            start_idx = chunk_idx * chunk_size
            end_idx = min((chunk_idx + 1) * chunk_size, len(sentences))
            chunk_text = '\n\n'.join(sentences[start_idx:end_idx])

            if idx < len(chunk_text):
                current_text = chunk_text[:idx+1]
                widget.delete('1.0', tk.END)
                apply_mixed_styles(widget, current_text)
                window.after(delay, update_text, chunk_idx, idx+1)
            else:
                window.after(700, update_text, chunk_idx + 1, 0)  # Pause before next chunk
        else:
            show_button()  # Show the button after typing is done

    update_text(0, 0)

def apply_mixed_styles(widget, text):
    widget.tag_configure('bold', font=bold_font)
    widget.tag_configure('normal', font=normal_font)
    
    bold_phrases = ["從同學會回家的路上", "領主出現", "交代任務"]
    
    start_idx = 0
    for phrase in bold_phrases:
        phrase_start = text.find(phrase, start_idx)
        if phrase_start != -1:
            phrase_end = phrase_start + len(phrase)
            widget.insert(tk.END, text[start_idx:phrase_start], 'normal')
            widget.insert(tk.END, text[phrase_start:phrase_end], 'bold')
            start_idx = phrase_end

    widget.insert(tk.END, text[start_idx:], 'normal')

def show_button():
    mybutton.grid(row=2, column=1, pady=20)  # Display the button after typing is done

def button_event():
    mybutton.grid_forget()  # Hide the initial button
    
    # Create a frame for the path buttons
    button_frame = tk.Frame(window)
    button_frame.grid(row=3, column=0, columnspan=3, pady=20)  # Place the frame below the text widget

    # Create and pack three buttons horizontally within the frame
    path1_button = tk.Button(button_frame, text='勇氣', command=lambda: open_python_file('魔鏡-勇氣.py'), width=15, height=2)
    path1_button.grid(row=0, column=0, padx=10)  # Adjust the padx values as needed
    
    path2_button = tk.Button(button_frame, text='愛情', command=lambda: open_python_file('path2.py'), width=15, height=2)
    path2_button.grid(row=0, column=1, padx=10)  # Adjust the padx value as needed

    path3_button = tk.Button(button_frame, text='友情', command=lambda: open_python_file('path3.py'), width=15, height=2)
    path3_button.grid(row=0, column=2, padx=10)  # Adjust the padx values as needed

def open_python_file(file_name):
    subprocess.Popen(['python', file_name])

# Create the main window
window = tk.Tk()
window.title('RPG')  # Set the title of the window
window.geometry('762x600')  # Set the size of the window

# Define fonts
normal_font = tkFont.Font(family='Helvetica', size=12)
bold_font = tkFont.Font(family='Helvetica', size=12, weight='bold')

# Create a Text widget for mixed font styles
text_widget = tk.Text(window, font=('Helvetica', 12), wrap='word')
text_widget.grid(row=0, column=0, columnspan=3, pady=20, padx=20)

# Create the initial button but do not show it yet
mybutton = tk.Button(window, text='開始幫助菲利爾', command=button_event, width=20, height=3)

# Initialize button clicked flag
button_clicked = False
# Dialogue with some bold text marked by specific phrases
dialogue = (
    "旁白：菲利爾，30歲男，月入25k的上班族，性格內向孤僻，從小到大被父母情緒勒索，做決定受父母控制、支配，不敢表達心中真實想法，可憐的菲利爾只能羨慕他人的自由，但同時懦弱的隱藏自己。這一天，菲利爾來到高中同學會。\n\n"
    "菲利爾：哈…囉\n\n"
    "艾德華：恩？誰在說話…..哎呀20年不見，多虧了這次同學會，終於有機會跟大家聚在一起了。大家，是不是都跟我過得一樣fantastic阿？\n\n"
    "李奇：告訴你啊，幸好當初選擇了創業，最近公司的市值真的是一翻再翻啊....每天數錢數到手軟啊（用錢搧風）\n\n"
    "愛德華：哼，你們還記得我大學釣到的那個boyfriend嗎，我的life有了他真的好幸福！一下帶我去japan 一下帶我去 america 還有那個 杜拜！我真的是very happy昂(喝一口飲料)\n\n"
    "菲利爾：是….. 我在說話……（另外兩人安靜往菲利爾看）\n\n"
    "愛德華：你是誰啊？你是...你是...你是…那個菲、菲、菲力、菲力牛排？！\n\n"
    "李奇：菲力牛排？我才不屑吃勒。他是那個跟失敗同名的菲利爾吧。\n\n"
    "愛得華：ㄟ？那個...菲利爾！我想起來了！啊...那個你高中的時候，唯一的friend，那個誰啊...（皺眉）啊蓋瑞，他怎麼沒有來。 好久沒聽聞他的消息了\n\n"
    "菲利爾：他、她、、他、我我、、、我\n\n"
    "李奇：他就是前幾年那個輕生的那個同學啊。哎，不要提這種不吉利的事情，害我賠錢的話你們負擔得起嗎？\n\n"
    "（菲利爾不發一語，看起來快崩潰）\n\n"
    "愛德華：ㄟ？那個金髮，那個古銅色肌膚，還有六塊肌，最近還投資房地產賺了六億美金的那個肯尼竟然來了！\n\n"
    "李奇：什麼！六億美金？？？？快我們去找他敬酒！\n\n"
    "愛德華：什麼！\n\n"
    "李奇：六億欸！\n\n"
    "從同學會回家的路上\n\n"
    "(菲利爾低頭走在路上)\n\n"
    "菲利爾：人家一夕之間賺了六億。我….我的人生根本就是失敗的代名詞。我從來不敢反抗家裡替我做的決定，女朋友也追不到，朋友也沒了，我做錯什麼了嗎？沒有一樣是順利的，沒有一樣是我可以自己選擇的！（抱頭慢慢開始跪下）\n\n"
    "父母:\n：讀這個系，才有好出頭啊\n：我賺錢養你，你就應該聽話啊，選這個比較好啦\n：追不到女生就聽媽媽的話，去相親。這個女生好，屁股大好生養，肯定能給我生個大胖小子\n：我們都是為了你好⋯\n：連這都做不好了，要你有什麼用\n：書都讀不好了，玩什麼社團\n\n"
    "菲利爾崩潰的大叫（跪地抱頭、槌地）\n\n"
    "\n領主出現\n\n"
    "旁白：可憐的菲利爾似乎無意間呼喚了來自平行時空的時空領主，領主們眼見孤苦無依的菲利爾，決定發揮慈悲心，給菲利爾一次重來的機會。\n\n"
    "三位時空領主慢動作嬌貴的走出來（菲利爾定格）\n\n"
    "領主Ａ：喊「時、間、暫、停」\n\n"
    "是誰這麼大膽把我們三個偉大的時間領主都吵醒了（生氣）害得我要使出我的時間暫停能力。\n\n"
    "領主Ｂ：等等泰米，他看起來好像有什麼心事，讓我哈特王用讀心術來看看吧（拿出神奇拐杖，閉眼讀心）\n\n"
    "\n菲利爾的心聲\n"
    "：明明我也很努力了⋯為什麼只有我是這樣啊\n"
    "：從小的選擇都是被決定好的⋯\n"
    "：為什麼不能做自己喜歡的事\n"
    "：為什麼⋯為什麼你要離我而去啊⋯\n\n"
    "看看這可憐的孩子，索爾，用你的能力幫幫他吧。\n\n"
    "領主Ｃ：好，看我使出我的奪魂術！抽出菲利爾的靈魂！啊，正好下屆時空領主選拔賽要到了！在我前方正是來參加選拔賽的引靈者團們，這就是你們來好好表現自己的機會了！就讓我們一起來幫助菲利爾吧\n\n"
    "交代任務\n\n"
    "領主Ｃ：各位引靈者，我已經將菲利爾的三魂七魄分給你們了。正如你們所見，可憐的菲利爾需要你們的幫助。\n\n"
    "領主Ａ：請跟隨我們的手下（隊輔向領主敬禮），在這平行時空中幫助可憐的菲利爾解決問題扭轉人生。由於分散後的靈魂極不穩定，每個時空的入口處最多只能有四個分靈同時存在。\n\n"
    "領主Ｂ：要解決的問題都寫在信封上了，現在請我們的手下上來領取你們的信封吧。偷偷告訴你們吧，信封上寫著你們要解決的問題以及能夠幫上忙的人，至於信封上的提示則代表你們要先前往的平行時空喔。\n\n"
    "領主Ｃ：此外，菲利爾一但被困在平行時空發太久，靈魂就會散去，導致他在現實世界消失。因此，你們需要搜集霹靂無敵巴拉巴拉能量，才能讓菲利爾的靈魂重新拼湊起來，回到現實世界喔！而這些能量，是四處散佈在各個平行時空中的，當你們完成各個時空中的選擇時，便會獲得各個時空中不同的能量，至於能量的樣子，就是我們身上的標誌喔。\n\n"
    "領主Ｂ：為了感謝你們的幫助，我們會計算你們獲得的能量數量！獲得最多能量的引靈者競選團即是我們的下屆時空領主，我們準備來退位休息拉～！\n\n"
    "領主Ａ：待會我們三位會在平行宇宙中巡邏，而菲利爾的空殼也會在各空間遊走。握有菲利爾的靈魂的你們要小心，當菲利爾接近你們時，請得低頭閉眼！不然靈魂會被空殼給吸收。至於當你們遇到我們三位時也會有指定任務，任務內容等遇到我們的時候就會知道拉～祝你們好運，我們就先走啦！現在開始幫助菲利爾吧！\n"
)

# Start typing the text
type_text(text_widget, dialogue)

# Run the main loop to display the window
window.mainloop()