import pandas as pd
from io import StringIO, BytesIO
from azure.storage.blob import BlockBlobService

def get_data_from_azure_blob(account_name, account_key, container_name, file_name):
    byte_stream = BytesIO()
    blob_service = BlockBlobService(account_name=account_name,
                                   account_key=account_key)
    blob_service.get_blob_to_stream(container_name=container_name, 
                                   blob_name=file_name, 
                                   stream=byte_stream)
    byte_stream.seek(0)
    df=pd.read_csv(byte_stream)
    byte_stream.close()
    return df

def push_dataframe_to_azure_blob(df, account_name, account_key, container_name, file_name):
    data= StringIO()
    df.to_csv(data)
    data=bytes(data.getvalue(), 'utf-8')
    data=BytesIO(data)
    blob_service = BlockBlobService(account_name=account_name,
                                   account_key=account_key)
    blob_service.create_blob_from_stream(container_name=container_name, 
                                   blob_name=file_name, 
                                   stream=data)
    data.close()
	
