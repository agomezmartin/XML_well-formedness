import os
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTranslator, QLocale
from src.ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)

    # Load translations
    translator = QTranslator()
    locale = QLocale.system().name()
    translation_path = os.path.join(os.path.dirname(__file__), 'translations', f'{locale}.qm')
    if os.path.exists(translation_path):
        translator.load(translation_path)
        app.installTranslator(translator)

    # Launch Main Window
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
