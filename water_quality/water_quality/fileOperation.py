
from os import listdir
import os
import pickle 
import shutil

def save_model(model,file_name):
    # print(os.getcwd())
    path="water_quality/models"

    
    for file in os.listdir(path):
        os.remove(path+'/'+file)
    
    with open(path+"/"+file_name+'.sav','wb') as f:
        pickle.dump(model,f)


def load_model():
    
    # we will have only one model in 'models' folder 
    path="water_quality/models"
    if len(listdir(path)) ==0:
        return "No Model Trained"
    
    for file in listdir(path):
        with open(path+'/'+file,'rb') as file:
            model=pickle.load(file)

    return model


def move_files():
    for file in listdir('data'):
        shutil.move('data/'+file,'data_archived/'+file)
