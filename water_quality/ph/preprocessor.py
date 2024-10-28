
import pandas as pd
import json 
import os
import shutil


class PHPreprocess:

    def preprocess_train(self,data_path):
        try:
            self.data_path=data_path
            file_name=self.data_path.split('/')[-1]
            df=pd.read_csv(self.data_path)
            shutil.move(self.data_path,f'ph/data_archived/{file_name}')
            df.fillna(df.mean(),inplace=True)
            data=df
            X=data.drop(columns=['ph'])

            Y=data['ph']

            return X,Y
        
        except:
            return "Invalid","Invalid"
    

    def preprocess_predict(self,data_path):
        try:
            self.data_path=data_path
            file_name=self.data_path.split("\\")[-1]

            df=pd.read_csv(self.data_path)
            
            shutil.move(self.data_path,f'ph/data_archived/{file_name}')


            df.fillna(df.mean(),inplace=True)
            data=df
            
            if 'ph' in data.columns:
                data.drop(columns=['ph'],inplace=True)

            
            with open('ph/schema.json','r') as file:
                schema=json.load(file)
            
            numOfCols=schema["NoofCols"]
            cols=schema['Cols']

            if numOfCols!=len(data.columns):
                return "Invalid"

            for col in data.columns:
                if col not in cols:
                    return "Invalid"

            return data
        
        except:
            return "Invalid"
    
