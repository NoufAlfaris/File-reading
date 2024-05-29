import tkinter as tk
import re
from  tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os

# Method to open a text file, separate words and numbers, and handle exceptions
def separate_numbers_and_words(file):
    numbersList = []
    wordsList = []
    ignoredLines = []

    specialCharactersPattern = re.compile(r'[!@#$%^&*(),.?":{}|<>]')

    try:
        # Open the specified file in read mode
        with open(file, 'r') as f:
            for line in f:
                
                for word in line.split():  # Check if number/word or special characters and add to appropriate list
                    if specialCharactersPattern.search(word):
                        ignoredLines.append(word)  # Collect ignored words
                        
                    if word.isdigit():
                        numbersList.append(word)
                    if word.isalpha():
                        wordsList.append(word)

        if not os.path.getsize(file) > 0:
            messagebox.showerror("Error", "File empty")
        else:
            if not numbersList and not wordsList:
                messagebox.showerror("Error", "Invalid input")

        if ignoredLines:
            ignoredMessage = "The following words were ignored due to special characters:\n" + "\n".join(ignoredLines)
            messagebox.showinfo("Info", ignoredMessage)
    except FileNotFoundError: # handle possible exceptions for file opening
        messagebox.showerror("Error", "File not found!")
    except PermissionError:
        messagebox.showerror("Error", "Permission denied to access the file!")
    except IOError:
        messagebox.showerror("Error", "Error reading the file!")
    except UnicodeDecodeError:
        messagebox.showerror("Error", "Invalid Type! Unable to decode file. please enter a valid txt file")
    # Return the two lists containing words and numbers in the file
    return numbersList, wordsList



#Method to display numbers and words from the selected file
def process_file():
    global numbersList, wordsList
    file_path = filedialog.askopenfilename() # Prompt the user to select a file
    if file_path:
        numbersList, wordsList = separate_numbers_and_words(file_path)
        # Clear existing content in the numbers and words text widgets
        numbers_text.delete(1.0, tk.END)
        words_text.delete(1.0, tk.END)
        # Insert the numbers and words into the text widgets
        numbers_text.insert(tk.END, "\n".join(numbersList))
        words_text.insert(tk.END, "\n".join(wordsList))



# Method to download a file containing numbers
def download_number_file():
    # Prompt the user to select a location to save the file
    file_path = filedialog.asksaveasfilename(defaultextension='.txt')
    if file_path:
        try:
            # Open the selected file in write mode
            with open(file_path, "w") as file:
                # convert numbers list to a string and write it to the file
                file.write("\n".join(map(str, numbersList)))
            messagebox.showinfo("Success", "Numbers file downloaded successfully!")
        except IOError:
            messagebox.showerror("Error", "Error downloading numbers file!")

# Method to download a file containing words
def download_word_file():
    file_path = filedialog.asksaveasfilename(defaultextension='.txt')
    if file_path:
        try:
            with open(file_path, "w") as file:
                # convert words list to a string
                file.write("\n".join(map(str, wordsList)))
            messagebox.showinfo("Success", "Words file downloaded successfully!")
        except IOError:
            messagebox.showerror("Error", "Error downloading words file!")

root = tk.Tk()
root.title("Python file generator") #set the title of thr window
root.geometry("800x600") # Set the size of the window

# Label to provide instruction to the user
instruction_label = tk.Label(root, text="Upload a text file to output a list of words and list of numbers")
instruction_label.grid(row=0, column=0, columnspan=2, pady=5, sticky="nsew") #center

# Button to upload a file
upload_button = tk.Button(root, text="Upload file", command=process_file, width=20, height=2)
upload_button.grid(row=1, column=0, columnspan=2, pady=5, sticky="nsew") #center

# Label for the words list
words_label = tk.Label(root, text="Words list")
words_label.grid(row=2, column=0, sticky="e") #to the right

# Text widget to display words
words_text = tk.Text(root, width=40, height=20)
words_text.grid(row=3, column=0, sticky="nsew")

# Label for the numbers list
numbers_label = tk.Label(root, text="Numbers list")
numbers_label.grid(row=2, column=1, sticky="w") #to the left

# Text widget to display numbers
numbers_text = tk.Text(root, width=40, height=20)
numbers_text.grid(row=3, column=1, sticky="nsew")

# Button to generate a file containing words list
generate_words_button = tk.Button(root, text="Generate words file", command=download_word_file, width=20, height=2)
generate_words_button.grid(row=4, column=0, padx=5, sticky="nsew") #center

# Button to generate a file containing numbers list
generate_numbers_button = tk.Button(root, text="Generate numbers file", command=download_number_file, width=20, height=2)
generate_numbers_button.grid(row=4, column=1, padx=5, sticky="nsew") #center

#configure rows and columns to make widgets expandable
root.grid_rowconfigure((0, 1, 3), weight=1)
root.grid_columnconfigure((0, 1), weight=1)

root.mainloop()
