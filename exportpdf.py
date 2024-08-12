


from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Employee Report', border=0, ln=1, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def generate_pdf(tasks, employee, date_from, date_to ):
    try:
        pdf = PDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)

        # Title
        pdf.set_font("Arial", 'B', size=14)
        pdf.cell(0, 10, f"Employee Report - {date_from} to {date_to}", ln=True, align="C")
        pdf.ln(10)

        # Employee Details page left
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"Employee Name: {employee.name}", ln=True)
        pdf.cell(0, 10, f"Employee ID: {employee.employee_id}", ln=True)
        pdf.ln(10)

        # Table Header
        pdf.set_font("Arial", 'B', size=10)
        column_widths = [10, 65, 20, 20, 40, 30] 
        headers = ["S.No", "Task Description", "Product", "Status", "Remarks", "Task ID"]

        for width, header in zip(column_widths, headers):
            pdf.cell(width, 10, header, border=1, align='C')
        pdf.ln()

        # Table Content
        pdf.set_font("Arial", size=10)
        for idx, task in enumerate(tasks, 1):
            pdf.cell(column_widths[0], 10, str(idx), border=1, align='C')
            pdf.cell(column_widths[1], 10, task.task_description[:50], border=1)  # TIN
            pdf.cell(column_widths[2], 10, task.product, border=1, align='C')
            pdf.cell(column_widths[3], 10, task.status, border=1, align='C')
            pdf.cell(column_widths[4], 10, task.remarks[:30], border=1)  # Truncate
            pdf.cell(column_widths[5], 10, task.clickup_matis_id, border=1, align='C')
            pdf.ln()

        # Total Number of Tasks
        pdf.ln(10)
        pdf.set_font("Arial", 'B', size=12)
        pdf.cell(0, 10, f"Total Number of Tasks: {len(tasks)}", ln=True)

        #the directory where the PDF will be saved
        output_dir = os.path.join(os.getcwd(), 'pdf_reports')
        os.makedirs(output_dir, exist_ok=True)

        # Save the PDF
        filename = f"report_{employee.employee_id}_{date_from}-to{date_to}.pdf"
        filepath = os.path.join(output_dir, filename)
        pdf.output(filepath)

        if not os.path.isfile(filepath):
            raise Exception("PDF file was not created.")

        return filepath
    except Exception as e:
        print(f"An error occurred: {e}")
        raise