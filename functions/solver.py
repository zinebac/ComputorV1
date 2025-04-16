from fractions import Fraction
import matplotlib.pyplot as plt


def sqrt(x:float) -> float:
    """square root function
        This function computes the square root of a number using the Newton-Raphson method.
        It raises a ValueError if the input is negative.

    Args:
        x (float):  The number to compute the square root of.
                    It must be a non-negative number.

    Raises:
        ValueError: If the input number is negative.

    Returns:
       float: The square root of the input number.
    """
    if x < 0:
        raise ValueError("Cannot compute square root of a negative number.")
    elif x == 0:
        return 0
    else:
        approx = x / 2.0
        while True:
            better_approx = (approx + x / approx) / 2.0
            if abs(better_approx - approx) < 1e-10:
                return better_approx
            approx = better_approx
            
def graph(a, b, c):
    """Draw the graph of a polynomial function.
        This function generates a graph of the polynomial function f(x) = ax² + bx + c.
        It uses matplotlib to create the graph and displays it.

    Args:
        a (any): the coefficient of x² in the polynomial function.
        b (any): the coefficient of x in the polynomial function.
        c (any): the constant term in the polynomial function.
    """
    x_vals = [x / 100.0 for x in range(-500, 501)]
    y_vals = [a * x ** 2 + b * x + c for x in x_vals]

    plt.figure(figsize=(8, 5))
    plt.axhline(0, color='gray', lw=1)
    plt.axvline(0, color='gray', lw=1)
    plt.plot(x_vals, y_vals, label=f"f(x) = {a}x² + {b}x + {c}", color='blue')
    plt.title("Polynomial Graph")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def solver(reduced: dict, degree: int, show_fraction=False, show_decimal=True, verbose=False, show_graph=False):
    """Solve a polynomial equation of degree 0, 1, or 2.
        This function takes a reduced polynomial equation and its degree as input,
        and computes the solutions based on the degree of the polynomial.

    Args:
        reduced (dict): a dictionary representing the reduced polynomial equation.
        degree (int): the degree of the polynomial equation.
        show_fraction (bool, optional): _description_. Defaults to False.
        show_decimal (bool, optional): _description_. Defaults to True.
        verbose (bool, optional): _description_. Defaults to False.
        show_graph (bool, optional): _description_. Defaults to False.
    """
    def fmt(x):
        return str(Fraction(x).limit_denominator()) if show_fraction and not show_decimal else \
               f"{Fraction(x).limit_denominator()} ({round(x, 6)})" if show_fraction and show_decimal else \
               str(round(x, 6))

    if degree == 0:
        print("\033[92mNo solution.\033[0m" if reduced.get(0, 0) != 0 else "\033[92mAll real numbers are solutions.\033[0m")

    elif degree == 1:
        a = reduced.get(1, 0)
        b = reduced.get(0, 0)
        if a == 0:
            print("\033[92mNo solution.\033[0m" if b != 0 else "\033[92mAll real numbers are solutions.\033[0m")
        else:
            x = -b / a
            print(f"\033[92mThe solution is:\033[0m\033[1m\n{fmt(x)}\033[0m")

    elif degree == 2:
        a = reduced.get(2, 0)
        b = reduced.get(1, 0)
        c = reduced.get(0, 0)
        discriminant = b**2 - 4*a*c

        if verbose:
            print(f"\033[95m[Solver] Discriminant: Δ = b² - 4ac = {b}² - 4*{a}*{c} = {discriminant}\033[0m")

        if discriminant > 0:
            root1 = (-b + sqrt(discriminant)) / (2*a)
            root2 = (-b - sqrt(discriminant)) / (2*a)
            print(f"\033[92mDiscriminant is strictly positive, the two solutions are:\033[0m\033[1m\n{fmt(root1)}\n{fmt(root2)}\033[0m")
        elif discriminant == 0:
            root = -b / (2*a)
            print(f"\033[92mOne real solution:\033[0m\033[1m\n{fmt(root)}\033[0m")
        else:
            real = -b / (2*a)
            imag = sqrt(abs(discriminant)) / (2*a)
            print(f"\033[92mDiscriminant is strictly negative, Two complex solutions:\033[0m\033[1m\n{fmt(real)} + {fmt(imag)}i\n{fmt(real)} - {fmt(imag)}i\033[0m")

        if show_graph:
            graph(a, b, c)

