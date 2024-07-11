import re


class InvalidRule(Exception):
    """
    Custom exception for invalid grammar rules.
    """
    pass


class ContextFreeGrammar:
    def __init__(self, variables: list[str],
                 terminals: list[str],
                 rules: dict[str, list[list[str]]],
                 start_variable: str):
        """
        Initialize the ContextFreeGrammar object.

        Parameters:
        variables (list[str]): List of variables (non-terminals) in the grammar.
        terminals (list[str]): List of terminals in the grammar.
        rules (dict[str, list[list[str]]]): Dictionary of production rules.
        start_variable (str): The start variable of the grammar.
        """
        self.variables = set(variables)  # Store variables as a set
        self.terminals = set(terminals)  # Store terminals as a set
        self.rules = rules  # Store production rules
        self.start_variable = start_variable  # Store start variable

        # Sort rules with the start variable at the beginning
        self.sort_rules()

    def sort_rules(self):
        """
        Sort the production rules to ensure the start variable's rules come first.
        """
        new_rules = {self.start_variable: self.rules[self.start_variable]}
        for variable, products in self.rules.items():
            if variable != self.start_variable:
                new_rules[variable] = products.copy()

        # Update the rules with the sorted rules
        self.rules = new_rules

    def add_product(self, variable: str, product: list[str]):
        """
        Add a new product (production rule) to a variable.

        Parameters:
        variable (str): The variable to which the product is added.
        product (list[str]): The product to add.
        """
        # Ensure the variable is in the set of variables
        self.variables.add(variable)

        if variable in self.rules.keys():
            # Append the product if it doesn't exist
            if product not in self.rules[variable]:
                self.rules[variable].append(product)
        else:
            # Create a new entry if the variable doesn't exist
            self.rules[variable] = [product]

    def add_rule(self, lhs: str, rhs: list[list[str]]):
        """
        Add a new rule to the grammar.

        Parameters:
        lhs (str): The left-hand side variable of the rule.
        rhs (list[list[str]]): The right-hand side productions of the rule.

        Raises:
        InvalidRule: If the left-hand side does not match the required pattern.
        """
        # Ensure lhs is in the correct format
        if not re.match(r'[A-Z]\d*$', lhs):
            raise InvalidRule

        for rhs_item in rhs:
            for item in rhs_item:
                if item.isupper() and item not in self.variables:
                    # Add new variable if it is not present
                    self.variables.add(item)

                if item.islower() or item == 'ε':
                    # Add new terminal if it is not present
                    self.terminals.add(item)

            # Add the right-hand side product
            self.add_product(lhs, rhs_item)

    def __repr__(self):
        """
        Provide a string representation of the grammar.

        Returns:
        str: The string representation of the grammar.
        """
        s = []
        for variable, product in self.rules.items():
            right_hand_side = [''.join(item) for item in product]

            # Format each rule
            s.append(f"{variable} → {'|'.join(right_hand_side)}")

        # Join all rules with newline characters
        return '\n'.join(s)
