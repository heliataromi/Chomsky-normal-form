# Chomsky Normal Form for the Context-Free Grammars

This project involves transforming context-free grammars (CFG) into Chomsky Normal Form (CNF). 

Inspired by the "Basis for the Theory of Computation" course at university, I challenged myself to implement the algorithm using Python. The algorithm was presented in ["Introduction to the Theory of Computation"](https://www.google.com/books/edition/Introduction_to_the_Theory_of_Computatio/4J1ZMAEACAAJ?hl=en) by [Michael Sipser](https://math.mit.edu/~sipser/).

## Features

- Define context-free grammars with variables, terminals, production rules, and a start variable.
- Remove epsilon (empty string) productions.
- Remove unit productions (productions where a variable produces another single variable).
- Convert CFGs to Chomsky Normal Form.

## Files

- `context_free_grammar.py`: Contains the `ContextFreeGrammar` class for representing context-free grammars.
- `transform_cnf.py`: Contains functions for transforming a CFG to CNF and the main script to execute the transformation.

## How to Use

Input the variables, terminals, and production rules as prompted.

## Example

Input:
```
Enter the variables: S A B
Enter the terminals: a b ε
Enter the products of S: AB BA
Enter the products of A: aAb ε
Enter the products of B: bBa ε
Enter the start variable: S
```

After transformation, the grammar will be converted to Chomsky Normal Form and displayed.