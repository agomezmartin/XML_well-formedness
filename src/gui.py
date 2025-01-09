import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Frame, Button, Label
from tkinter.scrolledtext import ScrolledText  # Import ScrolledText widget
from . import messages  # Importing messages from the src folder
from .logic.xml_validator import validate_all_xml_files, validate_with_dtd_std, select_directory, save_log_path
from .logic.page_slide_counter import count_pages_and_slides_in_directory

def create_gui():
    # Create the main window
    root = tk.Tk()
    root.title(messages.GUI_TITLE)
    root.geometry("600x400")  # Adjust this if needed for better fitting
    root.configure(bg="lightgrey")  # Set background to light grey for a macOS-like look

    # Create a main frame to hold all content
    main_frame = tk.Frame(root, bg="lightgrey", padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Create a ScrolledText widget for log content display (only once)
    log_text = ScrolledText(main_frame, width=70, height=10, wrap=tk.WORD, bg="white", fg="black", font=("Helvetica", 12))
    log_text.pack(pady=(20, 10), fill=tk.BOTH, expand=True)

    # Function to show the welcome screen
    def show_welcome_screen():
        # Clear the main frame but keep the log_text
        for widget in main_frame.winfo_children():
            if widget != log_text:
                widget.pack_forget()

        # Add a welcome message
        welcome_label = tk.Label(
            main_frame,
            text=messages.GUI_TITLE,
            font=("Helvetica", 18, "bold"),
            bg="lightgrey",
            fg="black",
            anchor="center"
        )
        welcome_label.pack(pady=(50, 20))

    # Function to show the check well-formedness screen
    def show_check_well_formedness():
        # Clear the main frame but keep the log_text
        for widget in main_frame.winfo_children():
            if widget != log_text:
                widget.pack_forget()

        # Add a title label
        title_label = tk.Label(
            main_frame,
            text=messages.CHECK_WITH_PARSER,
            font=("Helvetica", 18, "bold"),
            bg="lightgrey",
            fg="black",
            anchor="center"
        )
        title_label.pack(pady=(10, 20))

        # Add a button for directory validation
        validate_button = tk.Button(
            main_frame,
            text=messages.CHECK_WITH_PARSER,
            font=("Helvetica", 14),
            command=lambda: select_directory_action(filedialog, messagebox, log_text),
            width=35,
            bg="white",
            fg="black",
            relief="flat",
            wraplength=300,  # Wrap the text if too long
            justify="center"
        )
        validate_button.pack(pady=10, padx=10)

        # Add a back button to return to the welcome screen
        back_button = tk.Button(
            main_frame,
            text=messages.BACK_TO_WELCOME_BUTTON,
            font=("Helvetica", 12),
            command=show_welcome_screen,
            bg="lightblue",
            fg="black",
            relief="flat",
            width=20
        )
        back_button.pack(pady=10)

    # Function to show the validate with DTD/STD screen
    def show_validate_dtd_std():
        # Clear the main frame but keep the log_text
        for widget in main_frame.winfo_children():
            if widget != log_text:
                widget.pack_forget()

        # Add a title label
        title_label = tk.Label(
            main_frame,
            text=messages.VALIDATE_WITH_DTD_STD,
            font=("Helvetica", 18, "bold"),
            bg="lightgrey",
            fg="black",
            anchor="center"
        )
        title_label.pack(pady=(10, 20))

        # Add a button for DTD/STD validation
        validate_dtd_std_button = tk.Button(
            main_frame,
            text=messages.VALIDATE_WITH_DTD_STD,
            font=("Helvetica", 14),
            command=lambda: validate_with_dtd_std_action(filedialog, messagebox, log_text),
            width=35,
            bg="white",
            fg="black",
            relief="flat",
            wraplength=300,  # Ensure text wraps if it's too long
            justify="center"
        )
        validate_dtd_std_button.pack(pady=10, padx=10)

        # Add a back button to return to the welcome screen
        back_button = tk.Button(
            main_frame,
            text=messages.BACK_TO_WELCOME_BUTTON,
            font=("Helvetica", 12),
            command=show_welcome_screen,
            bg="lightblue",
            fg="black",
            relief="flat",
            width=20
        )
        back_button.pack(pady=10)

    # Function to show page/slide counter screen
    def show_page_slide_counter():
        # Clear the main frame but keep the log_text
        for widget in main_frame.winfo_children():
            if widget != log_text:
                widget.pack_forget()

        # Add a title label
        title_label = tk.Label(
            main_frame,
            text=messages.PAGE_SLIDE_COUNTER,
            font=("Helvetica", 18, "bold"),
            bg="lightgrey",
            fg="black",
            anchor="center"
        )
        title_label.pack(pady=(10, 20))

        # Add a button for counting pages/slides
        count_button = tk.Button(
            main_frame,
            text=messages.START_BUTTON,
            font=("Helvetica", 14),
            command=lambda: count_pages_slides_action(filedialog, messagebox, log_text),
            width=35,
            bg="white",
            fg="black",
            relief="flat",
            wraplength=300,  # Wrap the text if too long
            justify="center"
        )
        count_button.pack(pady=10, padx=10)

        # Add a back button to return to the welcome screen
        back_button = tk.Button(
            main_frame,
            text=messages.BACK_TO_WELCOME_BUTTON,
            font=("Helvetica", 12),
            command=show_welcome_screen,
            bg="lightblue",
            fg="black",
            relief="flat",
            width=20
        )
        back_button.pack(pady=10)

    # Functions for actions
    def select_directory_action(filedialog, messagebox, log_text):
        directory = select_directory(filedialog)
        if directory:
            log_file = save_log_path(filedialog)
            if log_file:
                result = validate_all_xml_files(directory, log_file)
                # Insert log content into the ScrolledText widget
                log_text.insert(tk.END, result + "\n")  # Append new log
                log_text.yview(tk.END)  # Auto-scroll to the bottom
                if "Results saved to log file" in result:
                    messagebox.showinfo(messages.LOG_SAVED, result)
                else:
                    messagebox.showwarning(messages.LOG_ERROR, result)

    def validate_with_dtd_std_action(filedialog, messagebox, log_text):
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
            log_text.insert(tk.END, validation_result + "\n")  # Append new log
            log_text.yview(tk.END)  # Auto-scroll to the bottom

            if validation_result:
                messagebox.showinfo(messages.VALIDATION_SUCCESS, validation_result)
            else:
                messagebox.showwarning(messages.VALIDATION_ERROR, validation_result)

    def count_pages_slides_action(filedialog, messagebox, log_text):
        directory = select_directory(filedialog)
        if directory:
            log_file = save_log_path(filedialog)
            if log_file:
                result = count_pages_and_slides_in_directory(directory, log_file)
                log_text.insert(tk.END, result + "\n")  # Append new log
                log_text.yview(tk.END)  # Auto-scroll to the bottom
                if "Results saved to log file" in result:
                    messagebox.showinfo(messages.LOG_SAVED, result)
                else:
                    messagebox.showwarning(messages.LOG_ERROR, result)

    # Create the menu bar after defining all functions
    menubar = tk.Menu(root)
    
    # File top-level menu
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label=messages.FILE_MENU, menu=file_menu)

    # File menu
    xml_tasks_menu = tk.Menu(file_menu, tearoff=0)
    
    # XML Tasks submenu
    file_menu.add_cascade(label=messages.XML_TASKS_MENU, menu=xml_tasks_menu)
    xml_tasks_menu.add_command(label=messages.CHECK_WELL_FORMEDNESS, command=show_check_well_formedness)
    xml_tasks_menu.add_command(label=messages.VALIDATE_WITH_DTD_STD_MENU, command=show_validate_dtd_std)

    # Page/slide counter menu
    file_menu.add_command(label=messages.PAGE_SLIDE_COUNTER, command=show_page_slide_counter)  # New menu item

    root.config(menu=menubar)

    # Start with the welcome screen
    show_welcome_screen()

    # Run the application
    root.mainloop()
