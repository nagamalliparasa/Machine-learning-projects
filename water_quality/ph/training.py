
from .preprocessor import PHPreprocess
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from .fileOperation import save_model,load_model



class PHTraining:

    def train(self,data_path):
        try:
            print("Training Started")
            self.data_path=data_path
            pre=PHPreprocess()
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
            
            model=SVR()
            model.fit(X_scaled,y)

            print("Model trained")
            save_model(model,'svr')
            print("End of training successfully ended training")
            return None
        except:
            return "Invalid"


    
    def retrain(self,data_path):
        self.data_path=data_path
        pre=PHPreprocess()
        scaler=StandardScaler()
        X,y=pre.preprocess_train(self.data_path)
        X_scaled=scaler.fit_transform(X)

        model=load_model()
        if model=="No Model Trainied":
            return "First train the model"
        
        save_model(model,'svr')




