"""Validator tab UI component."""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QLabel, QRadioButton, QButtonGroup,
    QSplitter, QGroupBox, QMessageBox, QFileDialog,
    QProgressBar, QListWidget
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from core import DocstringGenerator, DocstringValidator
from utils.helpers import format_code_with_docstring
import config


class GeneratorThread(QThread):
    """Thread for generating docstrings."""

    progress = pyqtSignal(int, int)
    finished = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, generator, items, style):
        """Initialize the GeneratorThread."""
        super().__init__()
        self.generator = generator
        self.items = items
        self.style = style

    def run(self):
        """Run the generation process."""
        try:
            results = self.generator.generate_batch_docstrings(
                self.items,
                self.style,
                lambda current, total: self.progress.emit(current, total)
            )
            self.finished.emit(results)
        except Exception as e:
            self.error.emit(str(e))


class ValidatorTab(QWidget):
    """Tab for generating and validating docstrings."""

    def __init__(self, parser_tab):
        """Initialize the ValidatorTab."""
        super().__init__()
        self.parser_tab = parser_tab
        self.generator = DocstringGenerator()
        self.validator = DocstringValidator()
        self.current_style = "Google"
        self.generated_results = []
        self.generated_code = ""
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()

        # API Key input
        api_layout = QHBoxLayout()
        api_label = QLabel("Gemini API Key:")
        self.api_key_input = QTextEdit()
        self.api_key_input.setMaximumHeight(60)
        self.api_key_input.setPlaceholderText("Enter your Gemini API key here...")

        api_set_btn = QPushButton("Set API Key")
        api_set_btn.clicked.connect(self.set_api_key)

        api_layout.addWidget(api_label)
        api_layout.addWidget(self.api_key_input, 3)
        api_layout.addWidget(api_set_btn)

        layout.addLayout(api_layout)

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
        """Create the left panel with controls."""
        panel = QWidget()
        layout = QVBoxLayout()

        # Docstring Styles
        style_group = QGroupBox("Docstring Style")
        style_layout = QVBoxLayout()

        self.style_buttons = QButtonGroup()

        for style in config.DOCSTRING_STYLES:
            rb = QRadioButton(style)
            if style == "Google":
                rb.setChecked(True)
            rb.toggled.connect(lambda checked, s=style: self.change_style(s, checked))
            self.style_buttons.addButton(rb)
            style_layout.addWidget(rb)

        self.style_status_label = QLabel("Status: Ready")
        style_layout.addWidget(self.style_status_label)

        style_group.setLayout(style_layout)
        layout.addWidget(style_group)

        # Generate button
        self.generate_btn = QPushButton("Generate Docstrings")
        self.generate_btn.setObjectName("successButton")
        self.generate_btn.clicked.connect(self.generate_docstrings)
        layout.addWidget(self.generate_btn)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Validate button
        self.validate_btn = QPushButton("Validate PEP 257")
        self.validate_btn.clicked.connect(self.validate_docstrings)
        self.validate_btn.setEnabled(False)
        layout.addWidget(self.validate_btn)

        # Validation Status
        validation_group = QGroupBox("Validation Status")
        validation_layout = QVBoxLayout()

        self.compliant_label = QLabel("Compliant: 0")
        self.warnings_label = QLabel("Warnings: 0")
        self.errors_label = QLabel("Errors: 0")

        validation_layout.addWidget(self.compliant_label)
        validation_layout.addWidget(self.warnings_label)
        validation_layout.addWidget(self.errors_label)

        validation_group.setLayout(validation_layout)
        layout.addWidget(validation_group)

        # Download button
        self.download_btn = QPushButton("Download Output")
        self.download_btn.setObjectName("successButton")
        self.download_btn.clicked.connect(self.download_output)
        self.download_btn.setEnabled(False)
        layout.addWidget(self.download_btn)

        layout.addStretch()
        panel.setLayout(layout)
        return panel

    def create_right_panel(self):
        """Create the right panel with output."""
        panel = QWidget()
        layout = QVBoxLayout()

        # Generated Docstrings
        docstring_label = QLabel("Generated Docstrings:")
        docstring_label.setObjectName("subHeaderLabel")
        layout.addWidget(docstring_label)

        self.docstring_output = QTextEdit()
        self.docstring_output.setReadOnly(True)
        self.docstring_output.setPlaceholderText("Generated docstrings will appear here...")
        layout.addWidget(self.docstring_output)

        # Validation Results
        validation_label = QLabel("Validation Results:")
        validation_label.setObjectName("subHeaderLabel")
        layout.addWidget(validation_label)

        self.validation_output = QListWidget()
        layout.addWidget(self.validation_output)

        panel.setLayout(layout)
        return panel

    def set_api_key(self):
        """Set the Gemini API key."""
        api_key = self.api_key_input.toPlainText().strip()

        if not api_key:
            QMessageBox.warning(self, "Warning", "Please enter an API key.")
            return

        self.generator.set_api_key(api_key)
        config.GEMINI_API_KEY = api_key

        QMessageBox.information(self, "Success", "API key set successfully!")
        self.style_status_label.setText("Status: Ready")

    def change_style(self, style, checked):
        """Change the docstring style."""
        if checked:
            self.current_style = style
            self.style_status_label.setText(f"Status: {style} style selected")

    def generate_docstrings(self):
        """Generate docstrings for all functions."""
        # Check API key
        if not config.GEMINI_API_KEY:
            QMessageBox.warning(
                self,
                "API Key Required",
                "Please set your Gemini API key first."
            )
            return

        # Get parsed data
        parsed_data = self.parser_tab.get_parsed_data()

        if not parsed_data or not parsed_data['success']:
            QMessageBox.warning(
                self,
                "No Data",
                "Please parse some code in the Parser tab first."
            )
            return

        # Get all items (functions + classes)
        all_items = parsed_data['functions'] + parsed_data['classes']

        if not all_items:
            QMessageBox.warning(
                self,
                "No Functions",
                "No functions or classes found in the parsed code."
            )
            return

        # Start generation
        self.generate_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(len(all_items))

        # Create and start thread
        self.gen_thread = GeneratorThread(self.generator, all_items, self.current_style)
        self.gen_thread.progress.connect(self.update_progress)
        self.gen_thread.finished.connect(self.generation_finished)
        self.gen_thread.error.connect(self.generation_error)
        self.gen_thread.start()

    def update_progress(self, current, total):
        """Update the progress bar."""
        self.progress_bar.setValue(current)

    def generation_finished(self, results):
        """Handle generation completion."""
        self.generated_results = results
        self.progress_bar.setVisible(False)
        self.generate_btn.setEnabled(True)

        # Display results
        output = f"Generated Docstrings ({self.current_style} style)\n"
        output += "=" * 60 + "\n\n"

        for result in results:
            output += f"Function/Class: {result['name']}\n"
            output += "-" * 60 + "\n"

            if result['has_original']:
                output += "Original Docstring:\n"
                output += result['original_docstring'] + "\n\n"

            output += "Generated Docstring:\n"
            output += result['generated_docstring'] + "\n"
            output += "=" * 60 + "\n\n"

        self.docstring_output.setPlainText(output)

        # Enable validation
        self.validate_btn.setEnabled(True)

        QMessageBox.information(
            self,
            "Success",
            f"Generated {len(results)} docstrings successfully!"
        )

    def generation_error(self, error_msg):
        """Handle generation error."""
        self.progress_bar.setVisible(False)
        self.generate_btn.setEnabled(True)

        QMessageBox.critical(
            self,
            "Generation Error",
            f"Failed to generate docstrings:\n{error_msg}"
        )

    def validate_docstrings(self):
        """Validate the generated docstrings."""
        if not self.generated_results:
            QMessageBox.warning(self, "No Data", "Please generate docstrings first.")
            return

        # Get original code
        parsed_data = self.parser_tab.get_parsed_data()
        original_code = self.parser_tab.current_code

        # Build new code with generated docstrings
        # For simplicity, we'll validate each docstring individually
        self.validation_output.clear()

        total_violations = 0
        all_violations = []

        for result in self.generated_results:
            docstring = result['generated_docstring']
            name = result['name']

            # Validate this docstring
            validation_result = self.validator.validate_docstring(docstring, name)

            if validation_result.get('total_violations', 0) > 0:
                total_violations += validation_result['total_violations']

                for violation in validation_result.get('violations', []):
                    all_violations.append(violation)
                    self.validation_output.addItem(
                        f"❌ {name}: {violation['code']} - {violation['message']}"
                    )
            else:
                self.validation_output.addItem(f"✓ {name}: PEP 257 compliant")

        # Update statistics
        total_items = len(self.generated_results)
        compliant = total_items - len([v for v in all_violations if v])

        self.compliant_label.setText(f"Compliant: {compliant}/{total_items}")
        self.warnings_label.setText("Warnings: 0")
        self.errors_label.setText(f"Errors: {total_violations}")

        # Enable download
        self.download_btn.setEnabled(True)

        if total_violations == 0:
            QMessageBox.information(
                self,
                "Validation Success",
                "All docstrings are PEP 257 compliant!"
            )
        else:
            QMessageBox.warning(
                self,
                "Validation Issues",
                f"Found {total_violations} PEP 257 violations.\nCheck the validation results for details."
            )

    def download_output(self):
        """Download the generated output."""
        if not self.generated_results:
            QMessageBox.warning(self, "No Data", "Please generate docstrings first.")
            return

        # Ask for save location
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Generated Docstrings",
            "generated_docstrings.txt",
            "Text Files (*.txt);;All Files (*)"
        )

        if not file_path:
            return

        try:
            # Write output
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"Generated Docstrings ({self.current_style} style)\n")
                f.write("=" * 60 + "\n\n")

                for result in self.generated_results:
                    f.write(f"Function/Class: {result['name']}\n")
                    f.write("-" * 60 + "\n\n")

                    f.write("Generated Docstring:\n")
                    f.write(result['generated_docstring'] + "\n")
                    f.write("=" * 60 + "\n\n")

            QMessageBox.information(
                self,
                "Success",
                f"Docstrings saved to:\n{file_path}"
            )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to save file:\n{str(e)}"
            )
