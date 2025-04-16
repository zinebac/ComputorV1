import sys
import argparse
from functions.parser import parser
from functions.reducer import reducer
from functions.solver import solver

def main():    
    try: 
        arg_parser = argparse.ArgumentParser(
            prog="computer.py",
            description="\033[94m🧠 ComputorV1: Polynomial Equation Solver — Solve equations up to degree 2\033[0m",
            epilog="\033[94m📌 Example: python3 computer.py '5 * X^0 + 4 * X^1 = 1 * X^0' --verbose\033[0m",
            formatter_class=argparse.RawTextHelpFormatter
        )
        
        # Add arguments
        
        arg_parser.add_argument(
            'equation',
            type=str,
            help="Polynomial equation in the form 'a * X^b = c'"
        )
        arg_parser.add_argument(
            '--fraction', '-f',
            action='store_true',
            help="Display result as a fraction (irreducible form)"
        )
        arg_parser.add_argument(
            '--decimal', '-d',
            action='store_true',
            help="Display result as a decimal (default)"
        )
        arg_parser.add_argument(
            '--verbose', '-v',
            action='store_true',
            help="Display additional output"
        )
        arg_parser.add_argument(
            '--graph', '-g',
            action='store_true',
            help="Display the graph of the polynomial"
        )
        
        if len(sys.argv) == 1:
            arg_parser.print_help(sys.stderr)
            sys.exit(1)

        args = arg_parser.parse_args()
        
        left, right = args.equation.split('=', 1)
        left_dict = parser(left)
        right_dict = parser(right)
        reduced, equation_str = reducer(left_dict, right_dict, verbose=args.verbose)
        
        print(f"\033[92mReduced equation:\033[0m \033[1m{equation_str}\033[0m")

        degree = max(reduced.keys()) if reduced else 0
        print(f"\033[92mPolynomial degree:\033[0m \033[1m{degree}\033[0m")

        if degree > 2:
            raise ValueError("The polynomial degree is strictly greater than 2, I can't solve.")

        # Call solution function
        solver(
            reduced,
            degree,
            show_fraction=args.fraction,
            show_decimal=args.decimal or not args.fraction,  # default to decimal
            verbose=args.verbose,
            show_graph=args.graph
        )
    except ValueError as e:
        print(f"\033[91m❌ Error: {e}\033[0m")
    except Exception as e:
        print(f"\033[91m❌ An unexpected error occurred: {e}\033[0m")

if __name__ == '__main__':
    main()