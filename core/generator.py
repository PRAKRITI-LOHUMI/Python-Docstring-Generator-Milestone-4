"""
Docstring Generator using Google's Gemini API.
Generates docstrings in different styles (Google, NumPy, reST).
"""

import google.generativeai as genai
from utils.config import GEMINI_API_KEY, GEMINI_MODEL


class DocstringGenerator:
    """Generates docstrings using Gemini API."""
    
    def __init__(self, api_key=None):
        """Initialize the generator with API key."""
        self.api_key = api_key or GEMINI_API_KEY
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(GEMINI_MODEL)
        else:
            self.model = None
    
    def generate_docstring(self, function_info, style="Google"):
        """
        Generate a docstring for a function.
        
        Args:
            function_info: FunctionInfo object containing function details
            style (str): Docstring style (Google, NumPy, or reST)
            
        Returns:
            dict: Contains 'docstring', 'fixed_code', and 'errors'
        """
        if not self.model:
            return {
                "docstring": "Error: No API key configured",
                "fixed_code": None,
                "errors": ["API key not set"]
            }
        
        # If docstring exists, return it
        if function_info.existing_docstring:
            return {
                "docstring": function_info.existing_docstring,
                "fixed_code": None,
                "errors": [],
                "status": "existing"
            }
        
        # Create prompt for Gemini
        prompt = self._create_prompt(function_info, style)
        
        try:
            response = self.model.generate_content(prompt)
            result = self._parse_response(response.text, function_info)
            result["status"] = "generated"
            return result
        except Exception as e:
            return {
                "docstring": f"Error generating docstring: {str(e)}",
                "fixed_code": None,
                "errors": [str(e)],
                "status": "error"
            }
    
    def _create_prompt(self, function_info, style):
        """Create a prompt for the Gemini API."""
        args_str = ", ".join([f"{arg['name']}: {arg['type']}" for arg in function_info.args])
        
        prompt = f"""Generate a {style} style docstring for this Python function.

Function Name: {function_info.name}
Arguments: {args_str}
Return Type: {function_info.returns}

Function Code:
{function_info.body}

Requirements:
1. Follow {style} style docstring format strictly
2. Include purpose of the function
3. Describe all parameters with their types
4. Describe return type and value
5. Add inline comments for complex logic if needed
6. Follow PEP 257 conventions
7. First line should be a brief summary ending with a period
8. If multi-line, leave a blank line after the summary

Also, if you find any obvious errors in the code (syntax, logic), provide a fixed version.

Respond in this format:
DOCSTRING:
[Your generated docstring here]

FIXED_CODE:
[Fixed code if any errors found, otherwise write "No fixes needed"]

ERRORS_FOUND:
[List any errors you found, otherwise write "None"]
"""
        return prompt
    
    def _parse_response(self, response_text, function_info):
        """Parse the Gemini API response."""
        result = {
            "docstring": "",
            "fixed_code": None,
            "errors": []
        }
        
        try:
            # Split response into sections
            sections = response_text.split("FIXED_CODE:")
            if len(sections) >= 2:
                docstring_part = sections[0].replace("DOCSTRING:", "").strip()
                remaining = sections[1]
                
                errors_split = remaining.split("ERRORS_FOUND:")
                if len(errors_split) >= 2:
                    fixed_code = errors_split[0].strip()
                    errors_found = errors_split[1].strip()
                    
                    # Clean up the docstring
                    docstring_part = self._clean_docstring(docstring_part)
                    result["docstring"] = docstring_part
                    
                    if fixed_code and "No fixes needed" not in fixed_code:
                        result["fixed_code"] = fixed_code
                    if errors_found and "None" not in errors_found:
                        result["errors"] = [errors_found]
                else:
                    result["docstring"] = self._clean_docstring(docstring_part)
            else:
                # Fallback: treat entire response as docstring
                result["docstring"] = self._clean_docstring(response_text.strip())
        except Exception as e:
            # If parsing fails, just use the raw response
            result["docstring"] = self._clean_docstring(response_text.strip())
        
        return result
    
    def _clean_docstring(self, docstring_text):
        """
        Clean up the docstring text by removing code fences and extra quotes.
        
        Args:
            docstring_text (str): Raw docstring text from API
            
        Returns:
            str: Cleaned docstring text
        """
        # Remove markdown code fences
        docstring_text = docstring_text.replace("```python", "")
        docstring_text = docstring_text.replace("```", "")
        
        # Remove multiple triple quotes at start/end
        docstring_text = docstring_text.strip()
        
        # Remove leading/trailing triple quotes if present
        if docstring_text.startswith('"""'):
            docstring_text = docstring_text[3:]
        if docstring_text.endswith('"""'):
            docstring_text = docstring_text[:-3]
        
        if docstring_text.startswith("'''"):
            docstring_text = docstring_text[3:]
        if docstring_text.endswith("'''"):
            docstring_text = docstring_text[:-3]
        
        # Clean up extra whitespace
        docstring_text = docstring_text.strip()
        
        return docstring_text
    
    def generate_batch(self, functions, style="Google", progress_callback=None):
        """
        Generate docstrings for multiple functions.
        
        Args:
            functions (list): List of FunctionInfo objects
            style (str): Docstring style
            progress_callback (callable): Optional callback for progress updates
            
        Returns:
            dict: Mapping of function names to generated docstrings
        """
        results = {}
        total = len(functions)
        
        for i, func in enumerate(functions):
            result = self.generate_docstring(func, style)
            results[func.name] = result
            
            if progress_callback:
                progress_callback(i + 1, total)
        
        return results