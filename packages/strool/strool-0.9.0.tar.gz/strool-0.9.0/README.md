# strool

It's a lot like strings, but with boolean controls. They could display
the text or not, depending on the parameters. The recommended way to
import is "import strool as stl".

Inside the module there's available (check each one for more details):
- String_bool (alias: b and s_b): it will give text if "case" is True.
- String_case (alias: c and s_c): it will give text if "case" matches a
case in "case_list".
- whoosh: returns an invisible version of the string provided.
- CONSTANTS (BOOL, INT, STR, STL, ALL, F_STR, F_STL, F_ALL): constants
to use in the "return_type" parameter, of the .print() method of
String_bool and String_case. More details in `help(stl.b.print)`

## Installation

From your console write `pip install strool`

### Contact

Carlos González

carlos.a.gb95@gmail.com
