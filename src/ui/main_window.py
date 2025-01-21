import os
import math
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTextEdit, QMenuBar, QMenu, QFileDialog, QStackedWidget, QLabel, QPushButton
from PySide6.QtGui import QAction, QPixmap, QFont
from PySide6.QtCore import Qt

from ..logic.xml_tools import check_well_formedness, validate_xml
from ..logic.DTP_tools import count_pages_docx, count_slides_pptx, count_pages_pdf, is_editable_pdf


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.tr("DTP & XML Tools"))
        self.setGeometry(100, 100, 800, 600)

        # Load the logo once to use in both the home screen and menu
        self.pixmap = QPixmap('.\\src\\img\\logo.png')  # Ensure path is correct

        # Main Layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        # StackedWidget to switch between different feature views
        self.stacked_widget = QStackedWidget(self)
        self.layout.addWidget(self.stacked_widget)

        # Create the home screen widget
        self.home_widget = self.create_home_widget()

        # Create the feature windows
        self.xml_well_formedness_widget = self.create_xml_well_formedness_widget()
        self.xml_validation_widget = self.create_xml_validation_widget()
        self.page_slide_counter_widget = self.create_page_slide_counter_widget()

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

        from PySide6.QtGui import QFont

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

    def create_xml_well_formedness_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        self.result_area_well_formedness = QTextEdit(widget)
        self.result_area_well_formedness.setReadOnly(True)
        layout.addWidget(self.result_area_well_formedness)

        # Add Go Back Home Button
        back_home_button = QPushButton(self.tr("Go Back Home"), widget)
        back_home_button.clicked.connect(self.go_back_home)
        layout.addWidget(back_home_button)

        # Add Export Log Button (Initially Disabled)
        self.export_log_button_well_formedness = QPushButton(self.tr("Export Log"), widget)
        self.export_log_button_well_formedness.setEnabled(False)  # Initially disabled
        self.export_log_button_well_formedness.clicked.connect(lambda: self.export_log(self.result_area_well_formedness.toPlainText()))
        layout.addWidget(self.export_log_button_well_formedness)

        widget.setLayout(layout)
        return widget

    def create_xml_validation_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        self.result_area_validation = QTextEdit(widget)
        self.result_area_validation.setReadOnly(True)
        layout.addWidget(self.result_area_validation)

        # Add Go Back Home Button
        back_home_button = QPushButton(self.tr("Go Back Home"), widget)
        back_home_button.clicked.connect(self.go_back_home)
        layout.addWidget(back_home_button)

        # Add Export Log Button (Initially Disabled)
        self.export_log_button_validation = QPushButton(self.tr("Export Log"), widget)
        self.export_log_button_validation.setEnabled(False)  # Initially disabled
        self.export_log_button_validation.clicked.connect(lambda: self.export_log(self.result_area_validation.toPlainText()))
        layout.addWidget(self.export_log_button_validation)

        widget.setLayout(layout)
        return widget

    def create_page_slide_counter_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()
        self.result_area_page_slide = QTextEdit(widget)
        self.result_area_page_slide.setReadOnly(True)
        layout.addWidget(self.result_area_page_slide)

        # Add Go Back Home Button
        back_home_button = QPushButton(self.tr("Go Back Home"), widget)
        back_home_button.clicked.connect(self.go_back_home)
        layout.addWidget(back_home_button)

        # Add Export Log Button (Initially Disabled)
        self.export_log_button_page_slide = QPushButton(self.tr("Export Log"), widget)
        self.export_log_button_page_slide.setEnabled(False)  # Initially disabled
        self.export_log_button_page_slide.clicked.connect(lambda: self.export_log(self.result_area_page_slide.toPlainText()))
        layout.addWidget(self.export_log_button_page_slide)

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

        self.result_area_well_formedness.clear()
        self.result_area_well_formedness.append(self.tr("Checking XML Well-formedness in: {0}\n").format(path))

        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(".xml"):
                    file_path = os.path.join(root, file)
                    well_formed, error = check_well_formedness(file_path)
                    if well_formed:
                        self.result_area_well_formedness.append(self.tr("{0}: Well-formed").format(file))
                    else:
                        self.result_area_well_formedness.append(self.tr("{0}: Not well-formed. Error: {1}").format(file, error))

        # Enable Export Log Button once there are results
        self.export_log_button_well_formedness.setEnabled(True)

    def show_xml_validation(self):
        self.stacked_widget.setCurrentWidget(self.xml_validation_widget)
        xml_path = QFileDialog.getExistingDirectory(self, self.tr("Select XML Directory"))
        dtd_path = QFileDialog.getExistingDirectory(self, self.tr("Select DTD/STD Directory"))
        if not xml_path or not dtd_path:
            return

        self.result_area_validation.clear()
        self.result_area_validation.append(self.tr("Validating XML files in: {0} against DTD/STD files in: {1}\n").format(xml_path, dtd_path))

        # Placeholder for validation logic
        self.result_area_validation.append(self.tr("Validation feature is under development."))

        # Enable Export Log Button once there are results
        self.export_log_button_validation.setEnabled(True)

    def show_page_slide_counter(self):
        self.stacked_widget.setCurrentWidget(self.page_slide_counter_widget)
        path = QFileDialog.getExistingDirectory(self, self.tr("Select Directory"))
        if not path:
            return

        self.result_area_page_slide.clear()
        self.result_area_page_slide.append("==================================================================")
        self.result_area_page_slide.append(self.tr("Counting pages/slides in:\n{0}").format(path))
        self.result_area_page_slide.append("==================================================================")

        dtp_time = {
            self.tr("Word"): 5,
            self.tr("PPT"): 7,
            self.tr("Editable PDF"): 15,
            self.tr("Not-editable PDF"): 30
        }
        total_time = 0

        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                ext = file.lower().split('.')[-1]

                try:
                    if ext in ['doc', 'docx', 'docm']:
                        num_pages = count_pages_docx(file_path)
                        time = (num_pages * dtp_time[self.tr("Word")]) / 60
                        # Round up time to the nearest 0.25
                        time = math.ceil(time * 4) / 4  # Multiply by 4, round up, then divide by 4 to get increments of 0.25
                        total_time += time
                        self.result_area_page_slide.append(self.tr("File: '{0}' ({1} pages)\nDTP time: {2:.2f} hours").format(file, num_pages,time))
                        self.result_area_page_slide.append("------------------------------------------------------------------")

                    elif ext in ['ppt', 'pptx', 'ptm']:
                        num_slides = count_slides_pptx(file_path)
                        time = (num_slides * dtp_time[self.tr("PPT")]) / 60
                        # Round up time to the nearest 0.25
                        time = math.ceil(time * 4) / 4  # Multiply by 4, round up, then divide by 4 to get increments of 0.25
                        total_time += time
                        self.result_area_page_slide.append(self.tr("File: '{0}' ({1} slides)\nDTP time: {2:.2f} hours").format(file, num_slides, time))
                        self.result_area_page_slide.append("------------------------------------------------------------------")

                    elif ext == 'pdf':
                        num_pages = count_pages_pdf(file_path)
                        pdf_type = self.tr("Editable PDF") if is_editable_pdf(file_path) else self.tr("Not-editable PDF")
                        time = (num_pages * dtp_time[pdf_type]) / 60
                        # Round up time to the nearest 0.25
                        time = math.ceil(time * 4) / 4  # Multiply by 4, round up, then divide by 4 to get increments of 0.25
                        total_time += time
                        self.result_area_page_slide.append(self.tr("File: '{0}' ({2}:{1} pages)\nDPT time: {3:.2f} hours").format(file, num_pages, pdf_type, time))
                        self.result_area_page_slide.append("------------------------------------------------------------------")

                except Exception as e:
                    self.result_area_page_slide.append(self.tr("{0}: Error processing file. {1}").format(file, str(e)))

        self.result_area_page_slide.append(self.tr("\nTotal Estimated DTP Time: {0:.2f} hours").format(total_time))

        # Enable Export Log Button once there are results
        self.export_log_button_page_slide.setEnabled(True)

    def export_log(self, log_text):
        """Export log to a .txt file."""
        file_path, _ = QFileDialog.getSaveFileName(self, self.tr("Save Log"), "", self.tr("Text Files (*.txt)"))
        if file_path:
            with open(file_path, 'w') as file:
                file.write(log_text)
