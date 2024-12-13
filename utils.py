# utils.py

def clean_column_names(fieldnames):
    """Helper function to clean column names by stripping extra spaces."""
    return [field.strip() for field in fieldnames]
