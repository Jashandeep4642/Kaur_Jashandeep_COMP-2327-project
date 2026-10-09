# Intermediate Software Development Automated Teller Project

This project will be developed over the course of several assignments.  Each assignment will build on the work done in the previous assignment(s). Ultimately, an entire system will be created to manage bank transactions for clients who have one or more bank accounts.

## Author

Jashandeep Kaur

## Assignment 2 — Applying Object-Oriented Design

This assignment extends the banking classes with an abstract Transaction
class, BankTransferTransaction, CreditCardTransaction, and TransactionStatus.

Bank transfers charge the greater of $1.00 or 0.7% of the amount.
Credit card transactions charge 2% of the amount.

Transactions validate account status and available funds before processing.
Credit card transactions also require a nonblank authorization code.

## Setup

Install the email validation dependency:

```bash
python -m pip install email-validator
```

## Unit Tests

Run all tests from the project folder:

```bash
python -m unittest discover -s tests -v
```

The current test suite contains 52 passing tests.
