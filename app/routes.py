from flask import Flask, request, flash, url_for, redirect, render_template ,json

from app import app
from app.gmailread import read
from app.takeout import read_take
from app import client
    
@app.route('/',methods=['GET'])
def login():
    return render_template('base.html')

@app.route('/home',methods=['GET'])
def home():
    read()
    return render_template('base.html')

@app.route('/takeout',methods=['GET'])
def takeout():
    read_take()
    return render_template('base.html')

