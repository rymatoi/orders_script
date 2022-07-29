import apiclient
import httplib2
from oauth2client.service_account import ServiceAccountCredentials

# Файл, полученный в Google Developer Console
CREDENTIALS_FILE = 'credentials.json'
# ID Google Sheets документа
spreadsheet_id = '1YQ1DBuI5GWDq7r6tuKJ6DEB1yKHku1N4rWKvNYZgwCU'

# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)


def get_values() -> tuple:
    """
    Получает текущее содержимое файла с заказами
    :return: кортежи со значениями
    """
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='A2:D',
        majorDimension='ROWS'
    ).execute()
    return tuple(tuple(val) for val in result['values'])
