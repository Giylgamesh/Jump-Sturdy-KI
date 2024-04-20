# Python Code Documentation Guide

This document serves as a quick reference for writing documentation in Python projects.

### 3 Documentation Approaches:
- Docstrings:
<br>&#160;&#160;&#160;&#160;Docstrings are multi-line strings placed **within the code** to document functions, classes, and modules.
<br>&#160;&#160;&#160;&#160;Python recognizes these docstrings automatically and allows you to access them using the __doc__ attribute.
<br>&#160;&#160;&#160;&#160;Docstrings in Python typically follow the PEP 257 standard.

- Comments:
<br>&#160;&#160;&#160;&#160;Brief comments can be used to **explain specific sections of code** or complex logic.
<br>&#160;&#160;&#160;&#160;While not a replacement for docstrings, comments can provide additional context when needed.

- Readme Files:
<br>&#160;&#160;&#160;&#160;A README file provides an overview of the project, installation instructions, usage examples, and guidelines.

### Docstring Examples:

    def add_numbers(a, b):
      """
      Adds two numbers together.
  
      Args:
          a (int): The first number.
          b (int): The second number.
  
      Returns:
          int: The sum of the two numbers.
      """
      return a + b
.

    def function (param1, param2):
      """
      Short description of the function/class/module. 
    
      Args:
          param1 (type): Description of the first parameter.
          param2 (type): Description of the second parameter.
    
      Returns:
          type: Description of the return value.
      
      Raises:
          ExceptionType: Description of exceptions that might be raised.
      """

### Further Resources:
<br>&#160;&#160;&#160;&#160;PEP 257 Docstring Standard: https://peps.python.org/pep-0257/
<br>&#160;&#160;&#160;&#160;Sphinx Documentation Tool: https://sphinx-rtd-theme.readthedocs.io/
