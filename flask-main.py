
from flask import Flask, render_template,request,redirect,flash,url_for
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///fish.sqlite3'
app.config['SECRET_KEY']='632h3232ss'
db = SQLAlchemy(app)
app.user=""

class fishLog(db.Model):
   id = db.Column('fish_id', db.Integer, primary_key = True)
   name= db.Column('name' ,db.String(50))
def __init__(self, name, city, addr,pin):
   self.name = name

class accounts(db.Model):
   id = db.Column('account_id', db.Integer, primary_key = True)
   username= db.Column('username' ,db.String(50))
   password=db.Column('password' ,db.String(50))
def __init__(self, name, city, addr,pin):
   self.name = name
db.create_all()

@app.route("/login")
def login() :
        return render_template("login.html")
    
@app.route("/newacc",methods=["POST","GET"])
def newAcc() :
    if request.method=="POST":
   
        app.user=str(request.form["username"])
        passw=str(request.form["password"])
        checkUser=accounts.query.filter_by(username=app.user)
        
        #if user is not in db then it will throw an exception and the user can be added
        try:
           checkUser[0]
           flash('username taken')
           return redirect('/newacc')
           
          
           
        except:
            new_user=accounts(
                username=app.user,
                password=passw
                )
            db.session.add(new_user)
            db.session.commit()
      
            return render_template("home.html",username=app.user)
           
        
    else:       
        return  render_template("newAcc.html")
        
@app.route("/home",methods=["POST","GET"])
def home() :
    if (app.user==""):
        return redirect("/login")
    if request.method=="POST":
        fishName= str(request.form["fish"])
        new_fish=fishLog(
            name=fishName
            )
        db.session.add(new_fish)
        db.session.commit()
        return redirect(url_for('home',username=app.user))
    else:
        fishList= fishLog.query
        print(2)
        return render_template("home.html",fishList=fishList,username=app.user)
    
if __name__== "__main__":
    app.run(debug=False)
