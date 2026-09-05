import pandas as pd
from thefuzz import fuzz
from datetime import datetime
import os

class ReconcileAI:
    def __init__(self, bank_file, razorpay_file):
        self.bank_df = pd.read_csv(bank_file)
        self.razorpay_df = pd.read_csv(razorpay_file)
        self.results = []
        self.anomalies = []

        # Convert dates to datetime objects
        self.bank_df['Date'] = pd.to_datetime(self.bank_df['Date'])
        self.razorpay_df['Date'] = pd.to_datetime(self.razorpay_df['Date'])

    def calculate_confidence_score(self, bank_row, rp_row):
        score = 0
        
        # 1. Amount Matching (40 points)
        if abs(bank_row['Amount'] - rp_row['Amount']) < 1.0:
            score += 40
        elif abs(bank_row['Amount'] - rp_row['Amount']) < 50.0:
            score += 20 # Tolerance for fees
            
        # 2. Date Proximity (30 points) - Understanding 1-3 day settlement delays
        days_diff = abs((bank_row['Date'] - rp_row['Date']).days)
        if days_diff == 0:
            score += 30
        elif days_diff <= 3:
            score += 20
        elif days_diff <= 7:
            score += 10
            
        # 3. Description Fuzzy Matching (30 points)
        text_similarity = fuzz.ratio(str(bank_row['Description']).lower(), str(rp_row['Description']).lower())
        score += int((text_similarity / 100) * 30)
        
        return score

    def detect_anomalies(self):
        # Detect Duplicates
        duplicates = self.razorpay_df[self.razorpay_df.duplicated(subset=['Amount'], keep=False)]
        for _, row in duplicates.iterrows():
            self.anomalies.append(f"Potential Duplicate: Amount {row['Amount']} on {row['Date'].date()}")

    def run_reconciliation(self):
        print("🧠 ReconcileAI is analyzing transactions...")
        self.detect_anomalies()
        
        used_rp_indices = []

        for _, b_row in self.bank_df.iterrows():
            best_match = None
            highest_score = 0

            for idx, r_row in self.razorpay_df.iterrows():
                if idx in used_rp_indices:
                    continue
                
                current_score = self.calculate_confidence_score(b_row, r_row)
                
                if current_score > highest_score:
                    highest_score = current_score
                    best_match = r_row
                    best_idx = idx

            # Categorize based on Confidence Score
            if highest_score >= 75:
                status = "Auto-Approved ✅"
                used_rp_indices.append(best_idx)
            elif highest_score >= 50:
                status = "Needs Review ⚠️"
                used_rp_indices.append(best_idx)
            else:
                status = "Unmatched ❌"
                best_match = None

            self.results.append({
                'Bank_Date': b_row['Date'].date(),
                'Bank_Desc': b_row['Description'],
                'Bank_Amount': b_row['Amount'],
                'Matched_RP_Desc': best_match['Description'] if best_match is not None else "None",
                'Matched_RP_Amount': best_match['Amount'] if best_match is not None else "None",
                'Confidence_Score': highest_score,
                'Status': status
            })

    def generate_report(self):
        results_df = pd.DataFrame(self.results)
        
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>ReconcileAI Audit Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f4f7f6; }}
                h1 {{ color: #2c3e50; }}
                table {{ width: 100%; border-collapse: collapse; background: white; margin-top: 20px; }}
                th, td {{ padding: 12px; border: 1px solid #ddd; text-align: left; }}
                th {{ background-color: #34495e; color: white; }}
                .anomaly {{ color: red; font-weight: bold; }}
                .summary-box {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            </style>
        </head>
        <body>
            <h1>🧠 ReconcileAI - Financial Audit Report</h1>
            <div class="summary-box">
                <h2>Summary Statistics</h2>
                <p>Total Bank Transactions: {len(self.bank_df)}</p>
                <p>Total Razorpay Transactions: {len(self.razorpay_df)}</p>
                <p>Auto-Approved Matches: {len([r for r in self.results if 'Auto-Approved' in r['Status']])}</p>
                <p>Flagged for Review: {len([r for r in self.results if 'Needs Review' in r['Status']])}</p>
                <p>Unmatched: {len([r for r in self.results if 'Unmatched' in r['Status']])}</p>
            </div>

            <h2>⚠️ Detected Anomalies</h2>
            <ul>
                {''.join([f'<li class="anomaly">{a}</li>' for a in self.anomalies]) if self.anomalies else '<li>No anomalies detected.</li>'}
            </ul>

            <h2>📊 Transaction Matching Details</h2>
            {results_df.to_html(index=False)}
            
            <br><br>
            <p><em>Generated by ReconcileAI Engine | Intelligent Fuzzy-Matching & Anomaly Detection</em></p>
        </body>
        </html>
        """
        
        with open("reconciliation_report.html", "w", encoding="utf-8") as f:
            f.write(html_template)
        print("✅ Report generated! Open 'reconciliation_report.html' in your browser.")

if __name__ == "__main__":
    # 1. Generate sample data if it doesn't exist
    if not os.path.exists('bank_statement.csv'):
        import sample_data
        sample_data.generate_sample_files()

    # 2. Run the AI Engine
    engine = ReconcileAI('bank_statement.csv', 'razorpay_transactions.csv')
    engine.run_reconciliation()
    
    # 3. Generate the visual report
    engine.generate_report()
