import argparse

if __name__ == "__main__":
    # Get input
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
    n = int(args.number)
    if n < 0:
        raise ValueError("The number n must be non-negative!")

    # Define factorial function
    def fac(n):
        return n * fac(n - 1) if n > 1 else 1

    print("factorial({:d}) = {:d}".format(n, fac(n)))
