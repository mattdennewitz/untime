import ast
import pathlib

from .rules import *  # noqa


def analyze_file(input_path: str):
    """
    Analyze the complexity of a Python file.

    Args:
        input_path: The path to the Python file to analyze.

    Returns:
        A tuple containing a dictionary of complexity scores and the total score
    """

    with pathlib.Path(input_path).open("r") as source:
        tree = ast.parse(source.read())

    class_names = {
        node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
    }
    global_vars = {node.id for node in ast.walk(tree) if isinstance(node, ast.Global)}
    class_methods = {
        method.name
        for cls in ast.walk(tree)
        if isinstance(cls, ast.ClassDef)
        for method in cls.body
        if isinstance(method, ast.FunctionDef)
    }

    scores = {
        "cyclomatic_complexity": calculate_cyclomatic_complexity(tree),
        "nesting_depth": calculate_nesting_depth(tree),
        "function_length": sum(
            calculate_function_length(node) for node in ast.walk(tree)
        ),
        "parameter_count": sum(
            calculate_parameter_count(node) for node in ast.walk(tree)
        ),
        "class_coupling": sum(
            calculate_class_coupling(node, class_names) for node in ast.walk(tree)
        ),
        "cohesion": sum(calculate_cohesion(node) for node in ast.walk(tree)),
        "global_variable_usage": calculate_global_variable_usage(tree, global_vars),
        "inheritance_depth": calculate_inheritance_depth(tree),
        "number_of_interfaces": sum(
            calculate_number_of_interfaces(node) for node in ast.walk(tree)
        ),
        "polymorphism": sum(
            calculate_polymorphism(node, class_methods) for node in ast.walk(tree)
        ),
        'calculate_import_complexity': calculate_import_complexity(tree),
    }

    total_score = sum(scores.values()) / len(scores)

    return scores, total_score
