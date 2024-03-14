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
    print("="*50)
    print(f"API_GOOGLE_SHEET_UPDATE_LINES")
    print("="*50)
    print(f"{hour.current_time} Début de l'execution de la fonction")
    

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

    
    request = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption='RAW',
        body={'values': data}
    )

    response = request.execute()

    print(f"""
          Id Gsheet:\t\t{response['spreadsheetId']}
          Range:\t\t{response['updatedRange']}
          Row updated:\t\t{response['updatedRows']}
          Column updated:\t{response['updatedColumns']}
          Cells updated:\t{response['updatedCells']}
        """)
    print(f"{hour.current_time} Fin de l'execution de la fonction")