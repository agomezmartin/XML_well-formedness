import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Frame, Button, Label
from . import messages  # Importing messages from the src folder
from .xml_validator import validate_all_xml_files, validate_with_dtd_std, select_directory, save_log_path

def create_gui():
    # Create the main window
    root = tk.Tk()
    root.title(messages.GUI_TITLE)
    root.geometry("450x350")
    root.configure(bg="lightgrey")  # Set background to light grey for a macOS-like look

    # Create a main frame to hold all content
    main_frame = tk.Frame(root, bg="lightgrey", padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Add a title label with macOS-style font
    title_label = tk.Label(
        main_frame,
        text=messages.GUI_TITLE,
        font=("Helvetica", 18, "bold"),
        bg="lightgrey",
        fg="black",
        anchor="center"
    )
    title_label.pack(pady=(10, 20))

    # Add a frame for buttons with a subtle border for a clean layout
    button_frame = tk.Frame(main_frame, bg="lightgrey", highlightbackground="grey", highlightthickness=1)
    button_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    # Add a button for directory validation
    validate_button = tk.Button(
        button_frame,
        text=messages.CHECK_WITH_PARSER,
        font=("Helvetica", 14),
        command=lambda: select_directory_action(filedialog, messagebox),
        width=35,
        bg="white",
        fg="black",
        relief="flat",
        wraplength=300,
        justify="center"
    )
    validate_button.pack(pady=10, padx=10)

    # Add a button for validation using a DTD or STD file
    validate_dtd_std_button = tk.Button(
        button_frame,
        text=messages.VALIDATE_WITH_DTD_STD,
        font=("Helvetica", 14),
        command=lambda: validate_with_dtd_std_action(filedialog, messagebox),
        width=35,
        bg="white",
        fg="black",
        relief="flat",
        wraplength=300,
        justify="center"
    )
    validate_dtd_std_button.pack(pady=10, padx=10)

    # Add an exit button styled for macOS
    exit_button = tk.Button(
        main_frame,
        text=messages.EXIT_BUTTON,
        font=("Helvetica", 14),
        command=root.quit,
        bg="darkgrey",
        fg="white",
        relief="flat",
        width=12
    )
    exit_button.pack(pady=(20, 10))

    # Run the application
    root.mainloop()

def select_directory_action(filedialog, messagebox):
    directory = select_directory(filedialog)
    if directory:
        log_file = save_log_path(filedialog)
        if log_file:
            result = validate_all_xml_files(directory, log_file)
            if "Results saved to log file" in result:
                messagebox.showinfo(messages.LOG_SAVED, result)
            else:
                messagebox.showwarning(messages.LOG_ERROR, result)

def validate_with_dtd_std_action(filedialog, messagebox):
    # Ask the user to select the DTD/STD file
    dtd_std_file = filedialog.askopenfilename(
        title=messages.SELECT_DTD_STD_FILE,
        filetypes=[(messages.ALL_FILES, messages.ALL_FILES_EXTENSION)]
    )

    if not dtd_std_file:
        messagebox.showwarning(messages.ERROR_MESSAGE, messages.FILE_NOT_FOUND_ERROR.format(dtd_std_file))
        return

    # Ask for the directory containing XML files to validate
    directory = select_directory(filedialog)
    if directory:
        # Perform validation with the selected DTD/STD file
        validation_result = validate_with_dtd_std(directory, dtd_std_file)

        if validation_result:
            messagebox.showinfo(messages.VALIDATION_SUCCESS, validation_result)
        else:
            messagebox.showwarning(messages.VALIDATION_ERROR, validation_result)
