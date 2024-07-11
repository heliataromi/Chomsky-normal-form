from context_free_grammar import ContextFreeGrammar
from itertools import product


def generate_combinations(item: list[str], variable: str) -> list[list[str]]:
    """
    Generate all combinations of a list where a specific variable can be replaced
    by None or kept as is.

    Parameters:
    item (list): The list containing the items to be combined.
    variable (str): The variable to be replaced by None.

    Returns:
    list: A list of lists with all possible combinations where the variable is
          either None or retained.
    """
    # Find indices of the variable in the list
    indices = [i for i, x in enumerate(item) if x == variable]

    # Generate all binary combinations for the indices
    combinations = product([0, 1], repeat=len(indices))

    results = []
    for combination in combinations:
        new_list = item[:]
        for idx, include in zip(indices, combination):
            if not include:
                # Replace with None based on the combination
                new_list[idx] = None

        # Remove None elements
        result = [x for x in new_list if x is not None]

        # If result is empty, add epsilon ('ε')
        results.append(result if result else ['ε'])

    return results


def replace_products(grammar: ContextFreeGrammar, variable: str, products: list[list[str]]):
    """
    Replace the products of a given variable in the grammar with new products.

    Parameters:
    grammar (ContextFreeGrammar): The grammar object.
    variable (str): The variable whose products are to be replaced.
    products (list[list[str]]): The new products to replace the old ones.
    """
    # Clear existing products
    grammar.rules[variable].clear()

    # Add new products
    for product in products:
        grammar.add_product(variable, product)


def change_start_variable(grammar: ContextFreeGrammar):
    """
    Change the start variable of the grammar to a new variable 'S0' if needed.

    Parameters:
    grammar (ContextFreeGrammar): The grammar object.
    """
    for variable, products in grammar.rules.items():
        for product in products:

            # Check if the start variable is used in any production
            if product == [grammar.start_variable]:
                # Add a new start rule
                grammar.add_rule('S0', [[grammar.start_variable]])

                # Change the start variable
                grammar.start_variable = 'S0'

                # Sort rules based on new start variable
                grammar.sort_rules()
                return


def remove_epsilon_rules(grammar: ContextFreeGrammar):
    """
    Remove epsilon (empty string) rules from the grammar.

    Parameters:
    grammar (ContextFreeGrammar): The grammar object.
    """
    visited = set()
    nullable = {variable for variable, products in grammar.rules.items() if ['ε'] in products}

    while nullable:
        variable = nullable.pop()
        grammar.rules[variable].remove(['ε'])  # Remove epsilon rule
        visited.add(variable)

        for var, pros in grammar.rules.items():
            new_pros = []
            for pro in pros:
                if variable in pro:
                    # Generate combinations without the variable
                    new_pros.extend(generate_combinations(pro, variable))
                else:
                    new_pros.append(pro)

            # Replace products with new ones
            replace_products(grammar, var, new_pros)

            # Add variable to nullable set if it has epsilon production
            if ['ε'] in grammar.rules[var] and var not in visited:
                nullable.add(var)


def remove_unit_rules(grammar: ContextFreeGrammar):
    """
    Remove unit rules (rules where a variable produces another single variable) from the grammar.

    Parameters:
    grammar (ContextFreeGrammar): The grammar object.
    """
    unit_pairs = [(variable, product) for variable, products in grammar.rules.items()
                  for product in products if len(product) == 1 and product[0] in grammar.variables]

    for i, (variable, product) in enumerate(unit_pairs):
        if product[0] != variable:
            # Remove unit production
            grammar.rules[variable].remove(product)

            # Add new products if it wasn't removed before
            if not any([(variable, item) in unit_pairs[:i] for item in grammar.rules[product[0]]]):
                grammar.add_rule(variable, grammar.rules[product[0]])


def convert_to_proper_form(grammar: ContextFreeGrammar):
    """
    Convert the grammar to proper form (Chomsky Normal Form).

    Parameters:
    grammar (ContextFreeGrammar): The grammar object.
    """
    i = 1
    index = 0

    # Step 1: Ensure all productions have at most 2 variables
    while index < len(grammar.rules.items()):
        variable = list(grammar.rules.keys())[index]
        products = grammar.rules[variable]

        for product in products:
            if len(product) >= 3:
                grammar.rules[variable].remove(product)

                new_variable = f'U{i}'
                new_product = [product[1:]]

                for var, pros in grammar.rules.items():
                    if new_product == pros:
                        grammar.add_rule(variable, [[product[0], var]])
                        break
                else:
                    grammar.add_rule(new_variable, new_product)
                    grammar.add_rule(variable, [[product[0], new_variable]])
                    i += 1

        index += 1

    index = 0

    # Step 2: Ensure all terminals are only in unit productions
    while index < len(grammar.rules.items()):
        variable = list(grammar.rules.keys())[index]
        products = grammar.rules[variable]

        for j, product in enumerate(products):
            if len(product) >= 2:
                if product[0] in grammar.terminals:
                    new_variable = f'U{i}'
                    new_product = [[product[0]]]

                    for var, pros in grammar.rules.items():
                        if new_product == pros:
                            grammar.rules[variable][j] = [var, product[1]]
                            break
                    else:
                        grammar.add_rule(new_variable, new_product)
                        grammar.rules[variable][j] = [new_variable, product[1]]
                        i += 1

                product = grammar.rules[variable][j]

                if product[1] in grammar.terminals:
                    new_variable = f'U{i}'
                    new_product = [[product[1]]]

                    for var, pros in grammar.rules.items():
                        if new_product == pros:
                            grammar.rules[variable][j] = [product[0], var]
                            break
                    else:
                        grammar.add_rule(new_variable, new_product)
                        grammar.rules[variable][j] = [product[0], new_variable]
                        i += 1

        index += 1


def main(grammar: ContextFreeGrammar):
    """
    Main function to convert a context-free grammar to Chomsky Normal Form.

    Parameters:
    grammar (ContextFreeGrammar): The grammar object.

    Returns:
    ContextFreeGrammar: The transformed grammar.
    """
    change_start_variable(grammar)
    remove_epsilon_rules(grammar)
    remove_unit_rules(grammar)
    convert_to_proper_form(grammar)
    return grammar


if __name__ == "__main__":
    # Input grammar details from the user
    variables = input("Enter the variables: ").split()
    terminals = input("Enter the terminals: ").split()
    rules = dict()
    for variable in variables:
        rules[variable] = list(map(list, input(f"Enter the products of {variable}: ").split()))
    start_variable = input("Enter the start variable: ")

    # Create a grammar object
    grammar = ContextFreeGrammar(variables,
                                 terminals,
                                 rules,
                                 start_variable)

    # Transform the grammar to Chomsky Normal Form
    print(main(grammar))
