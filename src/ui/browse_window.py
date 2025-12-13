"""
Browse Mode Window - Load XML from file browser
"""
from typing import Optional
from PySide6.QtWidgets import QPushButton, QLineEdit, QFileDialog, QMessageBox, QLabel, QVBoxLayout, QHBoxLayout, \
    QWidget
from PySide6.QtCore import Qt
import xml.etree.ElementTree as ET

from .base_xml_window import BaseXMLWindow

# Utilities imports
from ..utils import file_io


class BrowseWindow(BaseXMLWindow):
    """Browse mode window for loading XML from files."""

    def __init__(self) -> None:
        self.file_path_box: QLineEdit = QLineEdit()

        super().__init__(
            window_title="🌐 SocialNet XML Parser - Browse Mode",
            mode_name="Browse mode"
        )

    def _setup_input_section(self, parent_layout: QVBoxLayout) -> None:
        """Set up the file browser input section."""
        # File selection area
        file_widget = QWidget()
        file_widget.setObjectName("filePanel")
        file_layout = QVBoxLayout(file_widget)
        file_layout.setContentsMargins(20, 20, 20, 20)
        file_layout.setSpacing(15)

        file_title = QLabel("Load XML Data")
        file_title.setStyleSheet("""
            QLabel {
                color: rgba(100, 230, 255, 255);
                font-size: 22px;
                font-weight: bold;
            }
        """)
        file_layout.addWidget(file_title)

        file_input_layout = QHBoxLayout()
        self.file_path_box.setPlaceholderText("/path/to/your/file.xml")
        self.file_path_box.setObjectName("fileInput")
        self.file_path_box.setMinimumHeight(40)

        browse_btn = QPushButton("📁 Browse")
        browse_btn.setObjectName("browseFileBtn")
        browse_btn.setMinimumHeight(40)
        browse_btn.setMinimumWidth(120)
        browse_btn.clicked.connect(self.browse)

        upload_btn = QPushButton("⬆ Upload")
        upload_btn.setObjectName("uploadBtn")
        upload_btn.setMinimumHeight(40)
        upload_btn.setMinimumWidth(180)
        upload_btn.clicked.connect(self.upload)

        file_input_layout.addWidget(self.file_path_box)
        file_input_layout.addWidget(browse_btn)
        file_input_layout.addWidget(upload_btn)

        file_layout.addLayout(file_input_layout)
        parent_layout.addWidget(file_widget)

    def _get_panel_selector(self) -> str:
        """Return the panel selector for stylesheet."""
        return "#filePanel, #resultPanel, #opsPanel"

    def _get_initialization_message(self) -> str:
        """Return the initialization message."""
        return "Ready to load XML file."

    def browse(self) -> None:
        """Handle file browsing."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select XML File",
            "",
            "XML Files (*.xml);;All Files (*)"
        )
        if file_path:
            if self.file_path_box:
                self.file_path_box.setText(file_path)

    def upload(self) -> None:
        """Handle file upload and parsing."""
        if not self.file_path_box.text():
            QMessageBox.warning(self, "No File", "Please select an XML file first.")
            return

        file_path = self.file_path_box.text()
        _,self.input_text = file_io.read_file(file_path)
        QMessageBox.information(
            self,
            "Success",
            f"File loaded successfully!\nData is ready for operations."
        )
        self.xml_controller.xml_data = ET.fromstring(self.input_text)
        if self.data_controller:
            self.data_controller.set_xml_data(self.xml_controller.get_xml_data())
        if self.graph_controller:
            self.graph_controller.set_xml_data(self.xml_controller.get_xml_data())