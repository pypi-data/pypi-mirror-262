# table_report.py
from .report_generator import BaseReportGenerator
from prettytable import PrettyTable

from prettytable import PrettyTable

class TableReportGenerator(BaseReportGenerator):
    def __init__(self, fields, centered_columns=None):
        self.fields = fields
        # A list of columns to center-align. This parameter is optional.
        self.centered_columns = centered_columns if centered_columns else []

    def generate_report(self, data):
        table = PrettyTable()
        table.field_names = self.fields

        for item in data:
            if isinstance(item, dict):
                row = [str(item.get(field, 'N/A'))[:80] for field in self.fields]
            else:
                row = [str(getattr(item, 'fields', {}).get(field, 'N/A'))[:20] for field in self.fields]
            table.add_row(row)

        # Set default alignment for all columns to left
        table.align = 'l'

        # Center-align specific columns if specified
        for col in self.centered_columns:
            if col in self.fields:
                table.align[col] = 'c'

        return table.get_string()

    def save_report(self, report, file_path):
        with open(file_path, 'w') as f:
            f.write(report)
