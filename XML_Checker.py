import tkinter as tk
from tkinter import filedialog, messagebox
from src import gui  # Import the GUI module
from src.logic import xml_validator # Import the xml_validator

# Run the GUI
if __name__ == "__main__":
    gui.create_gui()  # Launches GUI and passes xml_validator to the GUI function
