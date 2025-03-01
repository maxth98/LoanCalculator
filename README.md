# LoanCalculator
Annuity based loan calculator

## Installation

- Download Python 3.12 from https://www.python.org/downloads/release/python-3120/
- Install Poetry by using the command line: ``(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -``
- Install the dependecies by running ``poetry install`` in the working directory
- Run ``poetry run python serve.py`` to start Flask
- Execute ``http://127.0.0.1:5000/calc?principal=200000&duration=200&nom_intr=2.0&rdmp_intr=3.0&repay_amt=5000&repay_period=0`` in your Browser to retrieve an example repayment plan