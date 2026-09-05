import pandas as pd
from datetime import datetime, timedelta
import random

def generate_sample_files():
    # Fake Bank Statement
    bank_data = {
        'Date': ['2023-08-15', '2023-08-16', '2023-08-17', '2023-08-18', '2023-08-19'],
        'Description': ['Razorpay Settlement', 'Payment from Acme Corp', 'Razorpay Payout', 'Refund to John Doe', 'Wire Transfer XYZ'],
        'Amount': [10000.00, 500.00, 2500.00, -150.00, 5000.00]
    }
    pd.DataFrame(bank_data).to_csv('bank_statement.csv', index=False)

    # Fake Razorpay Transactions (Notice slight differences in dates/names to test AI)
    razorpay_data = {
        'Date': ['2023-08-15', '2023-08-15', '2023-08-17', '2023-08-18', '2023-08-15'],
        'Description': ['Razorpay Settlmnt', 'Acme Corporation', 'Razorpay Payot', 'Refund J. Doe', 'Duplicate Test'],
        'Amount': [10000.00, 500.00, 2500.00, -150.00, 10000.00],
        'Payment_ID': ['pay_123', 'pay_124', 'pay_125', 'pay_126', 'pay_127']
    }
    pd.DataFrame(razorpay_data).to_csv('razorpay_transactions.csv', index=False)
    print("✅ Sample data files created successfully.")

if __name__ == "__main__":
    generate_sample_files()
