
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.errors import HttpError

def API_GOOGLE_SHEET_UPDATE_LINES(account_google_secret, google_sheet_id, sheet_name, df):
    """
    Fonction permettant de mettre à jour un onglet Google Sheet avec un dataframe
    :param account_google_secret: str, chemin vers le fichier secret de l'API Google
    :param google_sheet_id: str, identifiant de la feuille Google
    :param sheet_name: str, nom de l'onglet à mettre à jour
    :param df: DataFrame, dataframe à mettre à jour
    :return: None
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
    range=f'{sheet_name}!A1:ZZ',
)
    clear_response = clear_request.execute()

    # Conversion du dataframe en liste de listes
    header = list(df.columns)
    data = df.values.tolist()
    data.insert(0, header)

    range_name = f'{sheet_name}!A1:{chr(ord("A") + df.shape[1] - 1)}{df.shape[0] + 1}'

    
    request = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption='RAW',
        body={'values': data}
    )

    response = request.execute()

    print('Execution OK')