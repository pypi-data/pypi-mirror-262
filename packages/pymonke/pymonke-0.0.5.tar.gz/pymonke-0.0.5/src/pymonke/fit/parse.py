from mypy_extensions import VarArg
import nltk
import numpy as np
from pandas import Series

from typing import Callable, List, Tuple, TypeAlias, Iterable, Dict

scalar: TypeAlias = float | int
array: TypeAlias = Series | np.ndarray
numerical: TypeAlias = scalar | array
func_type: TypeAlias = Callable[[VarArg(str)], str]


def __gauss(*args: str) -> str:
    return f"({args[0]} * exp((-(x - {args[1]}) ** 2) / (2 * {args[2]} ** 2)))"


def __linear(*args: str) -> str:
    return f"({args[0]} * x + {args[1]})"


__ALPH_OPERATORS = {
    'arccos': 'np.arccos',
    'arccosh': 'np.arccosh',
    'arcsin': 'np.arcsin',
    'arcsinh': 'np.arcsinh',
    'arctan': 'np.arctan',
    'arctanh': 'np.arctanh',
    'cos': 'np.cos',
    'cosh': 'np.cosh',
    'e': 'np.e',
    'exp': 'np.exp',
    'log': 'np.log',
    'pi': 'np.pi',
    'sin': 'np.sin',
    'sinh': 'np.sinh',
    'tan': 'np.tan',
    'tanh': 'np.tanh',
}

__SYMBOL_OPERATORS = {
    '*': '*',
    '+': '+',
    '-': '-',
    '/': '/',
    '^': '**',
}

__FUNCS: Dict[str, Tuple[func_type, List[str]]] = {
    "gauss": (__gauss, ["a", "x0", "sigma"]),
    "linear": (__linear, ["m", "b"]),
}


def __get_unique_name(name: str, params: List[str]) -> str:
    if name not in params:
        return name
    i = 1
    while (out := f"{name}{i}") in params:
        i += 1
        continue

    return out


def __is_param(token: str) -> bool:
    answer = (token not in __ALPH_OPERATORS and token not in __FUNCS and token.isalnum() and
              not token.isnumeric() and token != "x")
    if answer and token[0].isnumeric():
        raise ValueError("param names cannot start with a number")
    return answer


def rename_parameters(_formula: str, rename: Dict[str, str]) -> str:
    tokens = nltk.tokenize.wordpunct_tokenize(_formula)
    for index, token in enumerate(tokens):
        for key in rename.keys():
            if key == token:
                tokens[index] = rename[key]

    return "".join(tokens)


def replace_funcs(_formula: str) -> str:
    tokens = nltk.tokenize.wordpunct_tokenize(_formula)
    params: List[str] = []
    for token in tokens:
        if __is_param(token) and token not in params:
            params.append(token)

    for index, token in enumerate(tokens):
        if token in __FUNCS:
            b = [__get_unique_name(i, params) for i in __FUNCS[token][1]]
            tokens[index] = __FUNCS[token][0](*b)
            params.extend(b)

    return "".join(tokens)


def parse_function(_formula: str) -> Tuple[Callable[[numerical, VarArg(float | int)], numerical], List[str]]:
    """Creates a python function out of a string that represents a mathematical formula.
    x is the variable and all the other arguments are passed as positional arguments to the
    generated callable with the form f(x: float, *params) -> float.
    Returns the callable and a list of all the arguments mentioned in _formula"""
    tokens = nltk.tokenize.wordpunct_tokenize(_formula)
    params: List[str] = []
    for index, token in enumerate(tokens):
        if token in __ALPH_OPERATORS:
            tokens[index] = __ALPH_OPERATORS[token]
        elif __is_param(token):
            params.append(token)

    def function(x: numerical, *_params: scalar) -> numerical:
        if isinstance(x, Iterable):
            return np.array([function(i, *_params) for i in x])
        else:
            try:
                float(x)
            except TypeError:
                raise TypeError(r"Argument x must be a number or an iterable.")
        nonlocal tokens, params
        _tokens = tokens.copy()
        for i, tok in enumerate(_tokens):
            if tok in params:
                param_index = params.index(tok)
                _tokens[i] = str(_params[param_index])
            if tok == "x":
                _tokens[i] = str(x)
        string = " ".join(_tokens)
        for op in __SYMBOL_OPERATORS.keys():
            string = string.replace(op, __SYMBOL_OPERATORS[op])
        return eval(string)

    return function, params
