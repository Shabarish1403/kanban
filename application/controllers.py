from flask import Flask, request, redirect, url_for
from flask import render_template
from flask import current_app as app
from application.models import User, List, Card, UserList, ListCard
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
    user = User.query.filter_by(user_name=user_name).first()

    user_lists = UserList.query.filter_by(euser_id=user.user_id).all()
    lists = []
    for row in user_lists:
        lists.append(List.query.filter_by(list_id=row.elist_id).first())

    cards = {}
    for list in lists:
        list_cards = ListCard.query.filter_by(elist_id=list.list_id).all()
        cards_list = []
        for row in list_cards:
            cards_list.append(Card.query.filter_by(card_id=row.card_id).first())
        cards[list.list_name] = cards_list

    return render_template("home.html",user_name=user_name,lists=lists,cards=cards)

@app.route('/<user_name>/createlist',methods=["GET","POST"])
def createlist(user_name):
    if request.method=="GET":
        return render_template("create_list.html",user_name=user_name)
    elif request.method=="POST":
        list_name = request.form['name']
        description = request.form['description']
        l = List(list_name=list_name,description=description)
        ul = UserList()
        db.session.add(l)
        db.session.commit()
        return redirect(url_for("home",username=user_name))

@app.route('/<username>/<listname>/deletelist',methods=["GET","POST"])
def deletelist(listname,username):
    del_list = List.query.filter_by(list_name=listname).first()
    db.session.delete(del_list)
    db.session.commit()
    return redirect(url_for('home',username=username))

@app.route('/<username>/<listname>/updatelist',methods=["GET","POST"])
def updatelist(username,listname):
    list = List.query.filter_by(list_name=listname).first()
    if request.method == "GET":
        return render_template('update_list.html',username=username,list=list)
    elif request.method == "POST":
        list.description = request.form['description']
        db.session.commit()
        return redirect(url_for('home',username=username))


@app.route('/<username>/<listname>/createcard',methods=['POST','GET'])
def createcard(username,listname):
    if request.method == "GET":
        return render_template('create_card.html',username=username,listname=listname)
    elif request.method == "POST":
        card_name = request.form['name']
        content = request.form['content']
        deadline = request.form['deadline']
        c = Card(list_name=listname,card_name=card_name,content=content,deadline=deadline)
        db.session.add(c)
        db.session.commit()
        return redirect(url_for("home",username=username))

@app.route('/<username>/<listname>/<cardname>/deletecard',methods=["GET","POST"])
def deletecard(listname,username,cardname):
    del_card = List.query.filter_by(card_name=cardname).first()
    db.session.delete(del_card)
    db.session.commit()
    return redirect(url_for('home',username=username))
