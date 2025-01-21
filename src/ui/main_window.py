import os
import math
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTextEdit, QMenuBar, QMenu, QFileDialog, QStackedWidget, QLabel, QPushButton, QLineEdit
from PySide6.QtGui import QAction, QPixmap, QFont
from PySide6.QtCore import Qt

from ..logic.xml_tools import check_well_formedness, validate_xml
from ..logic.DTP_tools import count_pages_docx, count_slides_pptx, count_pages_pdf, is_editable_pdf, calculate_dtp_time

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.tr("DTP & XML Tools"))
        self.setGeometry(100, 100, 800, 600)

        # Load the logo once to use in both the home screen and menu
        self.pixmap = QPixmap('./src/img/logo.png')  # Ensure path is correct

        # Main Layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        # StackedWidget to switch between different feature views
        self.stacked_widget = QStackedWidget(self)
        self.layout.addWidget(self.stacked_widget)

        # Create all feature windows
        self.home_widget = self.create_home_widget()
        self.xml_well_formedness_widget = self.create_feature_widget(self.tr("Checking XML Well-formedness"))
        self.xml_validation_widget = self.create_feature_widget(self.tr("Validating XML against DTD/STD"))
        self.page_slide_counter_widget = self.create_feature_widget(self.tr("Counting pages/slides"))

        # Add all widgets to the stacked widget
        self.stacked_widget.addWidget(self.home_widget)
        self.stacked_widget.addWidget(self.xml_well_formedness_widget)
        self.stacked_widget.addWidget(self.xml_validation_widget)
        self.stacked_widget.addWidget(self.page_slide_counter_widget)

        # Display the home widget initially
        self.stacked_widget.setCurrentWidget(self.home_widget)

        # Menu Bar
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        # Add logo to the menu bar (top-left)
        self.add_logo_to_menu()

        # File Menu
        file_menu = QMenu(self.tr("File"), self)
        self.menu_bar.addMenu(file_menu)
        exit_action = QAction(self.tr("Exit"), self)
        exit_action.triggered.connect(self.close)  # Connect Exit to close the application
        file_menu.addAction(exit_action)

        # XML Tools Menu
        xml_menu = QMenu(self.tr("XML Tools"), self)
        self.menu_bar.addMenu(xml_menu)
        xml_menu.addAction(self.tr("Check XML Well-formedness"), self.show_xml_well_formedness)
        xml_menu.addAction(self.tr("Validate XML against DTD/STD"), self.show_xml_validation)

        # DTP Tools Menu
        dtp_menu = QMenu(self.tr("DTP Tools"), self)
        self.menu_bar.addMenu(dtp_menu)
        dtp_menu.addAction(self.tr("Page/Slide Counter"), self.show_page_slide_counter)

    def add_logo_to_menu(self):
        """Add the logo to the menu bar at the top-left side."""
        logo_label = QLabel(self)
        
        # Scale the logo to fit the menu height while maintaining its aspect ratio
        scaled_pixmap = self.pixmap.scaledToHeight(self.menuBar().height(), Qt.TransformationMode.FastTransformation)
        logo_label.setPixmap(scaled_pixmap)

        # Add logo to the left side of the menu bar
        self.menu_bar.setCornerWidget(logo_label, Qt.TopLeftCorner)

    def create_home_widget(self):
        """Create and return the home widget displaying the logo and title."""
        widget = QWidget()
        layout = QVBoxLayout()

        # Add Logo
        self.logo_label = QLabel(self)
        scaled_pixmap = self.pixmap.scaled(self.size().width() * 0.5, self.size().height() * 0.3, Qt.AspectRatioMode.KeepAspectRatio)
        self.logo_label.setPixmap(scaled_pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.logo_label)

        # Add Title
        title_label = QLabel(self.tr("Welcome to DTP & XML Tools"))
        title_label.setAlignment(Qt.AlignCenter)

        # Convert text to uppercase
        title_label.setText(title_label.text().upper())

        # Set custom font properties
        font = QFont("Lato", 24, QFont.Light)  # Font size 24, light weight
        title_label.setFont(font)

        layout.addWidget(title_label)

        widget.setLayout(layout)
        return widget

    def create_feature_widget(self, title_text):
        """Create a generic feature widget with result area, back home button, and export log button."""
        widget = QWidget()
        layout = QVBoxLayout()

        # Create the result area
        result_area = QTextEdit(widget)
        result_area.setReadOnly(True)
        layout.addWidget(result_area)

        # Add Go Back Home Button
        back_home_button = QPushButton(self.tr("Go Back Home"), widget)
        back_home_button.clicked.connect(self.go_back_home)
        layout.addWidget(back_home_button)

        # Add Export Log Button (Initially Disabled)
        export_log_button = QPushButton(self.tr("Export Log"), widget)
        export_log_button.setEnabled(False)  # Initially disabled
        export_log_button.clicked.connect(lambda: self.export_log(result_area.toPlainText()))
        layout.addWidget(export_log_button)

        # Add user input for specific times
        self.word_time_input = QLineEdit(self)
        self.word_time_input.setPlaceholderText(self.tr("Word files: Enter DTP time per page. (Optional) (Default value: 5 min/page)"))
        layout.addWidget(self.word_time_input)

        self.ppt_time_input = QLineEdit(self)
        self.ppt_time_input.setPlaceholderText(self.tr("Power Point files: Enter DTP time per page. (Optional) (Default value: 7 min/slide)"))
        layout.addWidget(self.ppt_time_input)

        self.pdf_time_input = QLineEdit(self)
        self.pdf_time_input.setPlaceholderText(self.tr("Editable PDF files: Enter DTP time per page. (Optional) (Default value: 15 min/page)"))
        layout.addWidget(self.pdf_time_input)

        # Store result area and export button for later access
        widget.result_area = result_area
        widget.export_log_button = export_log_button

        widget.setLayout(layout)
        return widget

    def go_back_home(self):
        """Switch to the home screen."""
        self.stacked_widget.setCurrentWidget(self.home_widget)

    def show_xml_well_formedness(self):
        self.stacked_widget.setCurrentWidget(self.xml_well_formedness_widget)
        path = QFileDialog.getExistingDirectory(self, self.tr("Select XML Directory"))
        if not path:
            return

        self.xml_well_formedness_widget.result_area.clear()
        self.xml_well_formedness_widget.result_area.append(self.tr("Checking XML Well-formedness in: {0}\n").format(path))

        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(".xml"):
                    file_path = os.path.join(root, file)
                    well_formed, error = check_well_formedness(file_path)
                    if well_formed:
                        self.xml_well_formedness_widget.result_area.append(self.tr("{0}: Well-formed").format(file))
                    else:
                        self.xml_well_formedness_widget.result_area.append(self.tr("{0}: Not well-formed. Error: {1}").format(file, error))

        # Enable Export Log Button once there are results
        self.xml_well_formedness_widget.export_log_button.setEnabled(True)

    def show_xml_validation(self):
        self.stacked_widget.setCurrentWidget(self.xml_validation_widget)
        xml_path = QFileDialog.getExistingDirectory(self, self.tr("Select XML Directory"))
        dtd_path = QFileDialog.getExistingDirectory(self, self.tr("Select DTD/STD Directory"))
        if not xml_path or not dtd_path:
            return

        self.xml_validation_widget.result_area.clear()
        self.xml_validation_widget.result_area.append(self.tr("Validating XML files in: {0} against DTD/STD files in: {1}\n").format(xml_path, dtd_path))

        # Placeholder for validation logic
        self.xml_validation_widget.result_area.append(self.tr("Validation feature is under development."))

        # Enable Export Log Button once there are results
        self.xml_validation_widget.export_log_button.setEnabled(True)

    def show_page_slide_counter(self):
        self.stacked_widget.setCurrentWidget(self.page_slide_counter_widget)
        path = QFileDialog.getExistingDirectory(self, self.tr("Select Directory"))
        if not path:
            return

        # Get custom times or default from dtp_time dictionary
        word_time = self.word_time_input.text() or '5'
        ppt_time = self.ppt_time_input.text() or '7'
        pdf_time = self.pdf_time_input.text() or '15'
        
        self.page_slide_counter_widget.result_area.clear()
        self.page_slide_counter_widget.result_area.append("==================================================================")
        self.page_slide_counter_widget.result_area.append(self.tr("Counting pages/slides in:\n{0}").format(path))
        self.page_slide_counter_widget.result_area.append("==================================================================")

        total_time = 0

        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                ext = file.lower().split('.')[-1]

                try:
                    if ext in ['doc', 'docx', 'docm']:
                        num_pages = count_pages_docx(file_path)
                        time = calculate_dtp_time('word', num_pages, word_time)
                        total_time += time
                        self.page_slide_counter_widget.result_area.append(self.tr("File: '{0}' ({1} pages)\nDTP time: {2:.2f} hours").format(file, num_pages, time))
                        self.page_slide_counter_widget.result_area.append("------------------------------------------------------------------")

                    elif ext in ['ppt', 'pptx', 'ptm']:
                        num_slides = count_slides_pptx(file_path)
                        time = calculate_dtp_time('ppt', num_slides, ppt_time)
                        total_time += time
                        self.page_slide_counter_widget.result_area.append(self.tr("File: '{0}' ({1} slides)\nDTP time: {2:.2f} hours").format(file, num_slides, time))
                        self.page_slide_counter_widget.result_area.append("------------------------------------------------------------------")

                    elif ext == 'pdf':
                        num_pages = count_pages_pdf(file_path)
                        pdf_type = self.tr("Editable PDF") if is_editable_pdf(file_path) else self.tr("Not-editable PDF")
                        time = calculate_dtp_time('pdf', num_pages, pdf_time)
                        total_time += time
                        self.page_slide_counter_widget.result_area.append(self.tr("File: '{0}' ({2}:{1} pages)\nDTP time: {3:.2f} hours").format(file, num_pages, pdf_type, time))
                        self.page_slide_counter_widget.result_area.append("------------------------------------------------------------------")

                except Exception as e:
                    self.page_slide_counter_widget.result_area.append(self.tr("{0}: Error processing file. {1}").format(file, str(e)))
                    self.page_slide_counter_widget.result_area.append("------------------------------------------------------------------")

        self.page_slide_counter_widget.result_area.append("==================================================================")
        self.page_slide_counter_widget.result_area.append(self.tr("Total Estimated DTP Time: {0:.2f} hours").format(total_time))
        self.page_slide_counter_widget.result_area.append("==================================================================")

        # Enable Export Log Button once there are results
        self.page_slide_counter_widget.export_log_button.setEnabled(True)

    def export_log(self, log_text):
        """Export log to a .txt file."""
        file_path, _ = QFileDialog.getSaveFileName(self, self.tr("Save Log"), "", self.tr("Text Files (*.txt)"))
        if file_path:
            with open(file_path, 'w') as file:
                file.write(log_text)

