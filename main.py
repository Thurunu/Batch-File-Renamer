import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from collections import Counter

class RenameFiles:
    def __init__(self, directory, new_prefix, selected_types, file_listbox_before, file_listbox_after):
        self.directory = directory
        self.new_prefix = new_prefix
        self.selected_types = selected_types
        self.file_listbox_before = file_listbox_before
        self.file_listbox_after = file_listbox_after

    def rename_files(self):
        if not os.path.isdir(self.directory):
            messagebox.showerror("Error", "Invalid directory.")
            return

        files = os.listdir(self.directory)
        self.file_listbox_before.delete(0, tk.END)
        self.file_listbox_after.delete(0, tk.END)

        i = 1
        for filename in files:
            _, extension = os.path.splitext(filename)
            extension = extension.lstrip('.')
            if extension in self.selected_types:
                new_filename = f"{self.new_prefix}_{i}.{extension}"
                old_filepath = os.path.join(self.directory, filename)
                new_filepath = os.path.join(self.directory, new_filename)

                try:
                    os.rename(old_filepath, new_filepath)
                    self.file_listbox_before.insert(tk.END, filename)
                    self.file_listbox_after.insert(tk.END, new_filename)
                    i += 1
                except OSError as error:
                    messagebox.showerror("Error", f"Error renaming {filename}: {error}")

        messagebox.showinfo("Success", "Files renamed successfully!")

# GUI functions
def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        dir_entry.delete(0, tk.END)
        dir_entry.insert(0, directory)
        update_file_list(directory)
        update_file_types_dropdown(directory)

def update_file_list(directory, file_type=None):
    file_listbox_before.delete(0, tk.END)
    if os.path.isdir(directory):
        files = os.listdir(directory)
        for file in files:
            if file_type:
                _, extension = os.path.splitext(file)
                if extension.lstrip('.') == file_type:
                    file_listbox_before.insert(tk.END, file)
            else:
                file_listbox_before.insert(tk.END, file)

def update_file_types_dropdown(directory):
    if os.path.isdir(directory):
        files = os.listdir(directory)
        extensions = [os.path.splitext(file)[1].lstrip('.') for file in files if os.path.isfile(os.path.join(directory, file))]
        file_type_counts = Counter(extensions)
        file_types = [f"{file_type} ({count} files)" for file_type, count in file_type_counts.items()]
        file_type_dropdown['values'] = file_types

def file_type_selected(event):
    directory = dir_entry.get()
    selected_file_type = file_type_dropdown.get()
    if directory and selected_file_type:
        selected_type = selected_file_type.split()[0]
        update_file_list(directory, file_type=selected_type)

def perform_rename():
    directory = dir_entry.get()
    new_prefix = name_entry.get()

    if not directory or not os.path.isdir(directory):
        messagebox.showerror("Error", "Please select a valid directory.")
        return

    if not new_prefix.strip():
        messagebox.showerror("Error", "Please enter a name to add for all files.")
        return

    selected_file_type = file_type_dropdown.get()
    if not selected_file_type:
        messagebox.showerror("Error", "Please select a file type.")
        return

    selected_type = selected_file_type.split()[0]

    renamer = RenameFiles(directory, new_prefix, [selected_type], file_listbox_before, file_listbox_after)
    renamer.rename_files()

# Create the main window
root = tk.Tk()
root.title("Batch File Renamer")
root.geometry("800x600")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

# Style configuration
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Helvetica", 10), padding=5)
style.configure("TLabel", font=("Helvetica", 10), background="#f0f0f0")
style.configure("TCombobox", font=("Helvetica", 10))

# Directory selection
tk.Label(root, text="Browse the directory you want to rename", font=("Helvetica", 12), bg="#f0f0f0").grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=5)
dir_entry = ttk.Entry(root, width=50)
dir_entry.grid(row=1, column=0, padx=10, pady=5)
browse_button = ttk.Button(root, text="Browse", command=browse_directory)
browse_button.grid(row=1, column=1, padx=10, pady=5)

# File type selection
tk.Label(root, text="File types in the directory:", font=("Helvetica", 12), bg="#f0f0f0").grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=5)
file_type_dropdown = ttk.Combobox(root, width=47, state="readonly")
file_type_dropdown.grid(row=3, column=0, columnspan=2, padx=10, pady=5)
file_type_dropdown.bind("<<ComboboxSelected>>", file_type_selected)

# Name input
tk.Label(root, text="Name you want to add for all files:", font=("Helvetica", 12), bg="#f0f0f0").grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=5)
name_entry = ttk.Entry(root, width=50)
name_entry.grid(row=5, column=0, padx=10, pady=5)
rename_button = ttk.Button(root, text="Rename", command=perform_rename)
rename_button.grid(row=5, column=1, padx=10, pady=5)

# File lists
file_listbox_before = tk.Listbox(root, width=40, height=15, bg="white", font=("Courier", 10))
file_listbox_before.grid(row=6, column=0, padx=10, pady=10)
tk.Label(root, text="File names before changing names", font=("Helvetica", 12), bg="#f0f0f0").grid(row=7, column=0, sticky="w", padx=10)

file_listbox_after = tk.Listbox(root, width=40, height=15, bg="white", font=("Courier", 10))
file_listbox_after.grid(row=6, column=1, padx=10, pady=10)
tk.Label(root, text="File names after changed", font=("Helvetica", 12), bg="#f0f0f0").grid(row=7, column=1, sticky="w", padx=10)

# Run the application
root.mainloop()