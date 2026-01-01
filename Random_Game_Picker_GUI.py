# What are you doing in here? Go use the damn program and play games!
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import random
import subprocess
import json
import os

def load_gamelist():
    if os.path.exists("gamelist.json"):
        with open("gamelist.json", "r") as f:
            return json.load(f)
    else:
        return []

def save_gamelist():
    with open("gamelist.json", "w") as f:
        json.dump(gamelist, f, indent=4)

gamelist = load_gamelist()

def pick_game_gui():
    if not gamelist:
        messagebox.showwarning("Empty List", "Add some games first, dummy!")
        return
    
    chosen = random.choice(gamelist)
    label_result.config(text=f"Selected: {chosen['name']}")
    def launch():
        clean_path = os.path.normpath(chosen['path'])
        command = [clean_path] + chosen['args']
        try:
            subprocess.Popen(command)
            root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch game: {e}")
    root.after(1400, launch)

def update_listbox():
    game_listbox.delete(0, tk.END)
    for game in gamelist:
        game_listbox.insert(tk.END, game['name'])

def browse_for_path(target_entry):
    filename = filedialog.askopenfilename(
        title="Select Game Executable",
        filetypes=(("Executable files", "*.exe"), ("All files", "*"))
    )
    if filename:
        universal_path = os.path.normpath(filename)
        target_entry.delete(0, tk.END)
        target_entry.insert(0, universal_path)

def open_add_window():
    add_win = tk.Toplevel(root)
    add_win.title("Add New Game")
    add_win.geometry("500x200")

    tk.Label(add_win, text="Game Name:").pack(pady=5)
    name_entry = tk.Entry(add_win, width=30)
    name_entry.pack()

    tk.Label(add_win, text="File Path:").pack(pady=5)
    path_entry = tk.Entry(add_win, width=50)
    path_entry.pack()

    ttk.Button(add_win, text="Browse...", 
          command=lambda: browse_for_path(path_entry)).pack(pady=5)
    
    def submit():
        name = name_entry.get()
        path = path_entry.get()
        if name and path:
            gamelist.append({"name": name, "path": path, "args": []})
            save_gamelist()
            update_listbox()
            add_win.destroy()
        else:
            messagebox.showwarning("Error", "Both fields required")

    ttk.Button(add_win, text="Save Game", command=submit).pack(pady=20)

def open_edit_window():
    try:
        selected_index = game_listbox.curselection()[0]
        game_to_edit = gamelist[selected_index]

        edit_win = tk.Toplevel(root)
        edit_win.title(f"Edit {game_to_edit['name']}")
        edit_win.geometry("500x200")

        tk.Label(edit_win, text="Game Name:").pack(pady=5)
        name_entry = tk.Entry(edit_win, width=30)
        name_entry.insert(0, game_to_edit['name'])
        name_entry.pack()

        tk.Label(edit_win, text="File Path:").pack(pady=5)
        path_entry = tk.Entry(edit_win, width=50)
        path_entry.insert(0, game_to_edit['path'])
        path_entry.pack()

        ttk.Button(edit_win, text="Browse...", 
          command=lambda: browse_for_path(path_entry)).pack(pady=5)

        def save_changes():
            game_to_edit['name'] = name_entry.get()
            game_to_edit['path'] = path_entry.get()
            
            save_gamelist()
            update_listbox()
            edit_win.destroy()
            messagebox.showinfo("Success", "Game updated!")

        ttk.Button(edit_win, text="Save Changes", command=save_changes).pack(pady=20)
        
    except IndexError:
        messagebox.showwarning("Select Game", "Please select a game to edit.")

def remove_game_gui():
    try:
        selected_index = game_listbox.curselection()[0]
        removed_game = gamelist.pop(selected_index)
        save_gamelist()
        update_listbox()
        messagebox.showinfo("Removed", f"Removed {removed_game['name']} from the list.")
    except IndexError:
        messagebox.showwarning("Select Game", "Please select a game to remove.")

root = tk.Tk()
root.title("Random Game Picker")

label_title = tk.Label(root, text="Random Picker", font=("Arial", 14))
label_title.grid(row=0, column=0, padx=10, pady=10)

btn_pick = ttk.Button(root, text="ROLL THE DICE", command=pick_game_gui)
btn_pick.grid(row=1, column=0, padx=10)

label_result = tk.Label(root, text="", font=("Arial", 12, "bold"))
label_result.grid(row=2, column=0, pady=20)

tk.Label(root, text="Your Games:").grid(row=0, column=1, sticky="w")

btn_open_add = ttk.Button(root, text="+ Add", command=open_add_window)
btn_open_add.grid(row=0, column=1, sticky="e", padx=10)

game_listbox = tk.Listbox(root, width=30)
game_listbox.grid(row=1, column=1, rowspan=2, padx=10)


btn_frame = tk.Frame(root)
btn_frame.grid(row=3, column=1, pady=5)

btn_edit = ttk.Button(btn_frame, text="Edit Selected", command=open_edit_window)
btn_edit.pack(side="left", padx=5)

btn_remove = ttk.Button(btn_frame, text="Remove Selected", command=remove_game_gui)
btn_remove.pack(side="left", padx=5)

update_listbox()

root.mainloop()
# Editorial comment: This code was a fun learning experience in python and tkinter, i  hope you enjoy using it as much as I enjoyed making it!