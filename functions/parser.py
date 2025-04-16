import re

def parser(side_str: str) -> dict:
    """
    parse the polynomial equation and return a dictionary of terms.

    Args:
        side_str (string):
            The polynomial equation to parse.
            It can contain terms like 2*X^2, -3*X, 5.5, etc.

    Raises:
        ValueError: 
            If the input string is not a valid polynomial equation.
            This includes syntax errors or invalid terms.

    Returns:
        dict: parsed polynomial terms.
                The keys are the exponents and the values are the coefficients.
                For example, for the equation 2*X^2 - 3*X + 5, it returns {2: 2.0, 1: -3.0, 0: 5.0}
    """
    # Remove all whitespaces
    side_str = re.sub(r'\s+', '', side_str)
    
    # Insert missing '*' between digits and X (e.g., 2X → 2*X)
    side_str = re.sub(r'(\d)(X)', r'\1*\2', side_str)
    
    # print(f"Parsing: {side_str}")

    terms = []
    errors = []

    # Regex to capture terms like:
    # - Explicit coefficients: 5*X^2, -3.14*X^1
    # - Implicit coefficients: X^2, -X
    # - Standalone constants: 42, -3.5
    term_pattern = r'''
        ([+-]?)                   # Optional sign
        (?:
            (?:(\d+\.?\d*|\.\d+)  # Coefficient (e.g., 5, 5.5, .5)
               \*?X\^?(\d*))      # Optional '*', X, optional exponent
            |(X)\^?(\d*)          # Implicit coefficient (e.g., X, X^2)
            |(\d+\.?\d*|\.\d+)    # Standalone constant (e.g., 42, -3.5)
        )
    '''

    for match in re.finditer(term_pattern, side_str, re.VERBOSE):
        sign, coeff_str, exp_coeff, x_only, exp_x, const = match.groups()

        if coeff_str:  # Case: explicit coefficient (e.g., 2*X^1)
            coeff = float(sign + coeff_str) if sign else float(coeff_str)
            exp = int(exp_coeff) if exp_coeff else 1
        elif x_only:  # Case: implicit coefficient (e.g., X^1)
            coeff = -1.0 if sign == '-' else 1.0
            exp = int(exp_x) if exp_x else 1
        elif const:  # Case: standalone constant (e.g., -3)
            coeff = float(sign + const) if sign else float(const)
            exp = 0
        else:
            errors.append(f"Invalid term: {match.group()}")
            continue

        terms.append((exp, coeff))

    # Check for unmatched parts (syntax errors)
    clean_str = re.sub(term_pattern, '', side_str, flags=re.VERBOSE)
    if clean_str:
        errors.append(f"Invalid syntax near: '{clean_str}'")

    if errors:
        raise ValueError("\n".join(errors))

    # Combine like terms
    terms_dict = {}
    for exp, coeff in terms:
        terms_dict[exp] = terms_dict.get(exp, 0.0) + coeff

    return terms_dict