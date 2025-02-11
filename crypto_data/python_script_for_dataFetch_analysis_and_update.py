import time
import pandas as pd
from data_fetcher import fetch_crypto_data
from data_analyzer import analyze_data
import dropbox
from io import BytesIO
import os
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
load_dotenv()

dropbox_access_token = os.getenv('DROPBOX_ACCESS_TOKEN')


dbx = dropbox.Dropbox(dropbox_access_token)

def upload_to_dropbox(file_content, file_path):
    try:
        # Upload file to Dropbox (overwrite if it exists)
        dbx.files_upload(file_content, file_path, mode=dropbox.files.WriteMode.overwrite)
        print(f"Successfully uploaded {file_path} to Dropbox.")
    except dropbox.exceptions.ApiError as e:
        print(f"Error uploading file: {e}")


def generate_pdf_report(analysis, timestamp):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    styles = getSampleStyleSheet()
    custom_style = ParagraphStyle(
        'CustomStyle',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
    )
    
    elements = []
    
    # Title
    elements.append(Paragraph("Cryptocurrency Analysis Report", styles['Title']))
    elements.append(Spacer(1, 12))
    
    # Timestamp
    elements.append(Paragraph(f"Report generated at: {timestamp}", styles['Italic']))
    elements.append(Spacer(1, 24))
    
    # Top 5 by Market Cap
    elements.append(Paragraph("Top 5 Cryptocurrencies by Market Cap:", styles['Heading2']))
    top5_data = [["Name", "Symbol", "Market Cap"]]
    for item in analysis["top_5_by_market_cap"]:
        top5_data.append([item['name'], item['symbol'], f"${item['market_cap']:,.2f}"])
    top5_table = Table(top5_data)
    top5_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('GRID', (0,0), (-1,-1), 1, colors.grey),
    ]))
    elements.append(top5_table)
    elements.append(Spacer(1, 24))
    
    # Average Price
    elements.append(Paragraph(f"Average Price of Top 50 Cryptocurrencies: ${analysis['average_price_top_50']:,.2f}", styles['Heading2']))
    elements.append(Spacer(1, 12))
    
    # 24h Changes
    elements.append(Paragraph("24-Hour Price Changes:", styles['Heading2']))
    changes_data = [
        ["Highest Gainer", analysis['highest_24h_change']['name'], f"{analysis['highest_24h_change']['change']:.2f}%"],
        ["Biggest Loser", analysis['lowest_24h_change']['name'], f"{analysis['lowest_24h_change']['change']:.2f}%"]
    ]
    changes_table = Table(changes_data, colWidths=[150, 200, 100])
    changes_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTSIZE', (0,0), (-1,-1), 12),
        ('BOX', (0,0), (-1,-1), 1, colors.black),
    ]))
    elements.append(changes_table)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer

def update_excel_files():
    result = fetch_crypto_data()
    if not result:
        print("Failed to fetch results.")
        return

    data = result[0]
    data_timestamp = result[1]

    if data.empty:
        print("Data is empty")
        return

    analysis = analyze_data(data)  # Move this line up before generating the PDF

    with BytesIO() as data_buffer:
        with pd.ExcelWriter(data_buffer, engine='openpyxl', mode='w') as writer:
            pd.DataFrame(data).to_excel(writer, index=False)
            writer.sheets['Sheet1'].cell(row=len(data) + 2, column=1, value=f"Last updated (IST): {data_timestamp}")
        data_buffer.seek(0)
        upload_to_dropbox(data_buffer.read(), '/crypto_data.xlsx')

    print(f"Updated: crypto_data.xlsx on Dropbox")

    pdf_buffer = generate_pdf_report(analysis, data_timestamp)  # Now `analysis` is properly initialized
    upload_to_dropbox(pdf_buffer.read(), '/crypto_analysis_report.pdf')
    print(f"Updated: crypto_analysis_report.pdf on Dropbox")

    print("All files updated successfully.")

    with BytesIO() as analysis_buffer:
        with pd.ExcelWriter(analysis_buffer, engine='openpyxl', mode='w') as writer:
            pd.DataFrame(analysis["top_5_by_market_cap"]).to_excel(writer, sheet_name="Top 5 by Market Cap", index=False)
            pd.DataFrame([{"Average Price": analysis["average_price_top_50"]}]).to_excel(writer, sheet_name="Average Price", index=False)

            highest_24h_change = analysis["highest_24h_change"]
            if isinstance(highest_24h_change, dict):
                highest_24h_change = [highest_24h_change]

            pd.DataFrame(highest_24h_change).to_excel(writer, sheet_name="Highest Change", index=False)
            lowest_24h_change = analysis["lowest_24h_change"]
            if isinstance(lowest_24h_change, dict):
                lowest_24h_change = [lowest_24h_change]

            pd.DataFrame(lowest_24h_change).to_excel(writer, sheet_name="Lowest Change", index=False)

            writer.sheets['Top 5 by Market Cap'].cell(row=len(analysis["top_5_by_market_cap"]) + 2, column=1, value=f"Last updated (IST): {data_timestamp}")
            writer.sheets['Average Price'].cell(row=5, column=2, value=f"Last updated (IST): {data_timestamp}")
            writer.sheets['Highest Change'].cell(row=5, column=2, value=f"Last updated (IST): {data_timestamp}")
            writer.sheets['Lowest Change'].cell(row=5, column=2, value=f"Last updated (IST): {data_timestamp}")
        analysis_buffer.seek(0)
        upload_to_dropbox(analysis_buffer.read(), '/crypto_analysis.xlsx')

    print(f"Updated: crypto_analysis.xlsx on Dropbox")
    with BytesIO() as analysis_buffer:
        with pd.ExcelWriter(analysis_buffer, engine='openpyxl', mode='w') as writer:
            pd.DataFrame(analysis["top_5_by_market_cap"]).to_excel(writer, sheet_name="Top 5 by Market Cap", index=False)
            pd.DataFrame([{"Average Price": analysis["average_price_top_50"]}]).to_excel(writer, sheet_name="Average Price", index=False)
            
            highest_24h_change = analysis["highest_24h_change"]
            if isinstance(highest_24h_change, dict):
                highest_24h_change = [highest_24h_change]

            pd.DataFrame(highest_24h_change).to_excel(writer, sheet_name="Highest Change", index=False)           
            lowest_24h_change = analysis["lowest_24h_change"]
            if isinstance(lowest_24h_change, dict):
                lowest_24h_change = [lowest_24h_change]

            pd.DataFrame(lowest_24h_change).to_excel(writer, sheet_name="Lowest Change", index=False)           

            writer.sheets['Top 5 by Market Cap'].cell(row=len(analysis["top_5_by_market_cap"]) + 2, column=1, value=f"Last updated (IST): {data_timestamp}")
            writer.sheets['Average Price'].cell(row=5, column=2, value=f"Last updated (IST): {data_timestamp}")
            writer.sheets['Highest Change'].cell(row=5, column=2, value=f"Last updated (IST): {data_timestamp}")
            writer.sheets['Lowest Change'].cell(row=5, column=2, value=f"Last updated (IST): {data_timestamp}")
        analysis_buffer.seek(0)
        upload_to_dropbox(analysis_buffer.read(), '/crypto_analysis.xlsx')

    print(f"Updated: crypto_analysis.xlsx on Dropbox")

if __name__ == '__main__':
    print("Starting updater script...")
    while True:
        update_excel_files()
        print("Waiting 5 minutes before next update...")
        time.sleep(300)