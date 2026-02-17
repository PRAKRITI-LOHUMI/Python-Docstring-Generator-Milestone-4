"""
Main Window for Docstring Generator Application.
Provides UI for parsing, generating, and validating docstrings.
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QPushButton, QLabel, QTextEdit, QListWidget, QGroupBox,
    QRadioButton, QFileDialog, QMessageBox, QProgressBar,
    QSplitter, QPlainTextEdit, QListWidgetItem
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import sys

from core.parser import CodeParser
from core.generator import DocstringGenerator
from core.validator import DocstringValidator
from utils.config import WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT
from ui.styles import (
    MAIN_STYLE, HEADER_STYLE, SUBHEADER_STYLE, INFO_LABEL_STYLE,
    SUCCESS_STYLE, WARNING_STYLE, ERROR_STYLE, CODE_EDITOR_STYLE
)


class GeneratorThread(QThread):
    """Thread for generating docstrings asynchronously."""
    
    progress = pyqtSignal(int, int)
    finished = pyqtSignal(dict)
    
    def __init__(self, generator, functions, style):
        super().__init__()
        self.generator = generator
        self.functions = functions
        self.style = style
    
    def run(self):
        """Run the generation process."""
        results = self.generator.generate_batch(
            self.functions,
            self.style,
            lambda current, total: self.progress.emit(current, total)
        )
        self.finished.emit(results)


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Initialize components
        self.parser = CodeParser()
        self.generator = None
        self.validator = DocstringValidator()
        
        # Data storage
        self.source_code = ""
        self.parsed_functions = []
        self.generated_docstrings = {}
        self.validation_results = {}
        
        # Setup UI
        self.init_ui()
        self.setStyleSheet(MAIN_STYLE)
    
    def init_ui(self):
        """Initialize the user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Header
        header = QLabel("Python Docstring Generator")
        header.setStyleSheet(HEADER_STYLE)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # API Key input
        api_layout = QHBoxLayout()
        api_label = QLabel("Gemini API Key:")
        self.api_key_input = QTextEdit()
        self.api_key_input.setMaximumHeight(40)
        self.api_key_input.setPlaceholderText("Enter your Gemini API key here...")
        api_button = QPushButton("Set API Key")
        api_button.clicked.connect(self.set_api_key)
        
        api_layout.addWidget(api_label)
        api_layout.addWidget(self.api_key_input)
        api_layout.addWidget(api_button)
        layout.addLayout(api_layout)
        
        # Tab Widget
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_parser_tab(), "Parser and Baseline")
        self.tabs.addTab(self.create_synthesis_tab(), "Synthesis and Validation")
        
        layout.addWidget(self.tabs)
    
    def create_parser_tab(self):
        """Create the parser and baseline generation tab."""
        tab = QWidget()
        layout = QHBoxLayout(tab)
        
        # Left Panel
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_panel.setMaximumWidth(350)
        
        # File Upload Section
        file_group = QGroupBox("Source Code Input")
        file_layout = QVBoxLayout()
        
        upload_btn = QPushButton("Upload Python File")
        upload_btn.clicked.connect(self.upload_file)
        file_layout.addWidget(upload_btn)
        
        paste_btn = QPushButton("Paste Code")
        paste_btn.clicked.connect(self.paste_code)
        file_layout.addWidget(paste_btn)
        
        parse_btn = QPushButton("Parse Code")
        parse_btn.clicked.connect(self.parse_code)
        file_layout.addWidget(parse_btn)
        
        file_group.setLayout(file_layout)
        left_layout.addWidget(file_group)
        
        # Parser Accuracy
        accuracy_group = QGroupBox("Parser Accuracy")
        accuracy_layout = QVBoxLayout()
        
        self.accuracy_label = QLabel("Accuracy: 0%")
        self.accuracy_label.setStyleSheet(INFO_LABEL_STYLE)
        accuracy_layout.addWidget(self.accuracy_label)
        
        self.accuracy_bar = QProgressBar()
        self.accuracy_bar.setValue(0)
        accuracy_layout.addWidget(self.accuracy_bar)
        
        accuracy_group.setLayout(accuracy_layout)
        left_layout.addWidget(accuracy_group)
        
        # Functions List
        functions_group = QGroupBox("Detected Functions")
        functions_layout = QVBoxLayout()
        
        self.functions_list = QListWidget()
        self.functions_list.itemClicked.connect(self.show_function_details)
        functions_layout.addWidget(self.functions_list)
        
        functions_group.setLayout(functions_layout)
        left_layout.addWidget(functions_group)
        
        # Coverage Report
        coverage_group = QGroupBox("Coverage Report")
        coverage_layout = QVBoxLayout()
        
        self.coverage_label = QLabel("Total Functions: 0\nWith Docstring: 0\nWithout Docstring: 0")
        self.coverage_label.setStyleSheet(INFO_LABEL_STYLE)
        coverage_layout.addWidget(self.coverage_label)
        
        coverage_group.setLayout(coverage_layout)
        left_layout.addWidget(coverage_group)
        
        left_layout.addStretch()
        
        # Main Panel with vertical splitter
        main_panel = QWidget()
        main_layout = QVBoxLayout(main_panel)
        
        # Create vertical splitter for resizable sections
        main_splitter = QSplitter(Qt.Vertical)
        
        # Source Code Preview Section
        preview_widget = QWidget()
        preview_layout = QVBoxLayout(preview_widget)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        
        preview_label = QLabel("Source Code Preview")
        preview_label.setStyleSheet(SUBHEADER_STYLE)
        preview_layout.addWidget(preview_label)
        
        self.code_preview = QPlainTextEdit()
        self.code_preview.setReadOnly(True)
        self.code_preview.setStyleSheet(CODE_EDITOR_STYLE)
        preview_layout.addWidget(self.code_preview)
        
        main_splitter.addWidget(preview_widget)
        
        # AST Parsing Output Section
        ast_widget = QWidget()
        ast_layout = QVBoxLayout(ast_widget)
        ast_layout.setContentsMargins(0, 0, 0, 0)
        
        ast_label = QLabel("AST Parsing Output")
        ast_label.setStyleSheet(SUBHEADER_STYLE)
        ast_layout.addWidget(ast_label)
        
        self.ast_output = QTextEdit()
        self.ast_output.setReadOnly(True)
        ast_layout.addWidget(self.ast_output)
        
        main_splitter.addWidget(ast_widget)
        
        # Set initial sizes (60% preview, 40% AST output)
        main_splitter.setSizes([400, 300])
        
        main_layout.addWidget(main_splitter)
        
        # Add panels to horizontal splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(main_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        
        main_tab_layout = QVBoxLayout()
        main_tab_layout.addWidget(splitter)
        
        tab_widget = QWidget()
        tab_widget.setLayout(main_tab_layout)
        return tab_widget
    
    def create_synthesis_tab(self):
        """Create the synthesis and validation tab."""
        tab = QWidget()
        layout = QHBoxLayout(tab)
        
        # Left Panel
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_panel.setMaximumWidth(350)
        
        # Docstring Style Selection
        style_group = QGroupBox("Docstring Style")
        style_layout = QVBoxLayout()
        
        self.style_google = QRadioButton("Google Style")
        self.style_numpy = QRadioButton("NumPy Style")
        self.style_rest = QRadioButton("reST Style")
        self.style_google.setChecked(True)
        
        style_layout.addWidget(self.style_google)
        style_layout.addWidget(self.style_numpy)
        style_layout.addWidget(self.style_rest)
        
        generate_btn = QPushButton("Generate Docstrings")
        generate_btn.clicked.connect(self.generate_docstrings)
        style_layout.addWidget(generate_btn)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        style_layout.addWidget(self.progress_bar)
        
        style_group.setLayout(style_layout)
        left_layout.addWidget(style_group)
        
        # Validation Controls
        validation_group = QGroupBox("Validation")
        validation_layout = QVBoxLayout()
        
        validate_btn = QPushButton("Validate PEP 257")
        validate_btn.clicked.connect(self.validate_docstrings)
        validation_layout.addWidget(validate_btn)
        
        validation_group.setLayout(validation_layout)
        left_layout.addWidget(validation_group)
        
        # Status Summary
        status_group = QGroupBox("Status Summary")
        status_layout = QVBoxLayout()
        
        self.status_compliant = QLabel("✓ Compliant: 0")
        self.status_compliant.setStyleSheet(SUCCESS_STYLE)
        status_layout.addWidget(self.status_compliant)
        
        self.status_warnings = QLabel("⚠ Warnings: 0")
        self.status_warnings.setStyleSheet(WARNING_STYLE)
        status_layout.addWidget(self.status_warnings)
        
        self.status_errors = QLabel("✗ Errors: 0")
        self.status_errors.setStyleSheet(ERROR_STYLE)
        status_layout.addWidget(self.status_errors)
        
        status_group.setLayout(status_layout)
        left_layout.addWidget(status_group)
        
        # Download Button
        download_btn = QPushButton("Download Output")
        download_btn.clicked.connect(self.download_output)
        left_layout.addWidget(download_btn)
        
        left_layout.addStretch()
        
        # Main Panel with vertical splitter for resizable sections
        main_panel = QWidget()
        main_layout = QVBoxLayout(main_panel)
        
        # Create vertical splitter for resizable sections
        main_splitter = QSplitter(Qt.Vertical)
        
        # Section 1: Generated Docstrings
        docstring_widget = QWidget()
        docstring_layout = QVBoxLayout(docstring_widget)
        docstring_layout.setContentsMargins(0, 0, 0, 0)
        
        docstring_label = QLabel("Generated Docstrings")
        docstring_label.setStyleSheet(SUBHEADER_STYLE)
        docstring_layout.addWidget(docstring_label)
        
        self.docstring_output = QTextEdit()
        self.docstring_output.setReadOnly(True)
        docstring_layout.addWidget(self.docstring_output)
        
        main_splitter.addWidget(docstring_widget)
        
        # Section 2: Code Fix Suggestions
        fixes_widget = QWidget()
        fixes_layout = QVBoxLayout(fixes_widget)
        fixes_layout.setContentsMargins(0, 0, 0, 0)
        
        fixes_label = QLabel("Suggested Code Fixes")
        fixes_label.setStyleSheet(SUBHEADER_STYLE)
        fixes_layout.addWidget(fixes_label)
        
        self.fixes_output = QTextEdit()
        self.fixes_output.setReadOnly(True)
        self.fixes_output.setPlaceholderText("Code fix suggestions will appear here after generation...")
        fixes_layout.addWidget(self.fixes_output)
        
        main_splitter.addWidget(fixes_widget)
        
        # Section 3: Validation Results
        validation_widget = QWidget()
        validation_layout = QVBoxLayout(validation_widget)
        validation_layout.setContentsMargins(0, 0, 0, 0)
        
        validation_label = QLabel("Validation Results")
        validation_label.setStyleSheet(SUBHEADER_STYLE)
        validation_layout.addWidget(validation_label)
        
        # Chart
        self.chart_widget = QWidget()
        chart_layout = QVBoxLayout(self.chart_widget)
        chart_layout.setContentsMargins(0, 0, 0, 0)
        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvasQTAgg(self.figure)
        chart_layout.addWidget(self.canvas)
        validation_layout.addWidget(self.chart_widget)
        
        # Detailed validation report
        validation_report_label = QLabel("Detailed Report:")
        validation_report_label.setStyleSheet(INFO_LABEL_STYLE)
        validation_layout.addWidget(validation_report_label)
        
        self.validation_output = QTextEdit()
        self.validation_output.setReadOnly(True)
        self.validation_output.setPlaceholderText("Validation details will appear here after validation...")
        validation_layout.addWidget(self.validation_output)
        
        main_splitter.addWidget(validation_widget)
        
        # Set initial sizes for splitter (equal distribution)
        main_splitter.setSizes([300, 200, 300])
        
        main_layout.addWidget(main_splitter)
        
        # Add panels to horizontal splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(main_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        
        main_tab_layout = QVBoxLayout()
        main_tab_layout.addWidget(splitter)
        
        tab_widget = QWidget()
        tab_widget.setLayout(main_tab_layout)
        return tab_widget
    
    def set_api_key(self):
        """Set the Gemini API key."""
        api_key = self.api_key_input.toPlainText().strip()
        if api_key:
            self.generator = DocstringGenerator(api_key)
            QMessageBox.information(self, "Success", "API Key set successfully!")
        else:
            QMessageBox.warning(self, "Warning", "Please enter a valid API key.")
    
    def upload_file(self):
        """Upload a Python file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Python File", "", "Python Files (*.py)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.source_code = f.read()
                self.code_preview.setPlainText(self.source_code)
                QMessageBox.information(self, "Success", "File loaded successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load file: {str(e)}")
    
    def paste_code(self):
        """Open dialog to paste code."""
        from PyQt5.QtWidgets import QDialog
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Paste Python Code")
        dialog.setGeometry(200, 200, 600, 400)
        
        layout = QVBoxLayout(dialog)
        
        text_edit = QTextEdit()
        text_edit.setPlaceholderText("Paste your Python code here...")
        layout.addWidget(text_edit)
        
        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(dialog.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(dialog.reject)
        
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
        if dialog.exec_() == QDialog.Accepted:
            self.source_code = text_edit.toPlainText()
            self.code_preview.setPlainText(self.source_code)
            QMessageBox.information(self, "Success", "Code pasted successfully!")
    
    def parse_code(self):
        """Parse the source code."""
        if not self.source_code:
            QMessageBox.warning(self, "Warning", "Please load or paste source code first.")
            return
        
        self.parsed_functions = self.parser.parse_code(self.source_code)
        
        # Update accuracy
        self.accuracy_label.setText(f"Accuracy: {self.parser.accuracy:.1f}%")
        self.accuracy_bar.setValue(int(self.parser.accuracy))
        
        # Update functions list
        self.functions_list.clear()
        for func in self.parsed_functions:
            status = "✓" if func.existing_docstring else "✗"
            item = QListWidgetItem(f"{status} {func.name}()")
            self.functions_list.addItem(item)
        
        # Update coverage
        coverage = self.parser.get_coverage_stats()
        self.coverage_label.setText(
            f"Total Functions: {coverage['total']}\n"
            f"With Docstring: {coverage['with_docstring']}\n"
            f"Without Docstring: {coverage['without_docstring']}"
        )
        
        # Update AST output
        ast_text = "AST Parsing Results:\n\n"
        for func in self.parsed_functions:
            ast_text += f"Function: {func.name}\n"
            ast_text += f"  Line: {func.lineno}\n"
            ast_text += f"  Arguments: {', '.join([arg['name'] for arg in func.args])}\n"
            ast_text += f"  Returns: {func.returns or 'None'}\n"
            ast_text += f"  Has Docstring: {'Yes' if func.existing_docstring else 'No'}\n\n"
        
        self.ast_output.setText(ast_text)
        
        if self.parser.errors:
            QMessageBox.warning(
                self, "Parse Warnings",
                f"Parsing completed with warnings:\n" + "\n".join(self.parser.errors)
            )
        else:
            QMessageBox.information(self, "Success", f"Parsed {len(self.parsed_functions)} functions!")
    
    def show_function_details(self, item):
        """Show details of selected function."""
        func_name = item.text().split()[-1].replace("()", "")
        
        for func in self.parsed_functions:
            if func.name == func_name:
                details = f"Function: {func.name}\n\n"
                details += f"Arguments:\n"
                for arg in func.args:
                    details += f"  - {arg['name']}: {arg['type'] or 'Any'}\n"
                details += f"\nReturns: {func.returns or 'None'}\n\n"
                
                if func.existing_docstring:
                    details += f"Existing Docstring:\n{func.existing_docstring}\n\n"
                else:
                    details += "No existing docstring.\n\n"
                
                details += f"Function Body:\n{func.body}"
                
                self.ast_output.setText(details)
                break
    
    def generate_docstrings(self):
        """Generate docstrings for all functions."""
        if not self.generator:
            QMessageBox.warning(
                self, "Warning",
                "Please set your Gemini API key first."
            )
            return
        
        if not self.parsed_functions:
            QMessageBox.warning(
                self, "Warning",
                "Please parse source code first."
            )
            return
        
        # Get selected style
        if self.style_google.isChecked():
            style = "Google"
        elif self.style_numpy.isChecked():
            style = "NumPy"
        else:
            style = "reST"
        
        # Start generation in thread
        self.progress_bar.setValue(0)
        self.thread = GeneratorThread(self.generator, self.parsed_functions, style)
        self.thread.progress.connect(self.update_progress)
        self.thread.finished.connect(self.generation_finished)
        self.thread.start()
    
    def update_progress(self, current, total):
        """Update progress bar."""
        progress = int((current / total) * 100)
        self.progress_bar.setValue(progress)
    
    def generation_finished(self, results):
        """Handle generation completion."""
        self.generated_docstrings = results
        
        # Display docstrings
        docstring_text = "Generated Docstrings:\n\n"
        docstring_text += "=" * 80 + "\n\n"
        
        # Display code fixes separately
        fixes_text = "Suggested Code Fixes:\n\n"
        fixes_text += "=" * 80 + "\n\n"
        has_fixes = False
        
        for func_name, result in results.items():
            # Add to docstrings output
            docstring_text += f"Function: {func_name}\n"
            docstring_text += "-" * 80 + "\n"
            docstring_text += f"Status: {result.get('status', 'unknown').upper()}\n\n"
            docstring_text += result['docstring'] + "\n"
            docstring_text += "\n" + "=" * 80 + "\n\n"
            
            # Add to fixes output if there are fixes or errors
            if result.get('fixed_code') or result.get('errors'):
                has_fixes = True
                fixes_text += f"Function: {func_name}\n"
                fixes_text += "-" * 80 + "\n"
                
                if result.get('errors'):
                    fixes_text += f"⚠ Issues Found:\n"
                    for error in result['errors']:
                        fixes_text += f"  • {error}\n"
                    fixes_text += "\n"
                
                if result.get('fixed_code'):
                    fixes_text += f"Suggested Fixed Code:\n"
                    fixes_text += f"{result['fixed_code']}\n"
                
                fixes_text += "\n" + "=" * 80 + "\n\n"
        
        # Update outputs
        self.docstring_output.setText(docstring_text)
        
        if has_fixes:
            self.fixes_output.setText(fixes_text)
        else:
            self.fixes_output.setText("No code issues detected! All functions are syntactically correct.")
        
        QMessageBox.information(self, "Success", "Docstrings generated successfully!")

    
    def validate_docstrings(self):
        """Validate generated docstrings against PEP 257."""
        if not self.generated_docstrings:
            QMessageBox.warning(
                self, "Warning",
                "Please generate docstrings first."
            )
            return
        
        try:
            # Prepare docstrings dict for validation
            docstrings_dict = {}
            for func_name, result in self.generated_docstrings.items():
                docstrings_dict[func_name] = result
            
            # Validate
            self.validation_results = self.validator.validate_code(
                self.source_code,
                docstrings_dict
            )
            
            # Update status summary
            summary = self.validation_results['summary']
            self.status_compliant.setText(f"✓ Compliant: {summary['compliant']}")
            self.status_warnings.setText(f"⚠ Warnings: {summary['warnings']}")
            self.status_errors.setText(f"✗ Errors: {summary['errors']}")
            
            # Update chart
            self.update_validation_chart(summary)
            
            # Update detailed validation report
            status_items = self.validator.get_file_status(self.validation_results)
            validation_text = "PEP 257 Validation Details:\n\n"
            
            if not status_items:
                validation_text += "🎉 Excellent! All docstrings follow PEP 257 standards!\n\n"
                validation_text += "Your generated docstrings are fully compliant with Python's\n"
                validation_text += "documentation standards. No issues detected.\n"
            else:
                validation_text += f"Total Issues Found: {len(status_items)}\n\n"
                
                # Group by severity
                errors_list = [item for item in status_items if item['severity'] == 'error']
                warnings_list = [item for item in status_items if item['severity'] == 'warning']
                
                if errors_list:
                    validation_text += "❌ ERRORS (Must Fix):\n"
                    validation_text += "-" * 60 + "\n"
                    for item in errors_list:
                        validation_text += f"  • {item['code']}: {item['message']}\n"
                        validation_text += f"    Occurrences: {item['count']}\n\n"
                
                if warnings_list:
                    validation_text += "\n⚠ WARNINGS (Should Fix):\n"
                    validation_text += "-" * 60 + "\n"
                    for item in warnings_list:
                        validation_text += f"  • {item['code']}: {item['message']}\n"
                        validation_text += f"    Occurrences: {item['count']}\n\n"
            
            self.validation_output.setText(validation_text)
            
            QMessageBox.information(self, "Validation Complete", 
                                  f"PEP 257 validation completed!\n\n"
                                  f"Compliant: {summary['compliant']}\n"
                                  f"Warnings: {summary['warnings']}\n"
                                  f"Errors: {summary['errors']}")
        
        except Exception as e:
            QMessageBox.critical(
                self, "Validation Error",
                f"An error occurred during validation:\n\n{str(e)}\n\n"
                "Please check your generated docstrings and try again."
            )
    
    def update_validation_chart(self, summary):
        """Update the validation results chart."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        categories = ['Compliant', 'Warnings', 'Errors']
        values = [summary['compliant'], summary['warnings'], summary['errors']]
        colors = ['#4CAF50', '#FF9800', '#F44336']
        
        ax.bar(categories, values, color=colors)
        ax.set_ylabel('Count')
        ax.set_title('PEP 257 Validation Results')
        ax.grid(axis='y', alpha=0.3)
        
        self.canvas.draw()
    
    def download_output(self):
        """Download the generated docstrings and code."""
        if not self.generated_docstrings:
            QMessageBox.warning(
                self, "Warning",
                "Please generate docstrings first."
            )
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Output", "output_with_docstrings.py", "Python Files (*.py)"
        )
        
        if file_path:
            try:
                # Insert docstrings into source code
                output_code = self._insert_docstrings_into_code()
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(output_code)
                
                QMessageBox.information(self, "Success", "Output saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")
    
    def _insert_docstrings_into_code(self):
        """Insert generated docstrings into the source code."""
        lines = self.source_code.split('\n')
        result_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            result_lines.append(line)
            
            # Check if this is a function definition
            if line.strip().startswith('def '):
                func_name = line.split('def ')[1].split('(')[0].strip()
                
                # If we have a generated docstring for this function
                if func_name in self.generated_docstrings:
                    result = self.generated_docstrings[func_name]
                    docstring = result.get('docstring', '')
                    
                    if docstring and result.get('status') == 'generated':
                        # Add indentation
                        indent = len(line) - len(line.lstrip()) + 4
                        indent_str = ' ' * indent
                        
                        # Skip existing docstring if any
                        j = i + 1
                        while j < len(lines) and not lines[j].strip():
                            j += 1
                        if j < len(lines) and (lines[j].strip().startswith('"""') or lines[j].strip().startswith("'''")):
                            # Skip old docstring
                            while j < len(lines):
                                if '"""' in lines[j] or "'''" in lines[j]:
                                    if j > i + 1:
                                        i = j
                                        break
                                j += 1
                        
                        # Add new docstring
                        result_lines.append(indent_str + '"""')
                        for doc_line in docstring.split('\n'):
                            result_lines.append(indent_str + doc_line)
                        result_lines.append(indent_str + '"""')
            
            i += 1
        
        return '\n'.join(result_lines)