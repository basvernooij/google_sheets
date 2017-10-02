import httplib2
import pandas as pd
import apiclient
import oauth2client
from oauth2client.file import Storage
from os.path import expanduser

class GoogleSheet():
    """
    Class for initiating GoogleSheets API
    """
    def __init__(self):

        credential_path = expanduser("~") + "/.credentials/sheets_credentials_miamed.json"
        store = Storage(credential_path)
        self.credentials = store.get()
        self.service = self._initiate_api_connection()

    def _initiate_api_connection(self):
        """
        Provides the according service to work with Google Sheets

        :return: service object
        """
        http = self.credentials.authorize(httplib2.Http())

        discovery_url = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
        return apiclient.discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discovery_url)

    def get_values_of_sheet(self, spreadsheet_id, data_range):
        """
        Downloads data from a google work sheet and returns it as pandas dataframe

        :param spreadsheet_id: str
        :param data_range: str

        :return: dataframe
        """
        # Fetch data from Drive
        result = self.service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=data_range).execute()

        # Load into DataFrame
        header = result["values"][0]
        data = result["values"][1:]

        # exception handling if last column is empty (since data and header have different format then...)
        for line in data:
            for missing_item in range(len(header) - len(line)):
                line.append(pd.np.nan)

        return pd.DataFrame(data, columns=header)

    def write_dataframe_to_sheet(self, spreadsheet_id, dataframe, sheet_name, clear_sheet=False):
        if clear_sheet:
            self.clear_sheet(spreadsheet_id, sheet_name)

        # grab all values
        data = dataframe.values.tolist()

        # grab header
        header = dataframe.columns.tolist()

        # set header as first item in list of lists
        data.insert(0, header)

        body = {
            'values': data
        }

        self.service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=sheet_name,
            valueInputOption="USER_ENTERED", body=body).execute()

    def clear_sheet(self, spreadsheet_id, sheet_name):
        pass

