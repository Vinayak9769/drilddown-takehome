import pandas as pd
from langchain_core.runnables import RunnableLambda

def df_to_html(df: pd.DataFrame, title: str, output_filename: str):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                color: #333;
            }}
            h1 {{
                text-align: center;
                color: #2c3e50;
                padding-bottom: 10px;
                border-bottom: 1px solid #ddd;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th, td {{
                padding: 8px 12px;
                border: 1px solid #ddd;
                text-align: left;
            }}
            th {{
                background-color: #3498db;
                color: white;
            }}
            tr:nth-child(even) {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        {df.to_html(index=False)}
    </body>
    </html>
    """    
    with open(output_filename, 'w') as f:
        f.write(html_content)
    
    return output_filename

def generate_html_from_output(output: dict) -> str:
    output_html = "sales_report.html"
    title = output.get("title", "Sales Report")
    df = output.get("df")
    html_path = df_to_html(df, title, output_html)
    return html_path

html_generation_chain = RunnableLambda(func=generate_html_from_output)