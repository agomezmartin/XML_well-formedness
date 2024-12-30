import tkinter as tk
from tkinter import filedialog, messagebox
from src import gui, xml_validator  # Import the GUI module and the xml_validator

# Run the GUI
if __name__ == "__main__":
    gui.create_gui(xml_validator)  # Pass xml_validator to the GUI function
