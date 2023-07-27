
from flask import Flask, render_template,request,redirect,flash,url_for,session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///fish.sqlite3'
app.config['SECRET_KEY']='632h3232ss'
db = SQLAlchemy(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

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

@app.route("/login",methods=["GET","POST"])
def login():
         
    if(request.method=="POST"):
        if (request.form['submit_button']=='login'):
            session['user']=str(request.form["username"])
            passw=str(request.form["password"])
            checkUser=accounts.query.filter_by(username=session['user'],password=passw)
            
                #if user is not in db then it will throw an exception and the user can be added
            try:
                   checkUser[0]
                   return redirect(url_for(".home",username=session['user']))
            except:
                flash("password or username incorrect")
                return redirect('/login')
        if (request.form['submit_button']=='signup'):
            return redirect('/newacc')
    else:
       return render_template("login.html")
    
@app.route("/newacc",methods=["POST","GET"])
def newAcc() :
    if request.method=="POST":
   
        session['user']=str(request.form["username"])
        passw=str(request.form["password"])
        
        #checks to make username or password are not empty
        if( str(request.form["username"])=="" or passw==""):
            flash("username or password feild is empty")
            return  render_template("newAcc.html")
        
        checkUser=accounts.query.filter_by(username=session['user'])
        
        #if user is not in db then it will throw an exception and the user can be added
        try:
           checkUser[0]
           flash('username taken')
           return redirect('/newacc')
           
          
           
        except:
            new_user=accounts(
                username=session['user'],
                password=passw
                )
            db.session.add(new_user)
            db.session.commit()
      
            return redirect(url_for(".home",username=session['user']))
           
        
    else:       
        return  render_template("newAcc.html")
        
@app.route("/home",methods=["POST","GET"])
def home() :
    # an error means the user is not signed in so they are directed to the login page
    try:
        if request.method=="POST":
            if (request.form['submit_button']=='submit'):
                fishName= str(request.form["fish"])
                new_fish=fishLog(
                    name=fishName
                    )
                db.session.add(new_fish)
                db.session.commit()
                return redirect(url_for('home',username=session['user']))
            
            #if the user logs out their session is cleared and they are returned to login screen
            if (request.form['submit_button']=='logout'):
                session.clear()
                return redirect("/login")
        else:
            fishList= fishLog.query
            return render_template("home.html",fishList=fishList,username=session['user'])
    except:
        return redirect("/login")
    
if __name__== "__main__":
    app.run(debug=False)
