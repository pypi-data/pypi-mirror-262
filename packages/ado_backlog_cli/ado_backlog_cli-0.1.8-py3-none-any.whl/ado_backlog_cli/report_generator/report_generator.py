# report_generator.py
class BaseReportGenerator:
    def generate_report(self, data):
        raise NotImplementedError("Subclasses must implement this method.")
    
    def save_to_file(self, file_path):
        raise NotImplementedError("Subclasses must implement this method.")

# Example Implementation
# from .report_generator.table_report import TableReport
# from .report_generator.csv_report import CSVReport
# from .work_item_utils import get_work_items_without_target_date

# # Assuming you have a list of work items fetched and stored in `work_items`
# formatted_data = format_work_items_for_report(work_items)  # You'd implement this

# # To generate a table report
# table_report = TableReport()
# table_report.generate_report(formatted_data)
# table_report.save_to_file("path/to/save/table_report.txt")

# # To generate a CSV report
# csv_report = CSVReport()
# csv_report.generate_report(formatted_data)
# csv_report.save_to_file("path/to/save/csv_report.csv")
