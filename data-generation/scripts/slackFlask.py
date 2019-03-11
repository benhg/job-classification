#!/usr/bin/python3 

import sys
import datetime
from flask import Flask, request, render_template
import random
import json
import requests
import pytz
import time
import os
import pickle
from collections import Counter

app = Flask(__name__)

# get id from ehre: https://api.slack.com/methods/users.list/test

#students = ['Josh(<@U1JE6D9CK|Josh>)','Miles(<@U1H6MPCSU|Miles>)','Ben(<@U1H59603D|Ben>)','Joanna(<@U1H6FBYDA|Joanna>)','Ethan(<@U1J3S0EDN|Ethan>)','Janine(<@U1LKJTV2M|Janine>)','Wanqi(<@U1NSCAXDH|Wanqi>)','Logan(<@U1H7027GS|Logan>)','Elbert(<@U1SMBTE9K|Elbert>)']
#students = ['Yadu(<@U0Z7WMFNJ|yadunand>)']
students=[ 'Rohan(<@U5T3BLJF3|Rohan>)','Samarth(<@U5T0E680Y|Samarth>)','Alex(<@U5GG96EJH|Alex>)','Ben(<@U1H59603D|Ben>)','Justin(<@U1HH8GWTU|Justin>)','Theodore(<@U1JJT2WCV|Theodore>)','Miles(<@U1H6MPCSU|Miles>)','Logan(<@U1H7027GS|Logan>)', 'Blue(<@NOT A THING YET|Blue>)','Emily(<@NOT A THING YET|Blue>)']
student_ids = [s.split('@')[1].split("|")[0] for s in students]
student_names = [s.split('(')[0] for s in students]
scores=json.loads(open('/var/www/slackFlask/students.json').read())

def hasAccess(data):
    if data["channel_name"] != "summer_students":
        if data["user_id"] not in student_ids or data["user_id"] in ['U1JE6D9CK','U1H59603D']:
            return True
        return False
    else:
        return True

def url(channel):
    if channel == "summer_students":
        return "https://hooks.slack.com/services/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"
    else:
        return "https://hooks.slack.com/services/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"

@app.route('/')
def index():
    return 'Index Page'

@app.route('/shame', methods=["POST"])
def shame():
    if hasAccess(request.form):
        requests.post(url(request.form['channel_name']),data=json.dumps({'text': 'SHAME ON <@'+request.form['text']+'>'}))
    return ""



@app.route('/bing', methods=["POST"])
def bing():
    requests.post(url(request.form['channel_name']), data=json.dumps({'text': '<http://lmgtfy.com/?q='+request.form['text'].replace(' ','+')+">"}));
    return ""


@app.route('/delegate', methods=["POST"])
def delegate():
    if hasAccess(request.form):
        student=random.choice(students) + ": " + request.form['text'] + "\n\t -requested by "+request.form['user_name']+"(<@"+request.form["user_id"] + ">)"
        requests.post(url(request.form['channel_name']), data=json.dumps({'text': student}))
    else:
	requests.post(url(request.form['channel_name']), data=json.dumps({'text': request.form['user_name']+"(<@"+request.form["user_id"] + ">) attempted to delegate a task, but did not have permission."}))
    return ""


@app.route('/say', methods=["POST"])
def say():
    if hasAccess(request.form):
        requests.post(url(request.form['channel_name']), data=json.dumps({'text': request.form['text']}))
    else:
	requests.post(url(request.form['channel_name']), data=json.dumps({'text': request.form['user_name']+"(<@"+request.form["user_id"] + ">) attempted to say something, but did not have permission."}))
    return ""


@app.route('/pick', methods=['POST'])
def pick():
    requests.post(url(request.form['channel_name']), data=json.dumps({'text': '"'+str(random.choice(request.form['text'].split(',')))+'" was picked from ' + json.dumps(request.form["text"].split(',')) + "\n\t -requested by " + request.form['user_name'] + "(<@" + request.form["user_id"] + ">)"}))
    return ""



@app.route('/palindrome', methods=['POST'])
def palindrome():
    requests.post("https://hooks.slack.com/services/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", data=json.dumps({'text': request.form['text'][:-1]+request.form['text'][::-1]}))
    return ""


@app.route('/bathroom', methods=["POST"])
def bathroom():
    time=str(datetime.datetime.now(pytz.timezone('US/Central')))
    if request.form['text'].lower()=='leave':
        use=' left to use'
    elif request.form['text'].lower()=='return':
        use=' returned from'
    else:
        # requests.post('https://hooks.slack.com/services/T0Z6LE8MV/B1K1KD', json.dumps({'text':"USER "+request.form['user_name']+"(<"+request.form['user_id']+">) CANNOT FOLLOW BASIC INSTRUCTIONS"}))
        return ""

    string=request.form['user_name']+"(<@"+request.form['user_id']+">)" +use+" the restroom at "+time+"."
    requests.post('https://hooks.slack.com/services/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', json.dumps({'text':string}))
    return ""

@app.route('/leaderboard', methods=["GET"])
def leaderboard():
    scores=json.loads(open('/var/www/slackFlask/students.json').read())
    return render_template("leaderboard.html", scores=scores)

@app.route('/calculate')
def calculate():
    dict={}
    for student in student_names:
        dict2={}
        dict2['name']=student
        dict2['concern']=0
        dict2['pride']=0
        dict[student]=dict2
    file=open('students.json',"w")
    file.write(json.dumps(dict, indent=4))
    return ""

@app.route('/praise', methods=['POST'])
def praise():
    print(hello')
    if hasAccess(request.form):
        student=request.form[text]
        scores=json.loads(open('/var/www/slackFlask/students.json').read())
        scores[student]["pride"]+=1
        file=open("students.json","w")
        file.write(json.dumps(scores,indent=4))
        return ""
    else:
        pass

@app.route(
'/concern')
def concern():
    if hasAccess(request.form):
        student=request.form[text]
        scores=json.loads(open('/var/www/slackFlask/students.json').read())
        scores[student]["concern"]+=1
        file=open("students.json","w")
        file.write(json.dumps(scores,indent=4))
        return ""
    else:
        pass
        return ""
