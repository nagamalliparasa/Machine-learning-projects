

# from preprocessor import Preprocess 
from os import listdir 
import os 
from .fileOperation import load_model
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np 

class PHPredict:

    def predict(self,data):
        
        model=load_model()

        if model=='No Model Trained':
            return "Invalid"
        scaler=StandardScaler()
        data=scaler.fit_transform(data)

        predictions=model.predict(data)
        predictions=np.array(predictions)
        print(predictions)
        print("Type in model predict",type(predictions))

        return predictions

       