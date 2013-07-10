from flask import Flask, render_template, request, make_response
import plivo
from app import app
import csv


auth_id = "MAMZRKNGYYNZQ1YJBHYT"
auth_token = "OGM0NzhiNjE5YzdjNWVjNDY0MDJhMzM0ZjY4MDYx"


p = plivo.RestAPI(auth_id, auth_token)   
 
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/call/', methods=['POST'])
def call():

    # Default dial no.
    dialNumber1 = 9010026001
    dialNumber2 = 9010026001

    if request.method == 'POST':
    	file = request.files['datafile']
	with open(file, 'rb') as csvfile:
	    nosList = csv.reader(csvfile)
	    for no in noslist:
		dialNumber1 = no[0]

        global text
        text = request.args.get('text')

	# Make Calls
        params = {
        'from': '1800111108', # Caller Id
        'to' : dialNumber1, # User Number to Call	
        'answer_url' : "http://lets-talk.herokuapp.com/answer_url/",
        'answer_method' : 'POST'
	'timeout' : '60'
	'ring_timeout' : '20'
        }
        response = p.make_call(params)

        print dialNumber1, dialNumber2, response
        return render_template('index.html', dialNumber1=dialNumber1, dialNumber2=dialNumber2)


@app.route('/answer_url/', methods=['POST'])
def answer_url():
    r = plivo.Response()
    
    # Add speak
    body = text
    params = {'loop':1}
    r.addSpeak(body, **params)
    
    response = make_response(r.to_xml())
    response.headers["Content-type"] = "text/xml"

    return response
