"""Parser tab UI component."""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QLabel, QListWidget, QSplitter, QFileDialog,
    QGroupBox, QMessageBox
)
from PyQt5.QtCore import Qt
from core import CodeParser


class ParserTab(QWidget):
    """Tab for parsing source code and displaying AST output."""

    def __init__(self):
        """Initialize the ParserTab."""
        super().__init__()
        self.parser = CodeParser()
        self.current_code = ""
        self.parsed_data = None
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()

        # Top buttons
        button_layout = QHBoxLayout()

        self.upload_btn = QPushButton("Upload Python File")
        self.upload_btn.clicked.connect(self.upload_file)

        self.paste_btn = QPushButton("Paste Code")
        self.paste_btn.setObjectName("secondaryButton")
        self.paste_btn.clicked.connect(self.paste_code)

        self.parse_btn = QPushButton("Parse Code")
        self.parse_btn.setObjectName("successButton")
        self.parse_btn.clicked.connect(self.parse_code)
        self.parse_btn.setEnabled(False)

        button_layout.addWidget(self.upload_btn)
        button_layout.addWidget(self.paste_btn)
        button_layout.addWidget(self.parse_btn)
        button_layout.addStretch()

        layout.addLayout(button_layout)

        # Main splitter
        splitter = QSplitter(Qt.Horizontal)

        # Left panel
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)

        # Right panel
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)

        layout.addWidget(splitter)
        self.setLayout(layout)

    def create_left_panel(self):
        """Create the left panel with project info."""
        panel = QWidget()
        layout = QVBoxLayout()

        # Parser Accuracy
        accuracy_group = QGroupBox("Parser Accuracy")
        accuracy_layout = QVBoxLayout()

        self.accuracy_label = QLabel("No file parsed yet")
        self.accuracy_label.setObjectName("subHeaderLabel")
        accuracy_layout.addWidget(self.accuracy_label)

        self.coverage_label = QLabel("Coverage: 0%")
        accuracy_layout.addWidget(self.coverage_label)

        accuracy_group.setLayout(accuracy_layout)
        layout.addWidget(accuracy_group)

        # Functions List
        functions_group = QGroupBox("Functions & Classes")
        functions_layout = QVBoxLayout()

        self.functions_list = QListWidget()
        self.functions_list.itemClicked.connect(self.show_function_details)
        functions_layout.addWidget(self.functions_list)

        functions_group.setLayout(functions_layout)
        layout.addWidget(functions_group)

        panel.setLayout(layout)
        return panel

    def create_right_panel(self):
        """Create the right panel with code display."""
        panel = QWidget()
        layout = QVBoxLayout()

        # Source Code Preview
        source_label = QLabel("Source Code Preview:")
        source_label.setObjectName("subHeaderLabel")
        layout.addWidget(source_label)

        self.source_preview = QTextEdit()
        self.source_preview.setReadOnly(True)
        self.source_preview.setPlaceholderText("Upload or paste Python code here...")
        layout.addWidget(self.source_preview)

        # AST Parsing Output
        ast_label = QLabel("Selected Function/Class:")
        ast_label.setObjectName("subHeaderLabel")
        layout.addWidget(ast_label)

        self.ast_output = QTextEdit()
        self.ast_output.setReadOnly(True)
        self.ast_output.setPlaceholderText("Select a function or class from the list to view details...")
        layout.addWidget(self.ast_output)

        panel.setLayout(layout)
        return panel

    def upload_file(self):
        """Handle file upload."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Python File",
            "",
            "Python Files (*.py)"
        )

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.current_code = f.read()
                    self.source_preview.setPlainText(self.current_code)
                    self.parse_btn.setEnabled(True)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to read file: {str(e)}")

    def paste_code(self):
        """Enable pasting code directly."""
        self.source_preview.setReadOnly(False)
        self.source_preview.setPlaceholderText("Paste your Python code here and click Parse Code...")
        self.source_preview.setFocus()
        self.parse_btn.setEnabled(True)

        # Show message
        QMessageBox.information(
            self,
            "Paste Mode",
            "You can now paste your code in the preview area.\nClick 'Parse Code' when ready."
        )

    def parse_code(self):
        """Parse the current code."""
        # Get code from preview
        self.current_code = self.source_preview.toPlainText()

        if not self.current_code.strip():
            QMessageBox.warning(self, "Warning", "Please upload or paste some code first.")
            return

        # Parse the code
        self.parsed_data = self.parser.parse(self.current_code)

        if not self.parsed_data['success']:
            QMessageBox.critical(
                self,
                "Parse Error",
                f"Failed to parse code:\n{self.parsed_data['error']}"
            )
            return

        # Update UI
        self.update_statistics()
        self.update_functions_list()

        # Make source preview read-only again
        self.source_preview.setReadOnly(True)

        QMessageBox.information(self, "Success", "Code parsed successfully!")

    def update_statistics(self):
        """Update parser statistics."""
        if not self.parsed_data:
            return

        accuracy = self.parsed_data['accuracy']
        total = self.parsed_data['total_items']
        with_docs = self.parsed_data['items_with_docstrings']

        self.accuracy_label.setText(f"Accuracy: {accuracy:.1f}%")
        self.coverage_label.setText(
            f"Coverage: {with_docs}/{total} items have docstrings"
        )

    def update_functions_list(self):
        """Update the functions list."""
        self.functions_list.clear()

        if not self.parsed_data:
            return

        # Add functions
        for func in self.parsed_data['functions']:
            status = "✓" if func['has_docstring'] else "✗"
            self.functions_list.addItem(f"{status} Function: {func['name']} (line {func['line']})")

        # Add classes
        for cls in self.parsed_data['classes']:
            status = "✓" if cls['has_docstring'] else "✗"
            self.functions_list.addItem(f"{status} Class: {cls['name']} (line {cls['line']})")

    def show_function_details(self, item):
        """Show details of selected function/class."""
        if not self.parsed_data:
            return

        # Get item text
        text = item.text()

        # Extract name
        parts = text.split(": ")
        if len(parts) < 2:
            return

        name = parts[1].split(" (line")[0]

        # Find the item
        all_items = self.parsed_data['functions'] + self.parsed_data['classes']
        selected_item = None

        for item_data in all_items:
            if item_data['name'] == name:
                selected_item = item_data
                break

        if not selected_item:
            return

        # Display details
        details = f"Name: {selected_item['name']}\n"
        details += f"Line: {selected_item['line']}\n"
        details += f"Has Docstring: {'Yes' if selected_item['has_docstring'] else 'No'}\n\n"

        if 'params' in selected_item:
            details += "Parameters:\n"
            for param in selected_item['params']:
                param_str = f"  - {param['name']}"
                if 'type' in param:
                    param_str += f": {param['type']}"
                details += param_str + "\n"

            if selected_item.get('return_type'):
                details += f"\nReturn Type: {selected_item['return_type']}\n"

        details += "\nSource Code:\n"
        details += "=" * 50 + "\n"
        details += selected_item.get('source', '')

        self.ast_output.setPlainText(details)

    def get_parsed_data(self):
        """Get the parsed data for use in other tabs."""
        return self.parsed_data
