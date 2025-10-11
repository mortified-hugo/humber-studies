# 2 Loans Comparison

"""
Write a program that lets the user enter the loan amount and loan period in a number
of years and displays the monthly and total payments for each interest rate starting
from 5% to 8%, with an increment of 1/8.
"""


def interest_formula(loan_amount: float, interest_rate: float, n_of_months: int):
    # Formula according to the example in compute_loan.py
    monthly_payment = loan_amount * interest_rate / (1 - 1 / (1 + interest_rate) ** n_of_months)
    total_payment = monthly_payment * n_of_months

    return monthly_payment, total_payment


def create_roi_table(loan_amount: float, n_of_years: int):
    # Get the number of months
    n_of_months = n_of_years * 12
    # Define annual rate at 5%
    annual_interest_rate = 0.05

    # Header formated
    print(f"{'Interest Rate':<14}{'Monthly Payment':<16}{'Total Payment':<13}")

    # While loop to print the rows of the table. Adding 1/8 of a % each iteration.
    while annual_interest_rate < 0.081:  # Value to break it (more than 8, less than 8.125)
        # Get the monthly rate
        monthly_rate = annual_interest_rate/12
        # Use the interest formula
        monthly_payment, total_payment = interest_formula(loan_amount, monthly_rate, n_of_months)

        # Prepare the table rows (in a pretty way)
        interest_rate_as_percentage = f"{annual_interest_rate*100:.3f}%"
        print(f"{interest_rate_as_percentage:<14}{monthly_payment:<17.2f}{total_payment:<13.2f}")

        # Iterate interest rate
        annual_interest_rate += 0.00125
        annual_interest_rate = round(annual_interest_rate, 5)


# Run function
create_roi_table(loan_amount=float(input("Enter the loan amount, for example, 12000.95: ")),
                 n_of_years=int(input("Enter the number of years as an integer, for example, 3: ")))
