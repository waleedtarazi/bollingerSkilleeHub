from io import BytesIO, StringIO
import json
from typing import Annotated
from fastapi import BackgroundTasks, FastAPI, File, HTTPException, Response, UploadFile
import pandas as pd

from bollinger_helper import *

from fastapi import FastAPI

description = """
SkileeHub's BollingerBands API helps you do awesome tranding. 🤑

## You can do:
* **Upload csv & xlsx**. (__implemented but currently under constructions)
* **attach link for your stock data** (_not implemented_).
* **Yahoo data choosing**  Yahoo stock data like: AAPL,TATASTEEL.NS ! 
"""

app = FastAPI(
    title="skilleeBolinger",
    description=description,
    summary="invest on the right time 💹",
    version="0.1.3",
    contact={
        "name": "Waleed Al-Tarazi",
        "url": "https://www.linkedin.com/in/waleed-al-tarazi/",
        "email": "waleedaltarazy@gmail.com",
    },
)

def check_columns(df):
    """_summary_\n
    The  function checks whether the Data contains some spicifc column
    like: [close, open, high, low]
    
    Args:
        df (pandas dataframe)

    Returns:
        bool: contains needed columns  or not 
        str: the name of the not founded column
    """
    df_columns = [column for column in df.columns.tolist()]
    needed_params = ['Close', 'Open', 'High', 'Low']
    for column in needed_params:
        if column in df_columns:
            continue
        else:
            return False, column
    return True,""

def read_csv_file(file: UploadFile):
    """_summary_\n
    read the file as csv pandas data frame, check the columns using check_cloumns(pd) function
    Args:
        file (UploadFile): the file from the server

    Returns:
        bool, str: 
    """
    df = pd.read_csv(file.file)
    file.file.close()
    found,column = check_columns(df)
    if(found):
        return True,"",df
    else:
        return False, column,df
    

@app.get("/")
async def home():
    return {"message":"Add  **/docs**  to use the SwaggerUI"}


@app.post("/uploadfile/",description="currently will accept files, but not processing correctly ")
async def create_upload_file(file: UploadFile):
    found,not_found,data = read_csv_file(file)
    if(found):
        data = make_analysis("file")
        if data:
            buy_points = data[data['buy'].notnull()]
            sell_points = data[data['sell'].notnull()]
            return {"file_name" : file.filename,
                    "buy_points" : buy_points.to_json(orient='records',),
                    "sell_points" :sell_points.to_json(orient='records') }
    else:
        raise HTTPException(status_code=403,
                            detail=f"the column -> {not_found} <- is not found in the data you provided") 
        
    
@app.get('/analys/Yahoo-data/')
async def analys_yahoo(data_symbol: data_symbol):
    data = make_analysis(data_symbol.value)
    buy_points = data[data['buy'].notnull()]
    sell_points = data[data['sell'].notnull()]
    return {"data choosen" : data_symbol.value,
            "buy_points" : buy_points.to_json(orient='records',),
            "sell_points" :sell_points.to_json(orient='records') }