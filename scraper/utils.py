import pandas as pd
import matplotlib.pyplot as plt
import logging
import csv
import smtplib
import os
from datetime import datetime
from email.message import EmailMessage

# Configure logging to English
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_timestamped_filename(base_name: str, extension: str) -> str:
    """Generates a filename with a current timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    return f"{base_name}_{timestamp}.{extension}"

def save_to_csv(data: list, filename: str) -> None:
    """Saves the list of dictionaries to a CSV file."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Business Name", "Phone", "Website"])
        writer.writeheader()
        writer.writerows(data)
    logging.info(f"Successfully saved {len(data)} leads to {filename}")

def generate_visual_report(csv_filename: str, image_filename: str) -> None:
    """Reads CSV and generates a website presence chart."""
    try:
        df = pd.read_csv(csv_filename)
        df['Has Website'] = df['Website'].apply(lambda x: 'No' if x == 'N/A' else 'Yes')
        stats = df['Has Website'].value_counts()
        
        plt.figure(figsize=(8, 5))
        stats.plot(kind='bar', color=['#4CAF50', '#F44336'])
        plt.title('Business Analytics: Website Presence')
        plt.xlabel('Has Website')
        plt.ylabel('Total Count')
        plt.xticks(rotation=0)
        plt.tight_layout()
        plt.savefig(image_filename)
        logging.info(f"Visual report generated: {image_filename}")
    except Exception as e:
        logging.error(f"Failed to generate report: {e}")

def send_email_report(csv_path: str, image_path: str, sender: str, receiver: str) -> None:
    """Sends the report via Gmail SMTP using environment-based credentials."""
    app_password = os.environ.get("EMAIL_APP_PASSWORD")
    if not app_password:
        logging.error("Email delivery aborted: EMAIL_APP_PASSWORD environment variable not set.")
        return

    msg = EmailMessage()
    msg['Subject'] = f"Lead Gen Report - {datetime.now().strftime('%Y-%m-%d')}"
    msg['From'] = sender
    msg['To'] = receiver
    msg.set_content("Data extraction pipeline completed. Please find attachments below.")

    for path in [csv_path, image_path]:
        with open(path, 'rb') as f:
            file_data = f.read()
            msg.add_attachment(file_data, 
                               maintype='application' if path.endswith('.csv') else 'image', 
                               subtype='octet-stream' if path.endswith('.csv') else 'png', 
                               filename=os.path.basename(path))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender, app_password)
        smtp.send_message(msg)
    logging.info("Report dispatched successfully.")