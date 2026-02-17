"""
Source Code Parser using Python's AST module.
Extracts functions and their metadata from Python source code.
"""

import ast
import inspect


class FunctionInfo:
    """Stores information about a parsed function."""
    
    def __init__(self, name, args, returns, lineno, existing_docstring, body):
        self.name = name
        self.args = args
        self.returns = returns
        self.lineno = lineno
        self.existing_docstring = existing_docstring
        self.body = body


class CodeParser:
    """Parses Python source code to extract function information."""
    
    def __init__(self):
        self.functions = []
        self.errors = []
        self.accuracy = 0.0
    
    def parse_code(self, source_code):
        """
        Parse Python source code and extract function information.
        
        Args:
            source_code (str): The Python source code to parse
            
        Returns:
            list: List of FunctionInfo objects
        """
        self.functions = []
        self.errors = []
        
        try:
            tree = ast.parse(source_code)
            self._extract_functions(tree, source_code)
            self.accuracy = 100.0 if not self.errors else 95.0
            return self.functions
        except SyntaxError as e:
            self.errors.append(f"Syntax Error: {str(e)}")
            self.accuracy = 0.0
            return []
        except Exception as e:
            self.errors.append(f"Parse Error: {str(e)}")
            self.accuracy = 0.0
            return []
    
    def _extract_functions(self, tree, source_code):
        """Extract all function definitions from AST."""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_info = self._get_function_info(node, source_code)
                self.functions.append(func_info)
    
    def _get_function_info(self, node, source_code):
        """Extract detailed information from a function node."""
        # Get function name
        name = node.name
        
        # Get arguments
        args = []
        for arg in node.args.args:
            arg_name = arg.arg
            arg_type = self._get_annotation(arg.annotation)
            args.append({"name": arg_name, "type": arg_type})
        
        # Get return type
        returns = self._get_annotation(node.returns)
        
        # Get existing docstring
        existing_docstring = ast.get_docstring(node)
        
        # Get function body (for inline comments)
        body = self._get_function_body(node, source_code)
        
        return FunctionInfo(
            name=name,
            args=args,
            returns=returns,
            lineno=node.lineno,
            existing_docstring=existing_docstring,
            body=body
        )
    
    def _get_annotation(self, annotation):
        """Get type annotation as string."""
        if annotation is None:
            return None
        try:
            return ast.unparse(annotation)
        except:
            return str(annotation)
    
    def _get_function_body(self, node, source_code):
        """Extract the function body as text."""
        try:
            lines = source_code.split('\n')
            start_line = node.lineno - 1
            
            # Find the end of the function
            end_line = start_line + 1
            if node.body:
                last_stmt = node.body[-1]
                end_line = last_stmt.end_lineno if hasattr(last_stmt, 'end_lineno') else start_line + 10
            
            body_lines = lines[start_line:end_line]
            return '\n'.join(body_lines)
        except:
            return ""
    
    def get_coverage_stats(self):
        """Calculate coverage statistics."""
        total = len(self.functions)
        if total == 0:
            return {"total": 0, "with_docstring": 0, "without_docstring": 0, "percentage": 0.0}
        
        with_docstring = sum(1 for f in self.functions if f.existing_docstring)
        without_docstring = total - with_docstring
        percentage = (with_docstring / total) * 100
        
        return {
            "total": total,
            "with_docstring": with_docstring,
            "without_docstring": without_docstring,
            "percentage": percentage
        }
