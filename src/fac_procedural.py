import argparse


def parse_command_line() -> int:
    """Function to parse user input. User input is an integer.
    :Returns: n (input integer)"""
    parser = argparse.ArgumentParser(
        description="Program to calculate \
        factorial of n. Check -h or --help for options. \
        Usage: ./main.py -n 4"
    )
    parser.add_argument(
        "-n",
        "--number",
        default=1,
        help="Non-negative integer for \
        which the factorial shall be computed. Default value: 1",
    )
    args = parser.parse_args()
    return int(args.number)


def print_fac(n, fn) -> None:
    print("factorial({:d}) = {:d}".format(n, factorial(n)))


def _fac_helper(n, fn):
    return _fac_helper(n - 1, fn * n) if n > 1 else fn


def factorial(n) -> int:
    if n < 0:
        raise ValueError("The number n must be non-negative.")
    return _fac_helper(n, 1)


if __name__ == "__main__":
    n = parse_command_line()
    fn = factorial(n)

    print_fac(n, fn)
