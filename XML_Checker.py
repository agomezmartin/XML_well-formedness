# XML_Checker.py
import tkinter as tk
from tkinter import filedialog, messagebox

from src import xml_validator  # Import the module with all the functions

# Run the GUI from the xml_validator module
if __name__ == "__main__":
    xml_validator.create_gui(tk, filedialog, messagebox)
