import pandas as pd
import matplotlib.pyplot as plt
import logging
import csv

# Configure logging format and level for the entire application
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def save_to_csv(data: list, filename: str) -> None:
    """
    Writes the extracted data to a CSV file.
    """
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Business Name", "Phone", "Website"])
        writer.writeheader()
        writer.writerows(data)
    logging.info(f"Successfully saved {len(data)} leads to {filename}")

def generate_visual_report(csv_filename: str) -> None:
    """
    Reads the scraped CSV data and generates a bar chart 
    showing the distribution of businesses with and without websites.
    """
    try:
        df = pd.read_csv(csv_filename)
        
        # Analyze website presence based on 'N/A' values
        df['Has Website'] = df['Website'].apply(lambda x: 'No' if x == 'N/A' else 'Yes')
        stats = df['Has Website'].value_counts()
        
        # Setup plot dimensions and styles
        plt.figure(figsize=(8, 5))
        stats.plot(kind='bar', color=['#4CAF50', '#F44336'])
        
        # Add labels and title
        plt.title('Business Analytics: Website Presence')
        plt.xlabel('Has Website')
        plt.ylabel('Total Count')
        plt.xticks(rotation=0)
        plt.tight_layout()
        
        # Save the generated chart to disk
        report_name = "report_chart.png"
        plt.savefig(report_name)
        logging.info(f"Visual report generated and saved as {report_name}")
        
    except Exception as e:
        logging.error(f"Failed to generate report: {e}")