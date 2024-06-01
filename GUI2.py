import tkinter as tk
import tkinter.font as tkFont
import subprocess
import sys

def type_text(widget, text, delay=60, chunk_size=6):
    sentences = text.split('\n\n')
    total_chunks = (len(sentences) + chunk_size - 1) // chunk_size

    def update_text(chunk_idx, idx):
        if chunk_idx < total_chunks:
            if idx == 0:
                widget.delete('1.0', tk.END)
                window.after(700)

            start_idx = chunk_idx * chunk_size
            end_idx = min((chunk_idx + 1) * chunk_size, len(sentences))
            chunk_text = '\n\n'.join(sentences[start_idx:end_idx])

            if idx < len(chunk_text):
                current_text = chunk_text[:idx+1]
                widget.delete('1.0', tk.END)
                apply_mixed_styles(widget, current_text)
                window.after(delay, update_text, chunk_idx, idx+1)
            else:
                window.after(700, update_text, chunk_idx + 1, 0)

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
    mybutton.grid(row=2, column=1, pady=20)

def display_clue(path):
    clues = {
        '勇氣': '你哭他也哭，你笑他也笑，正面看的見，背面看不到',
        '愛情': '聽說這個平行宇宙中有一個上知天文下知地理的天才',
        '友情': '國際美人'
    }
    clue_text = clues.get(path, 'Unknown path')

    button_frame.grid_forget()
    text_widget.delete('1.0', tk.END)
    text_widget.insert(tk.END, clue_text, 'normal')

    proceed_button = tk.Button(window, text='Understood', command=lambda: launch_path(path), width=20, height=3)
    proceed_button.grid(row=5, column=1, pady=20)

def launch_path(path):
    file_names = {
        '勇氣': 'map.py',
        '愛情': 'map2.py',
        '友情': 'map3.py'
    }
    file_name = file_names.get(path, 'path1.py')
    if path not in completed_paths:
        completed_paths.append(path)
    subprocess.Popen(['python', file_name, *completed_paths])
    window.iconify()

def show_remaining_paths(completed_paths):
    paths = ['勇氣', '愛情', '友情']
    remaining_paths = [path for path in paths if path not in completed_paths]

    global button_frame
    button_frame = tk.Frame(window)
    button_frame.grid(row=3, column=0, columnspan=3, pady=20)
    
    if len(remaining_paths) == 1:
        path_button = tk.Button(button_frame, text=remaining_paths[0], command=lambda: display_clue(remaining_paths[0]), width=15, height=2)
        path_button.grid(row=0, column=1, padx=10)
        text_widget.delete('1.0', tk.END)
        text_widget.insert(tk.END, f"你已完成: {', '.join(completed_paths)}\n只剩一個摁題需要處理了，加油！", 'normal')
    elif len(remaining_paths) == 0:
        dialogue = '我是冠軍 我有金腰帶'
        type_text(text_widget, dialogue)
    else:
        for idx, path in enumerate(remaining_paths):
            path_button = tk.Button(button_frame, text=path, command=lambda p=path: display_clue(p), width=15, height=2)
            path_button.grid(row=0, column=idx, padx=10)
        text_widget.delete('1.0', tk.END)
        text_widget.insert(tk.END, f"你已完成： {', '.join(completed_paths)}\n去解決其他問題吧！", 'normal')

def button_event():
    mybutton.grid_forget()
    global button_frame
    button_frame = tk.Frame(window)
    button_frame.grid(row=3, column=0, columnspan=3, pady=20)

    path1_button = tk.Button(button_frame, text='勇氣', command=lambda: display_clue('勇氣'), width=15, height=2)
    path1_button.grid(row=0, column=0, padx=10)
    
    path2_button = tk.Button(button_frame, text='愛情', command=lambda: display_clue('愛情'), width=15, height=2)
    path2_button.grid(row=0, column=1, padx=10)

    path3_button = tk.Button(button_frame, text='友情', command=lambda: display_clue('友情'), width=15, height=2)
    path3_button.grid(row=0, column=2, padx=10)

# Create the main window
window = tk.Tk()
window.title('RPG')
window.geometry('762x600')

normal_font = tkFont.Font(family='Helvetica', size=12)
bold_font = tkFont.Font(family='Helvetica', size=12, weight='bold')

text_widget = tk.Text(window, font=('Helvetica', 12), wrap='word')
text_widget.grid(row=0, column=0, columnspan=3, pady=20, padx=20)

mybutton = tk.Button(window, text='開始幫助菲利爾', command=button_event, width=20, height=3)

completed_paths = []
if len(sys.argv) > 1:
    completed_paths = sys.argv[1:]
    show_remaining_paths(completed_paths)
else:
    text_widget.insert(tk.END, "Choose a path to begin your journey:", 'normal')

    path1_button = tk.Button(window, text='勇氣', command=lambda: display_clue('勇氣'), width=20, height=3)
    path1_button.grid(row=1, column=0, padx=10, pady=20)

    path2_button = tk.Button(window, text='愛情', command=lambda: display_clue('愛情'), width=20, height=3)
    path2_button.grid(row=1, column=1, padx=10, pady=20)

    path3_button = tk.Button(window, text='友情', command=lambda: display_clue('友情'), width=20, height=3)
    path3_button.grid(row=1, column=2, padx=10, pady=20)

window.mainloop()
