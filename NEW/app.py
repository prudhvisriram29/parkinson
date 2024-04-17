from flask_socketio import SocketIO
from flask import Flask, render_template, request, session, redirect, url_for
#import Predict as PR
import RF as RF
import SVMALG as SVM
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('Main.html')

@app.route('/Main')
def Main():
    return render_template('Main.html')

@app.route('/Working')
def Working():
    return render_template("Working.html")

@app.route('/Checkup')
def Checkup():
     return render_template("Prediction.html")

@app.route('/Training1',methods=['POST'])
def train1():
	path=request.form['path']
	print("Train Images",path)
	RF.process(path)
	return render_template("Training1.html",message="Training SuccesFully Finished")

@app.route('/Training2',methods=['POST'])
def train2():
	path=request.form['path']
	print("Train Images",path)
	SVM.process(path)
	return render_template("Training2.html",message="Training SuccesFully Finished")
			
    


@app.route('/Training1')
def Training1():
    return render_template("Training1.html")

@app.route('/Training2')
def Training2():
    return render_template("Training2.html")


parkinson_data = pd.read_csv('parkinsons.csv')
# Preprocess the data if needed
# For example, handle missing values, encode categorical variables, etc.

# Initialize and train the Random Forest classifier
X_train = parkinson_data.drop(['name', 'status'], axis=1)
y_train = parkinson_data['status']
rf_classifier = RandomForestClassifier(random_state=42)
rf_classifier.fit(X_train, y_train)

@app.route('/parkinson_prediction', methods=['POST'])
def parkinson_prediction():
    try:
        # Extracting data from the form
        mdvp_fo = float(request.form['mdvp_fo'])
        mdvp_fhi = float(request.form['mdvp_fhi'])
        mdvp_flo = float(request.form['mdvp_flo'])
        mdvp_jitter_percent = float(request.form['mdvp_jitter_percent'])
        mdvp_jitter_abs = float(request.form['mdvp_jitter_abs'])
        mdvp_rap = float(request.form['mdvp_rap'])
        mdvp_ppq = float(request.form['mdvp_ppq'])
        jitter_ddp = float(request.form['jitter_ddp'])
        mdvp_shimmer = float(request.form['mdvp_shimmer'])
        mdvp_shimmer_db = float(request.form['mdvp_shimmer_db'])
        shimmer_apq3 = float(request.form['shimmer_apq3'])
        shimmer_apq5 = float(request.form['shimmer_apq5'])
        mdvp_apq = float(request.form['mdvp_apq'])
        shimmer_dda = float(request.form['shimmer_dda'])
        nhr = float(request.form['nhr'])
        hnr = float(request.form['hnr'])
        rpde = float(request.form['rpde'])
        dfa = float(request.form['dfa'])
        spread1 = float(request.form['spread1'])
        spread2 = float(request.form['spread2'])
        d2 = float(request.form['d2'])
        ppe = float(request.form['ppe'])
        # Extract other input fields as needed

        # Make prediction using the trained model
        prediction = rf_classifier.predict([[mdvp_fo, mdvp_fhi, mdvp_flo, mdvp_jitter_percent, mdvp_jitter_abs,
                                         mdvp_rap, mdvp_ppq, jitter_ddp, mdvp_shimmer, mdvp_shimmer_db,
                                         shimmer_apq3, shimmer_apq5, mdvp_apq, shimmer_dda, nhr, hnr,
                                         rpde, dfa, spread1, spread2, d2, ppe]])  # Adjust input data based on your model

        # Prepare the result message
        parkinsons_diagnosis = "Parkinson's Test Result: Negative" if prediction[0] == 0 else "Parkinson's Test Result: Positive"

        # Pass the diagnosis result to the template for rendering
        return render_template("Prediction.html", parkinsons_diagnosis=parkinsons_diagnosis)
    except Exception as e:
        error_message = "Error processing request: {}".format(str(e))
        return render_template("error.html", error_message=error_message)



@app.route('/Prediction')
def Prediction():
    return render_template("Prediction.html")


@socketio.on('message')
def handleMessage(msg):
    print("Message received: " + msg)

@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    pass

if __name__ == '__main__':
    socketio.run(app, debug=True, host='127.0.0.1', port=4000)
