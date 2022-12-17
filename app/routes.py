from flask import Flask, request, flash, url_for, redirect, render_template ,json

from app import app

@app.route('/',methods=['GET'])
def login():
    return render_template('base.html')

