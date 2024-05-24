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
    global button_frame
    button_frame = tk.Frame(window)
    button_frame.grid(row=3, column=0, columnspan=3, pady=20)  # Place the frame below the text widget

    # Create and pack three buttons horizontally within the frame
    path1_button = tk.Button(button_frame, text='勇氣', command=lambda: display_clue('勇氣'), width=15, height=2)
    path1_button.grid(row=0, column=0, padx=10)  # Adjust the padx values as needed
    
    path2_button = tk.Button(button_frame, text='愛情', command=lambda: display_clue('愛情'), width=15, height=2)
    path2_button.grid(row=0, column=1, padx=10)  # Adjust the padx value as needed

    path3_button = tk.Button(button_frame, text='友情', command=lambda: display_clue('友情'), width=15, height=2)
    path3_button.grid(row=0, column=2, padx=10)  # Adjust the padx values as needed

def display_clue(path):
    clues = {
        '勇氣': 'You need to find the wise old man in the forest.',
        '愛情': 'Seek the maiden in the town square.',
        '友情': 'Look for the blacksmith in the village.'
    }
    clue_text = clues.get(path, 'Unknown path')

    # Hide path buttons
    button_frame.grid_forget()
    
    # Display the clue in the text widget
    text_widget.delete('1.0', tk.END)
    text_widget.insert(tk.END, clue_text, 'normal')

    # Create the button to proceed
    proceed_button = tk.Button(window, text='Understood', command=lambda: open_python_file(path), width=20, height=3)
    proceed_button.grid(row=5, column=1, pady=20)

def open_python_file(path):
    file_names = {
        '勇氣': 'map.py',
        '愛情': 'path2.py',
        '友情': 'path3.py'
    }
    file_name = file_names.get(path, 'path3.py')
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
dialogue = 'asdasdasdasd'

# Start typing the text
type_text(text_widget, dialogue)

# Run the main loop to display the window
window.mainloop()
