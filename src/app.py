
#imports
import tensorflow as tf
from flask import Flask, render_template, request, redirect, json

from call_prediction_dl import Predict

app = Flask(__name__)

@app.route('/')
def hello_world():
   return render_template('index.html')


"""
input
{
    "satisfaction": 75, (0-100)
    "evaluation": 60, (0-100)
    "number_of_projects": 4, (1-N)
    "average_montly_hours": 180, (1-999)
    "time_spend_company": 15, (1-99)
    "work_accident": 1, (no/yes)
    "promotion": 0, (no/yes)
    "department": "technical" (list, e.g "technical", "hr"
    "salary": "medium", (low/medium/high))
}
"""
@app.route('/input', methods=['POST'])
def get_input():
   req_data = request.get_json()
   satisfaction = req_data['satisfaction']
   # evaluation = req_data['evaluation']
   # number_of_projects = req_data['number_of_projects']
   # average_montly_hours = req_data['average_montly_hours']
   # time_spend_company = req_data['time_spend_company']
   # work_accident = req_data['work_accident']
   print(f'req_data is {req_data}')
   print(type(req_data))
   # print(f'satisfaction is {satisfaction}')
   # extract input from the payload
   # e.g input = '{"satisfaction":0.74,"evaluation":0.92,"number_of_projects":4,"average_montly_hours":261,"time_spend_company":5,"work_accident":0,"churn":1,"promotion":0,"department":"technical","salary":"medium"}'
   # get the data array from input
   # data = get_data_array(input) => [0.35164836,0.265625,0.0,0.28504673,0.125,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0]
   data = [satisfaction, 0.265625,0.0,0.28504673,0.125,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0]
   model = tf.keras.models.load_model('../data/processed_files' + '/test/' + 'my_model.h5')
   predict_output = Predict(model , data).risk_output
   # Predict(model , data)
   output = {"predict": str(predict_output)}
   print(predict_output)
   response = app.response_class(
      response=json.dumps(output),
      status=200,
      mimetype='application/json')
   return response
   # extract input from the payload
   # e.g input = '{"satisfaction":0.74,"evaluation":0.92,"number_of_projects":4,"average_montly_hours":261,"time_spend_company":5,"work_accident":0,"churn":1,"promotion":0,"department":"technical","salary":"medium"}'
   # get the data array from input
   # data = get_data_array(input) => [0.35164836,0.265625,0.0,0.28504673,0.125,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0]
   # send 'data' to the model
   # return the model's output to the client
   #print(request.data)
   #return redirect('/')
