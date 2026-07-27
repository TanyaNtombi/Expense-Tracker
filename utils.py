import pandas as pd
import io


def expenses_to_dataframe(expenses):
    """
    Convert a list of expenses into a pandas DataFrame.
    """
    return pd.DataFrame(
        expenses,
        columns=[
            "Amount (R)",
            "Category",
            "Date",
            "Description"
        ]
    )


def create_csv(df):
    """
    Convert a DataFrame into CSV format.
    """
    csv_buffer = io.StringIO()

    df.to_csv(
        csv_buffer,
        index=False
    )

    return csv_buffer.getvalue()


def format_currency(amount):
    """
    Format currency with commas and two decimal places.
    """
    return f"R {amount:,.2f}"