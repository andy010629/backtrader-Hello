import pymongo
import pandas as pd

db_client = pymongo.MongoClient("mongodb://localhost:27017/")

# def mongoClient(doc,db='shioajiOptionsData'):
db = 'shioajiOptionsData'
mydb = db_client[db]

def mongo_to_dataframe(doc,dt=None,db='shioajiOptionsData'):
    collection = mydb[doc]
    if dt:
        df_opts = pd.DataFrame(list(collection.find()))
        for index, row in df_opts.iterrows():
            if row['ts'] > dt:
                opt = df_opts.iloc[index-1]
                return opt
        return df_opts.iloc[-1]
    else:
        return pd.DataFrame(list(collection.find()))
