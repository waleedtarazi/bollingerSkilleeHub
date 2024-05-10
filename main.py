from io import BytesIO, StringIO
from typing import Annotated
from fastapi import FastAPI, File, HTTPException, UploadFile
import pandas as pd

from bollinger_helper import pre_processing_data


from fastapi import FastAPI

description = """
SkileeHub's BollingerBands API helps you do awesome tranding. 🤑

## uploadFile
You can do:
* **Upload csv & xlsx**.
* **attach link for your stock data** (_not implemented_).
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
        return True,"",df
    else:
        return False, column,df
        return False, column,df
    

@app.get("/")
async def home():
    return {"message":"Add  **/docs**  to use the SwaggerUI"}
@app.get("/")
async def home():
    return {"message":"Add  **/docs**  to use the SwaggerUI"}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    found,not_found,data = read_csv_file(file)
    found,not_found,data = read_csv_file(file)
    if(found):
        date = pre_processing_data(data)
        print(data.head())
        date = pre_processing_data(data)
        print(data.head())
        return {"file_name" : file.filename}
    else:
        raise HTTPException(status_code=403,
                            detail=f"the column -> {not_found} <- is not found in the data you provided") 
    


