import re
from flask import Flask, request, redirect, url_for
from flask import render_template
from flask import current_app as app
from application.models import User, List, Card
from .database import db

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        user_name = request.form['user_name']

        user = User.query.filter_by(user_name=user_name).first()

        if user==None:
            new_user = User(user_name=user_name)
            db.session.add(new_user)
            db.session.commit()

        return redirect(url_for('home',user_name=user_name))

    
@app.route("/home/<user_name>", methods=["GET","POST"])
def home(user_name):
    lists = List.query.filter_by(user_name=user_name).all()

    cards = {}
    for list in lists:
        print(list.cards)
        cards_list = Card.query.filter_by(list_id=list.list_id).all()
        cards[list.list_name] = cards_list

    return render_template("home.html",user_name=user_name,lists=lists,cards=cards)

@app.route('/<user_name>/createlist',methods=["GET","POST"])
def createlist(user_name):
    if request.method=="GET":
        return render_template("create_list.html",user_name=user_name)
    elif request.method=="POST":
        list_name = request.form['name']
        description = request.form['description']

        #need to add an alert in browser if listname already exists
        list = List.query.filter_by(user_name=user_name,list_name=list_name).first()
        if list == None:
            l = List(user_name=user_name,list_name=list_name,description=description)
            db.session.add(l)
            db.session.commit()

        return redirect(url_for("home",user_name=user_name))

@app.route('/<user_name>/<list_name>/deletelist',methods=["GET","POST"])
def deletelist(user_name,list_name):
    del_list = List.query.filter_by(user_name=user_name,list_name=list_name).first()
    db.session.delete(del_list)
    db.session.commit()
    return redirect(url_for('home',user_name=user_name))

@app.route('/<user_name>/<list_name>/updatelist',methods=["GET","POST"])
def updatelist(user_name,list_name):
    #need to add go back or home button
    list = List.query.filter_by(user_name=user_name,list_name=list_name).first()
    if request.method == "GET":
        return render_template('update_list.html',user_name=user_name,list=list)
    elif request.method == "POST":
        l = List.query.filter_by(user_name=user_name,list_name=request.form['name']).first()

        if list.list_name == request.form['name']:
            list.description = request.form['description']
            db.session.commit()
        elif l == None:
            list.list_name = request.form['name']
            list.description = request.form['description']
            db.session.commit()
        return redirect(url_for('home',user_name=user_name))

@app.route('/<user_name>/<list_name>/createcard',methods=['POST','GET'])
def createcard(user_name,list_name):
    if request.method == "GET":
        return render_template('create_card.html',user_name=user_name,list_name=list_name)
    elif request.method == "POST":
        card_name = request.form['name']
        content = request.form['content']
        deadline = request.form['deadline']

        list = List.query.filter_by(user_name=user_name, list_name=list_name).first()
        card = Card.query.filter_by(list_id = list.list_id, card_name=card_name).first()

        if card == None:
            c = Card(list_id=list.list_id,card_name=card_name,content=content,deadline=deadline)
            db.session.add(c)
            db.session.commit()
        return redirect(url_for("home",user_name=user_name))

@app.route('/<user_name>/<list_name>/<card_name>/deletecard',methods=["GET","POST"])
def deletecard(user_name,list_name,card_name):
    list = List.query.filter_by(user_name=user_name,list_name=list_name).first()
    del_card = Card.query.filter_by(list_id=list.list_id,card_name=card_name).first()
    db.session.delete(del_card)
    db.session.commit()
    return redirect(url_for('home',user_name=user_name))

@app.route('/<user_name>/<list_name>/<card_name>/updatecard', methods=['POST','GET'])
def updatecard(user_name,list_name,card_name):
    #need to add go back or home button
    lists = List.query.filter_by(user_name=user_name).all()
    list = List.query.filter_by(user_name=user_name,list_name=list_name).first()
    card = Card.query.filter_by(list_id=list.list_id,card_name=card_name).first()
    if request.method == "GET":
        return render_template('update_card.html',user_name=user_name,card=card,lists=lists,list=list)
    elif request.method == "POST":
        if list.list_name == request.form['list']: #need to alert if same card name exists in same list
            c = Card.query.filter_by(list_id=list.list_id,card_name=request.form['name']).first()
            if card.card_name == request.form['name']:
                card.content = request.form['content']
                card.deadline = request.form['deadline']
                db.session.commit()
            elif c == None:
                card.card_name = request.form['name']
                card.content = request.form['content']
                card.deadline = request.form['deadline']
                db.session.commit()
        else:
            newlist = List.query.filter_by(user_name=user_name,list_name=request.form['list']).first()
            c = Card.query.filter_by(list_id=newlist.list_id, card_name=request.form['name']).first()            
            if c == None:
                card.list_id = newlist.list_id
                card.card_name = request.form['name']
                card.content = request.form['content']
                card.deadline = request.form['deadline']
                db.session.commit()

        return redirect(url_for('home',user_name=user_name))