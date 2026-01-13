import pandas as pd


def load_sheet(conn, spreadsheet_url: str, worksheet: str):
    return conn.read(
        spreadsheet=spreadsheet_url,
        worksheet=worksheet,
        ttl=0
    )


def save_sheet(conn, spreadsheet_url: str, worksheet: str, df: pd.DataFrame):
    conn.update(
        spreadsheet=spreadsheet_url,
        worksheet=worksheet,
        data=df
    )
