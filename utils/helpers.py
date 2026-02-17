"""Helper utilities for the application."""


def format_code_with_docstring(original_code, docstring, indent_level=1):
    """
    Format code with a new docstring.

    Args:
        original_code: Original function/class source code
        docstring: Generated docstring to insert
        indent_level: Indentation level for the docstring

    Returns:
        Formatted code with the docstring
    """
    lines = original_code.split('\n')

    # Find the function/class definition line
    def_line_idx = 0
    for i, line in enumerate(lines):
        if line.strip().startswith('def ') or line.strip().startswith('class '):
            def_line_idx = i
            break

    # Calculate indentation
    indent = '    ' * indent_level

    # Format docstring
    formatted_docstring = f'{indent}"""\n'
    for line in docstring.split('\n'):
        formatted_docstring += f'{indent}{line}\n'
    formatted_docstring += f'{indent}"""'

    # Insert docstring after the definition line
    result_lines = lines[:def_line_idx + 1]
    result_lines.append(formatted_docstring)

    # Add remaining lines (skip old docstring if exists)
    skip_next = False
    for i in range(def_line_idx + 1, len(lines)):
        line = lines[i].strip()

        # Skip existing docstring
        if line.startswith('"""') or line.startswith("'''"):
            if line.count('"""') == 2 or line.count("'''") == 2:
                # Single line docstring
                continue
            else:
                skip_next = True
                continue

        if skip_next:
            if '"""' in line or "'''" in line:
                skip_next = False
            continue

        result_lines.append(lines[i])

    return '\n'.join(result_lines)


def get_severity_color(code):
    """
    Get color for violation severity.

    Args:
        code: Error code from pydocstyle

    Returns:
        Color name for the severity
    """
    # D1xx: Missing docstrings
    if code.startswith('D1'):
        return 'error'

    # D2xx: Whitespace issues
    if code.startswith('D2'):
        return 'warning'

    # D3xx: Quotes issues
    if code.startswith('D3'):
        return 'warning'

    # D4xx: Docstring content issues
    if code.startswith('D4'):
        return 'error'

    return 'error'
