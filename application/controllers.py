from flask import request, redirect, url_for, flash
from flask import render_template
from flask import current_app as app
from application.models import User, List, Card
from .database import db
from datetime import datetime as dt
import json

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        user_name = request.form['name']

        user = User.query.filter_by(name=user_name).first()

        if user==None:
            new_user = User(name=user_name)
            db.session.add(new_user)
            db.session.commit()

        user = User.query.filter_by(name=user_name).first()

        return redirect(url_for('home',user_id = user.id))

    
@app.route("/home/<user_id>", methods=["GET","POST"])
def home(user_id):
    user = User.query.get(user_id)
    lists = user.lists

    list_dt = {}
    card_dtn = {}
    card_dty = {}
    cards = {}
    for l in lists:
        list_dt[l.id] = l.update_date
        cards[l.name] = l.cards
        for c in l.cards:
            if c.toggle == '0':
                card_dtn[c.id] = c.deadline
            else:
                card_dty[c.id] = [c.deadline, c.complete_date]

    return render_template("home.html",user=user,lists=lists,cards=cards, list_dt=list_dt, card_dtn=card_dtn, card_dty=card_dty)


@app.route('/createlist/<user_id>',methods=["GET","POST"])
def createlist(user_id):
    user = User.query.get(user_id)
    if request.method=="POST":
        list_name = request.form['name']
        description = request.form['description']
        update_date = dt.isoformat(dt.now())

        l = List.query.filter_by(name=list_name,user=user).first()

        if l is None:
            l = List(name=list_name,description=description,update_date=update_date, user=user)
            db.session.add(l)
            db.session.commit()
            flash('List created succesfully')
        else:
            flash('List name already exists')

        return redirect(url_for("home",user_id = user.id))


@app.route('/deletelist/<list_id>',methods=["GET","POST"])
def deletelist(list_id):
    l = List.query.get(list_id)
    db.session.delete(l)
    db.session.commit()
    flash('List deleted succesfully')
    return redirect(url_for('home',user_id = l.user_id))


@app.route('/updatelist/<list_id>',methods=["GET","POST"])
def updatelist(list_id):
    l = List.query.get(list_id)
    user = User.query.get(l.user_id)

    if request.method == "POST":
        new = List.query.filter_by(name=request.form['name'],user=user).first()

        if l.name == request.form['name'] or new == None:
            l.name = request.form['name']
            l.description = request.form['description']
            db.session.commit()
            flash('List updated succesfully')
        else:
            flash('List name already exists')
        return redirect(url_for('home',user_id = user.id))


@app.route('/createcard/<list_id>',methods=['POST','GET'])
def createcard(list_id):
    l = List.query.get(list_id)
    user = User.query.get(l.user_id)
    if request.method == "POST":
        card_name = request.form['name']
        content = request.form['content']
        deadline = request.form['deadline']
        toggle = False
        create_date = dt.isoformat(dt.today())
        complete_date = 'Not completed'

        today = dt.today().strftime('%Y-%m-%d')
        if deadline < today:
            flash('The Date must be Bigger or Equal to today date')
            return redirect(url_for("home",user_id = user.id))

        card = Card.query.filter_by(name=card_name,list = l).first()

        if card == None:
            c = Card(name=card_name,content=content,deadline=deadline,toggle=toggle,create_date=create_date,complete_date=complete_date,list=l)
            l.update_date = dt.isoformat(dt.now())
            db.session.add(c)
            db.session.commit()
            flash('Card created successfully')
        else:
            flash('Card name already exists')
        return redirect(url_for("home",user_id = user.id))


@app.route('/deletecard/<card_id>',methods=["GET","POST"])
def deletecard(card_id):
    card = Card.query.get(card_id)
    l = List.query.get(card.list_id)
    db.session.delete(card)
    db.session.commit()
    flash('Card deleted successfully')
    return redirect(url_for('home',user_id = l.user_id))


@app.route('/updatecard/<card_id>', methods=['POST','GET'])
def updatecard(card_id):
    card = Card.query.get(card_id)
    l = List.query.get(card.list_id)
    user = User.query.get(l.user_id)

    if request.method == "POST":
        today = dt.today().strftime('%Y-%m-%d')
        if request.form['deadline'] < today:
            flash('The Date must be Bigger or Equal to today date')
            return redirect(url_for("home",user_id = user.id))

        flag = False
        newlist = List.query.filter_by(name=request.form['list'],user=user).first()
        c = Card.query.filter_by(name=request.form['name'],list=newlist).first()
        if l.name == request.form['list']:
            if card.name == request.form['name'] or c == None:
                flag = True
        elif c == None:
            card.list_id = newlist.id
            flag = True

        if flag:
            newlist.update_date = dt.isoformat(dt.now())
            card.name = request.form['name']
            card.content = request.form['content']
            card.deadline = request.form['deadline']
            db.session.commit()
            flash('Card updated successfully')
        else:
            flash('Card name already exists in the given list')

        return redirect(url_for('home',user_id = user.id))


@app.route('/toggle/<card_id>',methods=['POST'])
def toggle(card_id):
    if request.method == 'POST':
        tog = request.form['toggle-output']

        card = Card.query.get(card_id)
        l = List.query.get(card.list_id)
        
        if tog == 'true':
            card.toggle = 1
            card.complete_date = dt.isoformat(dt.today())
        else:
            card.toggle = 0
            card.complete_date = 'Not completed'
        db.session.commit()

    return redirect(url_for('home',user_id = l.user_id))


@app.route('/summary/<user_id>',methods=['GET','POST'])
def summary(user_id):
    if request.method == 'GET':
        user = User.query.get(user_id)
        (labels, data1, data0) = ([], [], [])
        for l in user.lists:
            labels.append(l.name)
            temp1 = 0
            temp0 = 0
            for card in l.cards:
                if card.toggle == '1':
                    temp1 += 1
                else:
                    temp0 += 1
            data1.append(temp1)
            data0.append(temp0)
        print(labels, data1, data0)
        return render_template('summary.html', user = user, labels = json.dumps(labels), data1 = json.dumps(data1), data0 = json.dumps(data0) )        
