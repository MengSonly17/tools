from flask import Flask, render_template, request, redirect, flash
import csv
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret123'  # Needed for flashing messages

REPORT_FILE = 'reports.csv'


@app.route('/', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        fb_link = request.form['fb_link'].strip()
        reason = request.form['reason']
        details = request.form['details'].strip()

        if not fb_link:
            flash("Facebook link is required.", "danger")
            return redirect('/')

        file_exists = os.path.isfile(REPORT_FILE)
        with open(REPORT_FILE, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(['Timestamp', 'Facebook Link', 'Reason', 'Details'])
            writer.writerow([datetime.now().isoformat(), fb_link, reason, details])

        flash("Report submitted successfully!", "success")
        return redirect('/')

    reasons = ["Spam", "Harassment", "Hate Speech", "Misinformation", "Scam", "Other"]
    return render_template('report.html', reasons=reasons)


if __name__ == '__main__':
    app.run(debug=True)

