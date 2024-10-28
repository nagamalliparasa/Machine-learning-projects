
# developed using flask 
import os 
from os import listdir
from flask import Flask,render_template,redirect,request,flash,url_for
import pandas as pd
import uuid



from water_quality.preprocessor import Preprocess
from water_quality.predict import Predict
from water_quality.training import Training



pre=Preprocess()
predict=Predict()
train=Training()
temp_store={}

# from water_quality.training import Training
app=Flask(__name__)

app.secret_key = 'your_unique_secret_key_here'

@app.route('/')
def home():

    return render_template('home.html')

@app.route('/potability')
def potability():
    # check once the model is trained or not
    # if len(listdir('water_quality/models')) == 0: 
    #     # Need to be trained 
    #     train=Training()
    #     data_path='water_quality/data'
    #     train.train(data_path)
    # if len(listdir('water_quality/models')) == 0: 
    #     return "Data is not give to train"
    
    print(len(listdir('water_quality/models')))
    print(len(listdir('water_quality/data')))
    if len(listdir('water_quality/models')) != 1:
        
        if len(listdir('water_quality/data')) ==0:
            flash("Train the data first")
            return redirect(request.url)
        
        for file in listdir('water_quality/data'):
            res=train.train(os.path.join('water_quality/data/',file))
            if res=="Invalid":
                flash("Not Enough data to train")


    return render_template('potability.html')



@app.route('/single_prediction',methods=['GET','POST'])
def single_prediction():
    
    if request.method=='POST':
        input1 = request.form.get('input1')
        input2 = request.form.get('input2')
        input3 = request.form.get('input3')
        input4 = request.form.get('input4')
        input5 = request.form.get('input5')
        input6 = request.form.get('input6')
        input7 = request.form.get('input7')
        df = pd.DataFrame({
            'ph': [input1],
            'Hardness': [input2],
            'Chloramines': [input3],
            'Sulfate': [input4],
            'Conductivity': [input5],
            'Organic_carbon': [input6],
            'Trihalomethanes': [input7]
        })
        print(df)
        df.to_csv('water_quality/data/pred.csv',index=False)
        
        return redirect(url_for('show_predictions'))


        # print(f'{input1},{input2},{input3},{input4},{input5},{input6},{input7},')
    else: 
        return render_template('single_pred.html')



@app.route('/batch_prediction',methods=['GET','POSt'])
def batch_prediction():
    if request.method=='POST':
        if 'file' not in request.files:
            flash("No file part")
            redirect(request.url)
        file=request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and file.filename.endswith('.csv'):
            # Save the file to the specified folder
            filepath = os.path.join('water_quality/data', file.filename)
            file.save(filepath)

            # Redirect to the display page and pass the filename
            return redirect(url_for('show_predictions'))
        else:
            flash('Please upload a valid CSV file')
            return redirect(request.url)
    else: 
        return render_template('batch_pred.html')
    

@app.route('/show_predictions')
def show_predictions():
    data_path='water_quality/data'
    predictions=[]
    for file in os.listdir(data_path):
        data=pre.preprocess_predict(os.path.join(data_path,file))
        if data.empty:
            flash("Invalid data given")
            redirect(url_for('potability'))
        
        predictions=predict.predict(data)

    unique_id=str(uuid.uuid4())
    temp_store[unique_id]=predictions
    return redirect(url_for('show_results',id=unique_id))
        
@app.route("/show_results")
def show_results():
    unique_id=request.args.get('id')
    predictions=temp_store.pop(unique_id,None)
    
    if predictions is None:
        return render_template('show_res.html')

    return render_template('show_res.html',predictions=predictions)





# Ph Check 

from ph.preprocessor import PHPreprocess
from ph.training import PHTraining
from ph.predict import PHPredict


ph_pre=PHPreprocess()
ph_predict=PHPredict()
ph_train=PHTraining()


@app.route('/ph_check')
def ph_check():
    print(len(listdir('ph/models')))
    print(len(listdir('ph/data')))
    if len(listdir('ph/models')) != 1:
        
        if len(listdir('ph/data')) ==0:
            flash("Train the data first")
            return redirect(request.url)
        
        for file in listdir('ph/data'):
            res=ph_train.train(os.path.join('ph/data/',file))
            if res=="Invalid":
                flash("Not Enough data to train")
    return render_template('ph_check.html')



@app.route('/ph_single_prediction',methods=['GET','POST'])
def ph_single_prediction():
    
    if request.method=='POST':
        input1 = request.form.get('input1')
        input2 = request.form.get('input2')
        input3 = request.form.get('input3')
        input4 = request.form.get('input4')
        input5 = request.form.get('input5')
        input6 = request.form.get('input6')
        input7 = request.form.get('input7')
        input8 = request.form.get('input8')
        input9 = request.form.get('input9')
        df = pd.DataFrame({
            'Hardness': [input1],
            'Solids':[input2],
            'Chloramines': [input3],
            'Sulfate': [input4],
            'Conductivity': [input5],
            'Organic_carbon': [input6],
            'Trihalomethanes': [input7],
            'Turbidity':[input8],
            'Potability':[input9]
        })
        print(df)
        df.to_csv('ph/data/predict.csv',index=False)
        
        return redirect(url_for('ph_show_predictions'))


        # print(f'{input1},{input2},{input3},{input4},{input5},{input6},{input7},')
    else: 
        return render_template('ph_single_pred.html')



@app.route('/ph_batch_prediction',methods=['GET','POSt'])
def ph_batch_prediction():
    if request.method=='POST':
        if 'file' not in request.files:
            flash("No file part")
            redirect(request.url)
        file=request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and file.filename.endswith('.csv'):
            # Save the file to the specified folder
            filepath = os.path.join('ph/data', file.filename)
            file.save(filepath)

            # Redirect to the display page and pass the filename
            return redirect(url_for('ph_show_predictions'))
        else:
            flash('Please upload a valid CSV file')
            return redirect(request.url)
    else: 
        return render_template('ph_batch_pred.html')


@app.route('/ph_show_predictions')
def ph_show_predictions():
    data_path='ph/data'
    predictions=[]
    for file in os.listdir(data_path):
        data=ph_pre.preprocess_predict(os.path.join(data_path,file))
        if data.empty:
            flash("Invalid data given")
            redirect(url_for('ph_check'))
        
        predictions=ph_predict.predict(data)

        print("Data is ")
        print(data)
        print("Predictions are")
        print(predictions)

    
    unique_id=str(uuid.uuid4())
    temp_store[unique_id]=predictions

    
    return redirect(url_for('ph_show_results',id=unique_id))


@app.route("/ph_show_results")
def ph_show_results():
    unique_id=request.args.get('id')

    predictions=temp_store.pop(unique_id,None)
    
    # res=predictions[1:-1].split()
    # print("Type",type(predictions))
    # print("Type res",type(res))
    # print("Results function")
    # print("Length of result is ",len(predictions))
    if predictions is None:
        return render_template('ph_show_res.html')
    # for i in predictions:
    #     # if i=='0' or i=='1':
    #     #     res.append(i)
    #     print(i)
    #     # res.append(i)


    return render_template('ph_show_res.html',predictions=predictions)



if __name__=='__main__':
    app.run(debug=True)
