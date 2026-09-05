# ReconcileAI 🧠💰

An intelligent reconciliation engine that automates bank statement matching using advanced fuzzy-matching algorithms, confidence scoring, and anomaly detection.

## The Problem
Finance teams spend hours manually matching bank statements with payment gateway transactions. Manual reconciliation has a 5-10% error rate, misses critical anomalies (fraud, duplicates), and delays financial reporting.

## The Solution
ReconcileAI ingests bank statements and payment gateway records (e.g., Razorpay), applying multi-factor weighted scoring to map transactions. 
- **Automated Matching:** Evaluates amount, date proximity, and description similarity.
- **Confidence Scoring:** Scores matches 0-100. (>75 Auto-approved, 50-75 Flagged for review, <50 Unmatched).
- **Anomaly Detection:** Flags duplicates, timing gaps, and unusual amounts.
- **Instant Reporting:** Generates professional HTML audit reports in seconds.

## How to Run Locally
1. Install Python 3.8+
2. Install dependencies: `pip install -r requirements.txt`
3. Place your `bank_statement.csv` and `razorpay_transactions.csv` in the folder.
4. Run the engine: `python app.py`
5. Open `reconciliation_report.html` in your browser to view results.
