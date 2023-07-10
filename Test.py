# importing pandas
import pandas as pd
  
# creating dataframe
df = pd.DataFrame({'Product' : ['Carrots', 'Broccoli', 'Banana', 'Banana',
                                'Beans', 'Orange', 'Broccoli', 'Banana'],
                   'Category' : ['Vegetable', 'Vegetable', 'Fruit', 'Fruit',
                                 'Vegetable', 'Fruit', 'Vegetable', 'Fruit'],
                   'Quantity' : [8, 5, 3, 4, 5, 9, 11, 8],
                   'Amount' : [270, 239, 617, 384, 626, 610, 62, 90]})



## Below Code uses the file() in the Downloads folder 
# importing google libraries to connect python to gsheet
import gspread
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name(
         'C:\\Users\\rahul.vimal\\Documents\\Personal\\My Practise Code (Python & R)\\Google API Keys (CAN ACE Project).json', scope)


gc = gspread.authorize(credentials)

## Given below is the Sheet name and Worksheet name. Make sure that the permission of the google sheet is given to the required gmail

gc = gspread.authorize(credentials)
yearly_data = gc.open("Temp").worksheet("Sheet1")

## Below command uploads the output stored in the dataframe df
## make sure that code of the google sheet link in provided in the below function along with the sheet name
d2g.upload(df, "1ospfeZS1VVtflDWda4weDgtyRJACKnxak8i_Pf8jWXA", "Sheet1", credentials=credentials, row_names=False)				   