
from flask import Flask, render_template,request,redirect,flash,url_for,session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///fish.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']='632h3232ss'

db = SQLAlchemy(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

class fish_Log(db.Model):
   id = db.Column('fish_id', db.Integer, primary_key = True)
   name= db.Column(db.String(50))
   date= db.Column(db.String(50))
   weight=db.Column(db.String(50))
   account_id=db.Column(db.Integer,db.ForeignKey('accounts.account_id'))
def __init__(self, name, account_id):
   self.name = name
   self.account_id=account_id

class accounts(db.Model):
   id = db.Column('account_id', db.Integer, primary_key = True)
   username= db.Column('username' ,db.String(50))
   password=db.Column('password' ,db.String(50))
   fishlogs= db.relationship('fish_Log', backref='log')
   
def __init__(self,username,password,fishlogs):
   self.username = username
   self.password= password
   
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
                   session["id"]=checkUser[0].id
                   return redirect(url_for(".home",username=session['user']))
            except Exception as e:
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
      
            return redirect('/login')
           
        
    else:       
        return  render_template("newAcc.html")
        
@app.route("/home",methods=["POST","GET"])
def home() :
    # an error means the user is not signed in so they are directed to the login page
    try:
        if request.method=="POST":
            if (request.form['submit_button']=='submit'):
                a_id = accounts.query.filter(accounts.username==session['user'])
                a_id=a_id[0].id
                fishName= str(request.form["fish"])
                new_fish=fish_Log(
                    name=fishName,
                    date="5-12-24",
                    weight="24kg",
                    account_id=a_id
                    
                    )
                db.session.add(new_fish)
                db.session.commit()
                return redirect(url_for('home',username=session['user']))
            
            #if the user logs out their session is cleared and they are returned to login screen
            if (request.form['submit_button']=='logout'):
                session.clear()
                return redirect("/login")
        else:
            fishList= fish_Log.query.filter(fish_Log.account_id == session['id'])
            return render_template("home.html",fishList=fishList,username=session['user'])
    except Exception as e:
        print(e)
        return redirect("/login")
    
if __name__== "__main__":
    app.run(debug=False)
