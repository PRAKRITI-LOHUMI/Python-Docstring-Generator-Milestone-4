"""
Docstring Validator using pydocstyle for PEP 257 compliance.
"""

import tempfile
import os
from pydocstyle import check


class DocstringValidator:
    """Validates docstrings against PEP 257 standards."""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.compliant_count = 0
    
    def validate_code(self, source_code, generated_docstrings=None):
        """
        Validate docstrings in Python code against PEP 257.
        
        Args:
            source_code (str): The Python source code
            generated_docstrings (dict): Optional dict of function -> docstring mapping
            
        Returns:
            dict: Validation results with errors, warnings, and compliance stats
        """
        try:
            # If we have generated docstrings, insert them into the code
            if generated_docstrings:
                source_code = self._insert_docstrings(source_code, generated_docstrings)
            
            # Write to temporary file for pydocstyle
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
                f.write(source_code)
                temp_path = f.name
            
            try:
                # Run pydocstyle checks
                issues = list(check([temp_path]))
                
                # Categorize issues
                errors = []
                warnings = []
                
                for issue in issues:
                    issue_dict = {
                        "code": issue.code,
                        "message": issue.message,
                        "line": issue.line,
                        "definition": str(issue.definition) if issue.definition else "Unknown"
                    }
                    
                    # Categorize by severity
                    if issue.code in ['D100', 'D101', 'D102', 'D103']:
                        errors.append(issue_dict)
                    else:
                        warnings.append(issue_dict)
                
                self.errors = errors
                self.warnings = warnings
                
                # Calculate compliance
                total_issues = len(issues)
                total_functions = source_code.count('def ')
                self.compliant_count = max(0, total_functions - len(errors))
                
                return self._format_results()
                
            finally:
                # Clean up temp file
                try:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                except:
                    pass
                    
        except Exception as e:
            # Return error result instead of crashing
            return {
                "errors": [{"code": "ERROR", "message": f"Validation error: {str(e)}", "line": 0, "definition": ""}],
                "warnings": [],
                "compliant": 0,
                "total_issues": 1,
                "summary": {
                    "compliant": 0,
                    "warnings": 0,
                    "errors": 1
                }
            }
    
    def _insert_docstrings(self, source_code, docstrings):
        """Insert generated docstrings into source code."""
        lines = source_code.split('\n')
        result_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            result_lines.append(line)
            
            # Check if this is a function definition
            if line.strip().startswith('def '):
                func_name = line.split('def ')[1].split('(')[0].strip()
                
                # If we have a docstring for this function
                if func_name in docstrings:
                    docstring = docstrings[func_name].get('docstring', '')
                    if docstring:
                        # Add indentation
                        indent = len(line) - len(line.lstrip()) + 4
                        indent_str = ' ' * indent
                        
                        # Add docstring
                        result_lines.append(indent_str + '"""')
                        for doc_line in docstring.split('\n'):
                            result_lines.append(indent_str + doc_line)
                        result_lines.append(indent_str + '"""')
            
            i += 1
        
        return '\n'.join(result_lines)
    
    def _format_results(self):
        """Format validation results."""
        total_issues = len(self.errors) + len(self.warnings)
        
        return {
            "errors": self.errors,
            "warnings": self.warnings,
            "compliant": self.compliant_count,
            "total_issues": total_issues,
            "summary": {
                "compliant": self.compliant_count,
                "warnings": len(self.warnings),
                "errors": len(self.errors)
            }
        }
    
    def get_file_status(self, results):
        """Get detailed file-wise status of validation."""
        status_items = []
        
        # Group issues by type
        issue_types = {}
        for error in results['errors']:
            code = error['code']
            if code not in issue_types:
                issue_types[code] = []
            issue_types[code].append(error)
        
        for warning in results['warnings']:
            code = warning['code']
            if code not in issue_types:
                issue_types[code] = []
            issue_types[code].append(warning)
        
        # Create status messages
        for code, issues in issue_types.items():
            message = self._get_issue_message(code)
            status_items.append({
                "code": code,
                "message": message,
                "count": len(issues),
                "severity": "error" if code in ['D100', 'D101', 'D102', 'D103'] else "warning"
            })
        
        return status_items
    
    def _get_issue_message(self, code):
        """Get human-readable message for error code."""
        messages = {
            'D100': 'Missing docstring in public module',
            'D101': 'Missing docstring in public class',
            'D102': 'Missing docstring in public method',
            'D103': 'Missing docstring in public function',
            'D200': 'One-line docstring should fit on one line',
            'D201': 'No blank lines allowed before function docstring',
            'D202': 'No blank lines allowed after function docstring',
            'D203': 'One blank line required before class docstring',
            'D204': 'One blank line required after class docstring',
            'D205': 'One blank line required between summary and description',
            'D206': 'Docstring should be indented with spaces, not tabs',
            'D207': 'Docstring is under-indented',
            'D208': 'Docstring is over-indented',
            'D209': 'Multi-line docstring closing quotes should be on a separate line',
            'D210': 'No whitespaces allowed surrounding docstring text',
            'D211': 'No blank lines allowed before class docstring',
            'D212': 'Multi-line docstring summary should start at the first line',
            'D213': 'Multi-line docstring summary should start at the second line',
            'D300': 'Use triple double quotes for docstrings',
            'D301': 'Use r""" if any backslashes in a docstring',
            'D400': 'First line should end with a period',
            'D401': 'First line should be in imperative mood',
            'D402': 'First line should not be the function signature',
            'D403': 'First word of the first line should be capitalized',
            'D404': 'First word of the docstring should not be "This"',
            'D405': 'Section name should be properly capitalized',
            'D406': 'Section name should end with a newline',
            'D407': 'Missing dashed underline after section',
            'D408': 'Section underline should be on the line after the section name',
            'D409': 'Section underline should match the length of its name',
            'D410': 'Missing blank line after section',
            'D411': 'Missing blank line before section',
            'D412': 'No blank lines allowed between section header and content',
            'D413': 'Missing blank line after last section',
            'D414': 'Section has no content',
            'D415': 'First line should end with a period, question mark, or exclamation point',
            'D416': 'Section name should end with a colon',
            'D417': 'Missing argument descriptions in the docstring'
        }
        return messages.get(code, f'PEP 257 violation: {code}')