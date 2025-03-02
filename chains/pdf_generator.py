from fpdf import FPDF
import pandas as pd
from langchain_core.runnables import RunnableLambda

class PDF(FPDF):
    def __init__(self, title, *args, **kwargs):
        self.report_title = title
        super().__init__(*args, **kwargs)

    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, self.report_title, 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def df_to_pdf(df: pd.DataFrame, title: str, output_filename: str):
    pdf = PDF(title, orientation='L', format='A4')
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()
    pdf.set_font("Arial", size=8)
    col_width_overrides = {
        "Timestamp": 60,
        "area_co": 60,
        "Staff": 60,
        "Name": 80,
        "Customer_Name" : 60
    }
    col_widths = []
    for col in df.columns:
        if col in col_width_overrides:
            col_widths.append(col_width_overrides[col])
        else:
            base_width = pdf.get_string_width(str(col)) + 10
            col_widths.append(base_width)
    page_width = pdf.w - 2 * pdf.l_margin
    total_width = sum(col_widths)
    if total_width > page_width:
        factor = page_width / total_width
        col_widths = [w * factor for w in col_widths]
    pdf.set_font("Arial", "B", 8)
    for i, col in enumerate(df.columns):
        pdf.cell(col_widths[i], 10, str(col), border=1, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=8)
    for idx, row in df.iterrows():
        for i, col in enumerate(df.columns):
            cell_text = str(row[col])
            pdf.cell(col_widths[i], 10, cell_text, border=1)
        pdf.ln(10)
    pdf.output(output_filename)

def generate_pdf_from_output(output: dict) -> str:
    output_pdf = "sales_report_landscape.pdf"
    title = output.get("title", "Sales Report")
    df = output.get("df")
    df_to_pdf(df, title, output_pdf)
    return output_pdf

pdf_generation_chain = RunnableLambda(func=generate_pdf_from_output)
