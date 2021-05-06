# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from flask import Flask, render_template, request
import json
from flask import make_response
from SendEmail.sendEmail import EmailSender
from email_templates import template_reader
import os



app = Flask(__name__)
@app.route('/webhook', methods=['POST'])
def webhook():
    #print("Affan here ........")
    #print("Request:")
    req = request.get_json(silent=True, force=True)
    #print(json.dumps(req, indent=4))
    res = processRequest(req)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

# processing the request from dialogflow
def processRequest(req):
    #log = logger.Log()

    sessionID=req.get('responseId')
    result = req.get("queryResult")
    user_says=result.get("queryText")
    #log.write_log(sessionID, "User Says: "+user_says)
    parameters = result.get("parameters")
    
    #cust_contact = parameters.get("phn_no")
    #course_no = parameters.get("number")
    cust_contact = "12345"
    course_no = "1"
    cust_name = parameters.get("name")
    cust_email = parameters.get("email")
    
    print(cust_name)
    #print(cust_contact)
    print(cust_email)
    #print(course_no)
    course_name = 'DataScienceMasters'

    # if(course_no == 1):
    #     course_name = 'DataScienceMasters'
    # elif(course_no == 2):
    #     course_name = 'MachineLearningMasters'
    # elif(course_no == 3):
    #     course_name ='DeepLearningMasters'
    # else:
    #     course_name ='NLPMasters'
        
    intent = result.get("intent").get('displayName')
    print(course_name)
    if (intent=='Get Promotional Emails'):
        email_sender=EmailSender()
        template= template_reader.TemplateReader()
        email_message=template.read_course_template(course_name)
        email_sender.send_email_to_student(cust_email,email_message)
        
        fulfillmentText="I have sent the brochure and a promocode valid for 10th June 2021. You can get 20% flat discount through this promocode. Enter 1 for main menu and 0 to exit the chat"
       
        return {
            "fulfillmentText": fulfillmentText
        }


    else:
        return "nothing found"
       
  


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
    #app.run()
