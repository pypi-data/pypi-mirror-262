from datetime import datetime
from dotenv import load_dotenv
import os 

from rich import print

from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.errors import HttpError

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import header

import smtplib
import json
import requests
import pandas as pd

# from pydrive2.auth import GoogleAuth
# from pydrive2.drive import GoogleDrive
# from pydrive2.files import FileNotUploadedError

from requests_oauthlib import OAuth1

import re

#from PyPDF2 import PdfReader

from google.cloud import bigquery

import time

# from openai import OpenAI
# from openai import OpenAIError

ids_slack = {
    "Claire": {"id":os.getenv("slack_claire_id"), "col":"#FF9F1C"},
    "Alexis": {"id":os.getenv("slack_alexis_id"), "col":"#17C3B2"},
    "Brice":  {"id":os.getenv("slack_brice_id"), "col":"#083D77"},
}

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class hour:
    now = datetime.now()
    current_time = now.strftime("%Y-%M-%d %H:%M:%S")

def computelog(header, msg, footer):
    print("="*50)
    print(f"{header}")
    print("="*50)
    print(f"{hour.current_time} Début de l'execution de la fonction")
    print(f"{msg}")
    print(f"{hour.current_time} {footer}")
     
    
def API_GOOGLE_SHEET_UPDATE_LINES(account_google_secret, google_sheet_id, df, sheet_name="Sheet1", range = "A1:ZZ"):
    """
        Fonction permettant de mettre à jour un onglet Google Sheet avec un dataframe
        Args
            account_google_secret: str, chemin vers le fichier secret de l'API Google
            google_sheet_id: str, identifiant de la feuille Google
            sheet_name: str, nom de l'onglet à mettre à jour. default: "Sheet1"
            range: str, plage de cellules à mettre à jour. default: "A1:ZZ"
            df: DataFrame, dataframe à mettre à jour

        Returns
            None
    """
    

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = account_google_secret
    creds = None
    creds = service_account.Credentials.from_service_account_file(
			SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    
    spreadsheet_id = google_sheet_id
    sheet_name = sheet_name
    
    service = build('sheets', 'v4', credentials=creds)

    clear_request = service.spreadsheets().values().clear(
    spreadsheetId=spreadsheet_id,
    range=f'{sheet_name}!{range}',
)
    clear_response = clear_request.execute()

    # Conversion du dataframe en liste de listes
    header = list(df.columns)
    data = df.values.tolist()
    data.insert(0, header)

    #range_name = f'{sheet_name}!A1:{chr(ord("A") + df.shape[1] - 1)}{df.shape[0] + 1}'
    range_name = f'{sheet_name}!{range}'

    try:
        request = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body={'values': data}
        )

        response = request.execute()

        header = "API_GOOGLE_SHEET_UPDATE_LINES"
        msg = f"""
            Id Gsheet:\t\t{response['spreadsheetId']}
            Range:\t\t{response['updatedRange']}
            Row updated:\t\t{response['updatedRows']}
            Column updated:\t{response['updatedColumns']}
            Cells updated:\t{response['updatedCells']}
                """
        footer = "Fin de l'execution de la fonction"
        computelog(header, msg, footer)
    except HttpError as error:
        print(f"An error occurred: {error}")

def API_GOOGLE_SHEET_GET_FILE (account_google_secret, google_sheet_id, range):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = account_google_secret
    creds = None
    creds = service_account.Credentials.from_service_account_file(
			SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    SAMPLE_SPREADSHEET_ID = google_sheet_id
    SAMPLE_RANGE_NAME = range
    try:
        service = build('sheets', 'v4', credentials=creds)
		# Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
								range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])
        print(f"{datetime.now()}\tExecution OK !")
        header_log = "API_GOOGLE_SHEET_GET_FILE"
        msg_log = f"{datetime.now()}\tExecution OK !\n"
        footer_log = "Fin de l'execution de la fonction"
        computelog(header_log, msg_log, footer_log)
        return values
    except HttpError as error:
        print(f"An error occurred: {error}")
    

def SQL_query(account_bigquery_secret, sql_path_file, last_execution_date = ""):
    """Execute a BigQuery SQL query and return the result as a DataFrame.
    :sql_path_file: The name of the SQL file to be executed.
    Returns:
        :df: A DataFrame containing the result of the SQL query.
    """
    sql_path = f"{sql_path_file}"
    with open(sql_path, "r") as file:
        sql = file.read()
    if last_execution_date != "":
        sql = sql.replace("WHERE date(updated_at) > DATE_SUB(CURRENT_DATE, INTERVAL 1 DAY)", f"WHERE date(updated_at) > DATE_SUB(\"{last_execution_date}\", INTERVAL 1 DAY)")
    
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = account_bigquery_secret
    client = bigquery.Client()
    df = client.query(sql).to_dataframe()
    return df