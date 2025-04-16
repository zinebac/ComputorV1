def reducer(left: dict, right: dict, verbose=False):
    """Reduce a polynomial equation by subtracting the right side from the left side.
        The function combines like terms, removes near-zero coefficients, and formats the output.

    Args:
        left (dict): _left side polynomial terms_.
        right (_type_): _right side polynomial terms_.
        verbose (bool, optional): _description_. Defaults to False.
    """
    def format_terms(terms_dict: dict) -> str:
        """Format the polynomial terms into a human-readable string.
            This function sorts the terms by exponent in descending order and formats them with their coefficients.
            It handles positive and negative signs appropriately.

        Args:
            terms_dict (dict): a dictionary of polynomial terms.

        Returns:
            string: a formatted string representation of the polynomial.
        """
        if not terms_dict:
            return "0"
        sorted_items = sorted(terms_dict.items(), key=lambda x: -x[0])
        parts = []
        for i, (exp, coeff) in enumerate(sorted_items):
            coeff = int(coeff) if coeff.is_integer() else round(coeff, 6)
            sign = "+" if coeff >= 0 and i != 0 else ""
            if exp == 0:
                part = f"{coeff}"
            elif exp == 1:
                part = f"{coeff} * X"
            else:
                part = f"{coeff} * X^{exp}"
            parts.append(f"{sign} {part}".strip())
        return " ".join(parts)

    reduced = {}

    if verbose:
        left_str = format_terms(left)
        right_str = format_terms(right)
        print("\033[95m[Reducer] Left side terms:\033[0m", left_str)
        print("\033[95m[Reducer] Right side terms:\033[0m", right_str)
        print(f"\033[95m[Reducer] Equation before reduction:\033[0m ({left_str}) - ({right_str}) = 0")

    # Subtract right from left
    for exp in left:
        reduced[exp] = left[exp]
    for exp in right:
        reduced[exp] = reduced.get(exp, 0.0) - right[exp]

    if verbose:
        print("\033[95m[Reducer] After subtraction:\033[0m", format_terms(reduced))

    # Remove near-zero coefficients
    reduced = {exp: coeff for exp, coeff in reduced.items() if abs(coeff) > 1e-9}

    if verbose:
        print("\033[95m[Reducer] After removing zeros:\033[0m", format_terms(reduced))

    if not reduced:
        return reduced, "0 = 0"

    # Sort and format final reduced equation
    sorted_terms = sorted(reduced.items(), key=lambda x: -x[0])
    equation_parts = []

    for i, (exp, coeff) in enumerate(sorted_terms):
        coeff = int(coeff) if coeff.is_integer() else round(coeff, 6)
        abs_coeff = abs(coeff)
        if exp == 0:
            term = f"{abs_coeff}"
        elif exp == 1:
            term = f"{abs_coeff} * X"
        else:
            term = f"{abs_coeff} * X^{exp}"
        if i == 0:
            equation_parts.append(f"-{term}" if coeff < 0 else f"{term}")
        else:
            sign = "-" if coeff < 0 else "+"
            equation_parts.append(f"{sign} {term}")

    equation_str = " ".join(equation_parts) + " = 0"

    return reduced, equation_str
