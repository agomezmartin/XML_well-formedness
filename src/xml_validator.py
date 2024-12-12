# src/xml_validator.py
import os
import xml.etree.ElementTree as ET
from datetime import datetime
from . import messages  # Import the messages from the src folder

# Function to validate XML well-formedness
def validate_xml(file_path):
    try:
        tree = ET.parse(file_path)
        return True, messages.VALID_XML.format(os.path.basename(file_path))
    except ET.ParseError as e:
        return False, messages.INVALID_XML.format(os.path.basename(file_path)) + f"\n{messages.PARSE_ERROR.format(e)}"

# Function to allow the user to select the directory containing XML files
def select_directory(filedialog):
    directory = filedialog.askdirectory(title=messages.SELECT_DIRECTORY)
    return directory

# Function to allow the user to select the path to save the log
def save_log_path(filedialog):
    log_dir = filedialog.askdirectory(title=messages.SELECT_LOG_DIRECTORY)
    if log_dir:
        log_filename = filedialog.asksaveasfilename(initialdir=log_dir, defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        return log_filename
    return None

# Function to validate all XML files in a given directory and log the results
def validate_all_xml_files(directory, log_file):
    try:
        with open(log_file, 'a') as log:
            log.write(f"{messages.LOG_HEADER} {directory}\n")
            log.write(messages.LOG_TIMESTAMP.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "\n")
            log.write(messages.LOG_SEPARATOR + "\n")
            
            # Get all XML files in the directory
            xml_files = [f for f in os.listdir(directory) if f.lower().endswith(".xml")]
            
            if not xml_files:
                return messages.NO_XML_FILES_FOUND
            
            # Loop through each XML file and validate
            for xml_file in xml_files:
                file_path = os.path.join(directory, xml_file)
                result, message = validate_xml(file_path)
                log.write(f"{messages.VALIDATED_FILE.format(os.path.basename(file_path))}\n")
                log.write(f"{messages.RESULT_SUCCESS if result else messages.RESULT_FAILURE}\n")
                log.write(f"{messages.ERROR_MESSAGE.format(message)}\n")
                log.write(messages.LOG_SEPARATOR + "\n")
            
            return messages.LOG_SAVED + log_file
    except Exception as e:
        return messages.LOG_FILE_ERROR + str(e)

# Function to create the main GUI window
def create_gui(tk, filedialog, messagebox):
    # Create the main window
    root = tk.Tk()
    root.title("XML Validator with Log")
    root.geometry("300x200")  # Width x Height

    # Add a button to trigger the directory selection and validation
    validate_button = tk.Button(root, text=messages.SELECT_DIRECTORY, command=lambda: select_directory_action(filedialog, messagebox))
    validate_button.pack(pady=30)

    # Run the application
    root.mainloop()

def select_directory_action(filedialog, messagebox):
    directory = select_directory(filedialog)
    if directory:
        log_file = save_log_path(filedialog)
        if log_file:
            result = validate_all_xml_files(directory, log_file)
            if "Results saved to log file" in result:
                messagebox.showinfo("Log Saved", result)
            else:
                messagebox.showwarning("Warning", result)
