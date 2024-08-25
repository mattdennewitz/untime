import ast


def calculate_cyclomatic_complexity(node) -> float:
    """
    Calculate the cyclomatic complexity of a node in the AST.

    The cyclomatic complexity is a software metric that measures the number of
    linearly independent paths through a program's source code.

    Args:
        node: An AST node.

    Returns:
        A float between 0.0 and 1.0 representing the cyclomatic complexity of
        the node. A value of 0.0 indicates that the node has no control flow
        complexity, while a value of 1.0 indicates that the node has maximum
        control flow complexity.
    """

    complexity = 0

    if isinstance(
        node, (ast.If, ast.For, ast.While, ast.With, ast.Try, ast.ExceptHandler)
    ):
        complexity += 1

    for child in ast.iter_child_nodes(node):
        complexity += calculate_cyclomatic_complexity(child)

    return min(complexity / 10.0, 1.0)


def calculate_nesting_depth(node, current_depth=0) -> float:
    """
    Calculate the nesting depth of a node in the AST.

    The nesting depth is a software metric that measures the maximum depth of
    nested control structures in a program's source code.

    Args:
        node: An AST node.
        current_depth: An integer representing the current nesting depth.

    Returns:
        A float between 0.0 and 1.0 representing the nesting depth of the node.
        A value of 0.0 indicates that the node is not nested within any control
        structures, while a value of 1.0 indicates that the node is nested to
        the maximum depth.
    """

    if isinstance(node, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
        current_depth += 1

    max_depth = current_depth

    for child in ast.iter_child_nodes(node):
        max_depth = max(max_depth, calculate_nesting_depth(child, current_depth))

    return min(max_depth / 5.0, 1.0)


def calculate_function_length(node) -> float:
    """
    Calculate the length of a function in lines of code.

    Args:
        node: An AST node.

    Returns:
        A float between 0.0 and 1.0 representing the length of the function.
        A value of 0.0 indicates that the function is empty, while a value of
        1.0 indicates that the function is very long.
    """

    if isinstance(node, ast.FunctionDef):
        return min(len(node.body) / 50.0, 1.0)

    return 0.0


def calculate_parameter_count(node) -> float:
    """
    Calculate the number of parameters in a function.

    Args:
        node: An AST node.

    Returns:
        A float between 0.0 and 1.0 representing the number of parameters in
        the function. A value of 0.0 indicates that the function has no
        parameters, while a value of 1.0 indicates that the function has many
        parameters.
    """

    if isinstance(node, ast.FunctionDef):
        return min(len(node.args.args) / 10.0, 1.0)

    return 0.0


def calculate_class_coupling(node, class_names) -> float:
    """
    Calculate the class coupling of a node in the AST. Class coupling is a
    measures the number of other classes that a class is dependent on.

    Args:
        node: An AST node.
        class_names: A set of class names in the AST.

    Returns:
        A float between 0.0 and 1.0 representing the class coupling of the node.
    """

    if isinstance(node, ast.ClassDef):
        num_references = sum(
            isinstance(child, ast.Name) and child.id in class_names
            for child in ast.walk(node)
        )

        return min(num_references / 10.0, 1.0)

    return 0.0


def calculate_cohesion(node) -> float:
    """
    Calculate the cohesion of a class in the AST. Cohesion is a measure of how
    closely related the methods of a class are to each other.

    Args:
        node: An AST node.

    Returns:
        A float between 0.0 and 1.0 representing the cohesion of the class.
    """

    if isinstance(node, ast.ClassDef):
        methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]

        if not methods:
            return 0.0

        attributes = {n.attr for n in ast.walk(node) if isinstance(n, ast.Attribute)}
        shared_attributes = sum(
            any(attr in attributes for attr in ast.walk(method)) for method in methods
        )

        return 1.0 - (shared_attributes / len(methods))

    return 0.0


def calculate_global_variable_usage(node, global_vars) -> float:
    """
    Calculate the usage of global variables in a node in the AST.

    Args:
        node: An AST node.
        global_vars: A set of global variable names in the AST.

    Returns:
        A float between 0.0 and 1.0 representing the usage of global variables
        in the node.
    """

    usage_count = sum(
        isinstance(child, ast.Name) and child.id in global_vars
        for child in ast.walk(node)
    )

    return min(usage_count / 10.0, 1.0)


def calculate_inheritance_depth(node, depth=0) -> float:
    """
    Calculate the inheritance depth of a class in the AST.

    The inheritance depth is a software metric that measures the number of
    classes that a class is derived from.

    Args:
        node: An AST node.
        depth: An integer representing the current inheritance depth.

    Returns:
        A float between 0.0 and 1.0 representing the inheritance depth of the
        class. A value of 0.0 indicates that the class does not inherit from any
        other classes, while a value of 1.0 indicates that the class has maximum
        inheritance depth.
    """
    if isinstance(node, ast.ClassDef):
        depth += len(node.bases)

    max_depth = depth

    for child in ast.iter_child_nodes(node):
        max_depth = max(max_depth, calculate_inheritance_depth(child, depth))

    return min(max_depth / 5.0, 1.0)


def calculate_number_of_interfaces(node) -> float:
    """
    Calculate the number of interfaces implemented by a class in the AST.

    Args:
        node: An AST node.

    Returns:
        A float between 0.0 and 1.0 representing the number of interfaces
        implemented by the class. A value of 0.0 indicates that the class does
        not implement any interfaces, while a value of 1.0 indicates that the
        class implements many interfaces.
    """

    if isinstance(node, ast.ClassDef):
        return min(len(node.bases) / 5.0, 1.0)

    return 0.0


def calculate_polymorphism(node, class_methods) -> float:
    """
    Calculate the polymorphism of a class in the AST.

    Polymorphism is a software metric that measures the number of methods in a
    class that override methods in its parent classes.

    Args:
        node: An AST node.
        class_methods: A set of method names in the class.

    Returns:
        A float between 0.0 and 1.0 representing the polymorphism of the class.
    """

    if isinstance(node, ast.ClassDef):
        overridden_methods = sum(
            isinstance(child, ast.FunctionDef) and child.name in class_methods
            for child in node.body
        )

        return min(overridden_methods / 5.0, 1.0)

    return 0.0


def calculate_import_count(node) -> int:
    """
    Calculate the number of import statements in the AST.

    Args:
        node: An AST node.

    Returns:
        An integer representing the number of import statements in the AST.
    """

    if isinstance(node, (ast.Import, ast.ImportFrom)):
        return 1
    return 0


def calculate_import_complexity(tree) -> float:
    """
    Calculate the complexity of the import statements in the AST.

    Args:
        tree: The AST of the Python file.

    Returns:
        A float between 0.0 and 1.0 representing the complexity of the import
        statements in the file. A value of 0.0 indicates that the file has no
        import statements, while a value of 1.0 indicates that the file has
        many import statements.
    """

    import_count = sum(calculate_import_count(node) for node in ast.walk(tree))
    return min(import_count / 20.0, 1.0)
