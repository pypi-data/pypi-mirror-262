"""strool - Fusion between str and bool
    
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
String_bool and String_case. More details in `help(stl.b.print)`"""

from __future__ import annotations
from typing import Iterable as _Iterable
from typing import Any as _Any
from typing import Literal as _Literal
from typing import IO as _IO
from collections import UserString as _UserString
from re import sub as _sub

BOOL = 0
INT = 1
STR = 2
STL = 3
ALL = 32
F_STR = 33
F_STL = 34
F_ALL = 35

def whoosh(string : str) -> str:
    """WHOOOOOSH!! NOW YOUR STRING IS INVISIBLE!!!!
    
    (It substitutes visible characters with invisible ones)"""
    return _sub(r'(?!\s).', ' ', string)

class String_bool(_UserString):
    """String_bool - A string, but it will show text or not, depending on the
    boolean value of "case".

    Parameters:
    - string: actual text stored, it will be shown if "case" is True.
    - case: boolean that will determine if the object outputs text.
    - negated: if true, text will be shown when "case" is False.
    - invisible_ink: if true, when text must be hidden, it'll be substituted
    with invisible characters (useful when your program's structure is
    partly or completely determined by text, specially console programs).

    Except for "string", all parameters are saved inside the object with the
    name of the parameter (e.g.: "case" is saved in "object.case"). The
    parameter "string" is saved in "object.data".
    
    Methods:
    - check: returns True if text will be shown, otherwise False.
    - reset_count: sets the counter of how many times the text has been
    shown to 0.
    - print: prints the text if "check" returns True, otherwise it'll not
    print anything, unless "invisible_ink" is True, then it'll print
    invisible text. To keep track of what has been printed, you can set
    "return_type" to BOOL, INT, STR, STL, to get True or False, how many
    times it has been shown, the string shown or the strool object,
    respectively. You can give return types in a list, and it will return
    them in the order you provided, unless you give the return type ALL. ALL
    will provide BOOL, INT, STR and STL (means strool) in that order.
    - modify: an easy way to modify the object's parameters. Specially
    useful when you convert between strool types. It modifies the object and
    returns it, so you can use it when you save the object into a variable
    or when it is already given a variable name.

    To convert between strool types, simply give the old strool object to
    the new strool constructor. e.g.:
    `new_object = stl.String_case(string_bool_object))`.
    It'll ignore any parameters and save all data from the object. If you
    convert from String_case to String_bool, it'll keep the data from
    case_list and case_sensitive, to be able to use it again if you turn it
    into a String_case again."""

    __slots__ = ['data', 'case', 'negated', 'invisible_ink', 'recount', '_last_try', 'case_list', 'case_sensitive']

    def __init__(self, string : str | s_b | s_c , case : bool = True, *, negated: bool = False, invisible_ink : bool = False) -> None:

        try:
            super().__init__(string.data)
            self.case = string.case
            self.negated = string.negated
            self.invisible_ink = string.invisible_ink
            self.recount = string.recount
            self._last_try = string._last_try

            try:
                self.case_list = string.case_list
                self.case_sensitive = string.case_sensitive
            except: pass

        except:
            super().__init__(string)
            self.case = case
            self.negated = negated
            self.invisible_ink = invisible_ink
            self.recount = 0
            self._last_try = False
       
    def check(self):
        """It will return True if text would be shown (visibly), otherwise False"""
        if self.negated: return not self.case
        else: return self.case

    def _give(self):
        self.recount += 1
        self._last_try = True
        return self.data
    
    def reset_count(self):
        """Sets the counter of how many times text has been shown, to zero"""
        self.recount = 0

    def __str__(self):
        self._last_try = False
        match [self.check(), self.invisible_ink]:
            case [True, _] : return self._give()
            case [False, False] : return ''
            case [False, True] : return whoosh(self.data)
    
    def print(self, *, end: str | None = "\n", return_type : int | _Iterable = [], file: _IO[str] | None = None, flush: _Literal[False] = False):
        """The method responsible for printing, it can do pretty much the same as
        regular "print(strool_object)", but it can be simpler to read by humans,
        specially when you don't want/have to save the text in a variable.
        You can also set a return_type to have a record of what has been printed.

        The possible values for "return_type" are:
        - BOOL: will return True or False, depending if the text has been shown.
        - INT: will return the total amount of times the text has been shown.
        - STR: will return the actual string shown, if it was shown, otherwise
        it'll return an empty string.
        - STL: will return the actual strool shown, if it was shown, otherwise
        it'll return "None".
        - F_STR: force string, it will return the string stored, always.
        - F_STL: force strool, it will return the strool object, always.
        - ALL: will return a list with BOOL, INT, STR and STL, in that order.
        - F_ALL: will return a list with BOOL, INT, F_STR and F_STL, in that
        order.

        For multiple selection, you can make it an Iterable, and it will return
        a list with all the returns in the order they were written. For example:
        `object.print(return_type = (stl.STR, stl.BOOL))` will return str and
        bool, in that order."""
        def _append_to_return_list(self, item):
            match (item, self._last_try, self.invisible_ink):
                case (0, x, y) : return_list.append(self._last_try) # BOOL
                case (1, x, y) : return_list.append(self.recount) # INT
                case (2, True, _) : return_list.append(self.data) # STR
                case (2, False, True) : return_list.append(whoosh(self.data))
                case (2, False, False) : return_list.append('')
                case (3, True, _) : return_list.append(self) # STL
                case (3, False, _) : return_list.append(None)
                case (32, True, _): # ALL
                    return_list.extend((self._last_try, self.recount, self.data, self))
                case (32, False, True):
                    return_list.extend((self._last_try, self.recount, whoosh(self.data), None))
                case (32, False, False):
                    return_list.extend((self._last_try, self.recount, '', None))
                case (33, x, y): return_list.append(self.data) # F_STR
                case (34, x, y): return_list.append(self) # F_STL
                case (35, x, y): # F_ALL
                    return_list.extend((self._last_try, self.recount, self.data, self))
        def _handle_end(self, end):
            match [self._last_try, self.invisible_ink]:
                case [True, _] : return end
                case [False, False] : return ''
                case [False, True] : return whoosh(end)

        print(self.__str__(), end=_handle_end(self, end), file=file, flush=flush)

        return_list = []

        if isinstance(return_type, _Iterable):
            for item in return_type:
                if item in [BOOL, INT, STR, STL, ALL]: _append_to_return_list(self, item)
        else: _append_to_return_list(self, return_type)

        match len(return_list):
            case 0 : return None
            case 1 : return return_list[0]
            case _ : return return_list

    def modify(self, string : str | s_b | s_c = None, case : _Any = None, case_list : _Iterable = None, *,  negated : bool = None, invisible_ink : bool = None, case_sensitive : bool = None):
        """An easy way to modify the object's parameters. Specially
        useful when you convert between strool types. It modifies the object and
        returns it, so you can use it when you save the object into a variable
        or when it is already given a variable name.
        
        This method ignores variables set to None. To set the value of "case" to
        None, do `object.case = None`."""
        if string == None: pass
        else: self.data = string
        if case == None: pass
        else: self.case = case
        if negated == None: pass
        else: self.negated = negated
        if invisible_ink == None: pass
        else: self.invisible_ink = invisible_ink
        if case_list == None: pass
        else: self.case_list = case_list
        if case_sensitive == None: pass
        else: self.case_sensitive = case_sensitive
        
        return self

    def _debug(self):
        try: cs = self.case_sensitive
        except: cs = None

        try: cl = self.case_list
        except: cl = None

        lista_variables = [self.data, self.case, self.negated, self.invisible_ink, self.recount, self._last_try, cl, cs]
        print('\nVariables:', type(self))
        for valores, nombres in zip(lista_variables, self.__slots__):
            print(nombres, ':', valores)

class String_case(String_bool):
    """String_case - A string, but it will show text or not, depending if
    "case" can be found on "case_list"

    Unique parameters:
    - case_list: list of items to compare with "case", to find a match.
    - case_sensitive: if true, when "case" is a string, it won't consider
    something a match unless the uppercase and lowercase letters match.

    Parameters shared with String_bool (slightly different use):
    - string: actual text stored, it will be shown if "case" matches a case
    in "case_list".
    - case: item to be found in "case_list".
    - negated: if true, text will be shown when "case" is NOT in "case_list".
    - invisible_ink: if true, when text must be hidden, it'll be substituted
    with invisible characters (useful when your program's structure is
    partly or completely determined by text, specially console programs).
    
    Except for "string", all parameters are saved inside the object with the
    name of the parameter (e.g.: "case" is saved in "object.case"). The
    parameter "string" is saved in "object.data".

    Methods (identical to those from String_bool):
    - check: returns True if text would be shown, otherwise False.
    - reset_count: sets the counter of how many times the text has been
    shown to 0.
    - print: prints the text if "check" returns True, otherwise it'll not
    print anything, unless "invisible_ink" is True, then it'll print
    invisible text. To keep track of what has been printed, you can set
    "return_type" to BOOL, INT, STR, STL, to get True or False, how many
    times it has been shown, the string shown or the strool object,
    respectively. You can give return types in a list, and it will return
    them in the order you provided, unless you give the return type ALL. ALL
    will provide BOOL, INT, STR and STL (means strool) in that order.
    - modify: an easy way to modify the object's parameters. Specially
    useful when you convert between strool types. It modifies the object and
    returns it, so you can use it when you save the object into a variable
    or when it is already given a variable name.

    To convert between strool types, simply give the old strool object to
    the new strool constructor. e.g.:
    `new_object = stl.String_bool(string_case_object))`.
    It'll ignore any parameters and save all data from the object. If you
    convert from String_case to String_bool, it'll keep the data from
    case_list and case_sensitive, to be able to use it again if you turn it
    into a String_case again."""

    def __init__(self, string: str | s_b | s_c , case: _Any = None, case_list : _Iterable = [], *, case_sensitive : bool = False, negated: bool = False, invisible_ink: bool = False) -> None:
        super().__init__(string, case, negated=negated, invisible_ink=invisible_ink)
        
        try:
            self.case_list = string.case_list
            self.case_sensitive = string.case_sensitive
        except:
            self.case_list = case_list
            self.case_sensitive = case_sensitive

    def check(self):
        """It will return True if text would be shown (visibly), otherwise False"""
        match (isinstance(self.case, (str, _UserString)), self.case_sensitive):
            case ( True, False ) :
                case = self.case.casefold()
                case_list = []
                for item in self.case_list:
                    try: case_list.append(item.casefold())
                    except: case_list.append(item)                
            case _ :
                case = self.case
                case_list = self.case_list
            
        if self.negated: return not case in case_list
        else: return case in case_list
    
b = s_b = String_bool
c = s_c = String_case
