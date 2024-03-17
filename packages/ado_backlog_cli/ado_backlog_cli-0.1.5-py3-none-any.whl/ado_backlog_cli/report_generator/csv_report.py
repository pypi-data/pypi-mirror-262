from .report_generator import BaseReportGenerator
from prettytable import PrettyTable

class CSVReportGenerator(BaseReportGenerator):
    def __init__(self, fields):
        self.fields = fields
    
    def generate_report(self, work_items):
        rows = []
        for item in work_items:
            row = [getattr(item, field, 'N/A') for field in self.fields]
            rows.append(row)
        return rows
    
    def save_report(self, report_rows, file_path):
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(self.fields)  # Writing the header
            for row in report_rows:
                writer.writerow(row)
