from io import BytesIO, StringIO
from typing import Annotated
from fastapi import FastAPI, File, HTTPException, UploadFile
import pandas as pd


app = FastAPI()

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
    needed_params = ['close', 'open', 'high', 'low']
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
        return True,""
    else:
        return False, column
    

@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    found,not_found = read_csv_file(file)
    if(found):
        return {"file_name" : file.filename}
    else:
        raise HTTPException(status_code=403,
                            detail=f"the column -> {not_found} <- is not found in the data you provided") 
    


