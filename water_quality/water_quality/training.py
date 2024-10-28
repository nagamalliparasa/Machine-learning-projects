# Trainmodel 

from .preprocessor import Preprocess
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from .fileOperation import save_model,load_model

class Training:

    def train(self,data_path):
        try:
            print("Training Started")
            self.data_path=data_path
            pre=Preprocess()
            scaler=StandardScaler()
            X,y=pre.preprocess_train(self.data_path)
            print("Preprocessing done")
            print(X)
            print(y)
            
            if X.empty:
                return 'Invalid'
            if y.empty:
                return 'Invalid'
            
            X_scaled=scaler.fit_transform(X)
            
            model=GradientBoostingClassifier(learning_rate=0.05, max_depth=4, min_samples_leaf=2, min_samples_split=5, n_estimators=200)
            model.fit(X_scaled,y)

            print("Model trained")
            save_model(model,'gbdt')
            print("End of training successfully ended training")
            return None
        except:
            return "Invalid"


    
    def retrain(self,data_path):
        self.data_path=data_path
        pre=Preprocess()
        scaler=StandardScaler()
        X,y=pre.preprocess_train(self.data_path)
        X_scaled=scaler.fit_transform(X)

        model=load_model()
        if model=="No Model Trainied":
            return "First train the model"
        
        save_model(model,'gbdt')




