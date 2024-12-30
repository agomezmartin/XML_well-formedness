import tkinter as tk
from tkinter import filedialog, messagebox
from . import messages  # Importing messages from the src folder

# Function to create the main GUI window
def create_gui(xml_validator):
    # Create the main window
    root = tk.Tk()
    root.title(messages.GUI_TITLE)  # Add a title for the window
    root.geometry("300x200")  # Width x Height

    # Add a button to trigger the directory selection and validation
    validate_button = tk.Button(
        root,
        text=messages.SELECT_DIRECTORY,
        command=lambda: select_directory_action(xml_validator, filedialog, messagebox)
    )
    validate_button.pack(pady=30)

    # Run the application
    root.mainloop()

def select_directory_action(xml_validator, filedialog, messagebox):
    directory = xml_validator.select_directory(filedialog)
    if directory:
        log_file = xml_validator.save_log_path(filedialog)
        if log_file:
            result = xml_validator.validate_all_xml_files(directory, log_file)
            if "Results saved to log file" in result:
                messagebox.showinfo(messages.LOG_SAVED, result)
            else:
                messagebox.showwarning(messages.LOG_ERROR, result)
