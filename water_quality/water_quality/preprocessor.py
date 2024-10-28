
import pandas as pd
import json 
import os
import shutil

class Preprocess:

    def preprocess_train(self,data_path):
        try:
            self.data_path=data_path
            file_name=self.data_path.split('/')[-1]
            df=pd.read_csv(self.data_path)
            shutil.move(self.data_path,f'water_quality/data_archived/{file_name}')
            df.fillna(df.mean(),inplace=True)
            data=df.drop(columns=['Solids','Turbidity'])
            X=data.drop(columns=['Potability'])

            Y=data['Potability']

            return X,Y
        
        except:
            return "Invalid","Invalid"
    

    def preprocess_predict(self,data_path):
        try:
            self.data_path=data_path
            file_name=self.data_path.split("\\")[-1]

            df=pd.read_csv(self.data_path)
            
            shutil.move(self.data_path,f'water_quality/data_archived/{file_name}')


            df.fillna(df.mean(),inplace=True)
            data=df
            if 'Solids' in data.columns:
                data.drop(columns=['Solids'],inplace=True)
            if 'Turbidity' in data.columns:
                data.drop(columns=['Turbidity'],inplace=True)
            
            if 'Potability' in data.columns:
                data.drop(columns=['Potability'],inplace=True)

            
            with open('water_quality/schema.json','r') as file:
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
    


        