
from flask import Flask, render_template,request,redirect,flash,url_for,session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
import hashlib
from werkzeug.utils import secure_filename
import os
import uuid as uuid

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///fish.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']='632h3232ss'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'webp','jfif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

db = SQLAlchemy(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

UPLOAD_FOLDER ='static/images'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
Session(app)

class fish_Log(db.Model):
   id = db.Column('fish_id', db.Integer, primary_key = True)
   name= db.Column(db.String(50))
   image= db.Column(db.String(50))
   date= db.Column(db.String(50))
   weight=db.Column(db.String(50))
   length=db.Column(db.String(50))
   lure=db.Column(db.String(50))
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
   
#db.create_all()
@app.route("/",methods=["POST","GET"])
@app.route("/login",methods=["GET","POST"])
def login():
   
#check to see if user is logged in and if they are bring them to the home page
#and if not do nothing
    try:
      session['user']
      return redirect(url_for("home",username=session['user']))
    except:
       pass
       
    
        
    if(request.method=="POST"):
        if (request.form['submit_button']=='login'):
            session['user']=str(request.form["username"]).strip()
            passw=str(request.form["password"]).strip()
            passw=hashlib.sha256(passw.encode('utf-8')).hexdigest()
            checkUser=accounts.query.filter_by(username=session['user'],password=passw)
            
                #if user is not in db then it will throw an exception and the user can be added
            try:
                   print(checkUser[0])
                   session["id"]=checkUser[0].id
                   return redirect(url_for("home",username=session['user']))
            except Exception as e:
                session.clear()
                flash("password or username incorrect")
                return render_template("login.html")
        if (request.form['submit_button']=='signup'):
            return redirect('/newacc')
    else:
       return render_template("login.html")
    
@app.route("/newacc",methods=["POST","GET"])
def newAcc() :
    if request.method=="POST":

        user=str(request.form["username"]).strip()
        passw=str(request.form["password"]).strip()
        passw=hashlib.sha256(passw.encode('utf-8')).hexdigest()
        
        #checks to make username or password are not empty
        if( str(request.form["username"])=="" or passw==""):
            flash("username or password feild is empty")
            return  render_template("newAcc.html")
        
        checkUser=accounts.query.filter_by(username=user)
        
        #if user is not in db then it will throw an exception and the user can be added
        try:
           
           checkUser[0]
           flash('username taken')
           #session.clear()
           return redirect('/newacc')
           
          
           
        except:
            new_user=accounts(
                username=user,
                password=passw
                )
            db.session.add(new_user)
            db.session.commit()
      
            return redirect('/login')
           
        
    else:       
        return  render_template("newAcc.html")

@app.route("/logout")
def logout():
            #if the user logs out their session is cleared and they are returned to login screen
                session.clear()
                return redirect("/login")

@app.route("/lookup",methods=["POST","GET"])
def lookup():
    users=""
    if request.method=="POST":
      
      
        try:
            s =str( request.form["term"]).strip()
            users = accounts.query.filter(accounts.username.like('%'+s+'%'))
            term=s
            if(s==""):
                 flash("Search Box is empty please input a username")
                 return redirect(url_for('lookup',users=[]))
            elif(users[0].username==""):
                flash("No results found")
                return redirect(url_for('lookup',users=[]))
            return render_template("lookup.html",users=users)
        except Exception as e:
            flash("No results found")

            return redirect(url_for('lookup',users=[]))
   
    return render_template("lookup.html",users=users)
@app.route("/delete/<int:id>")
def delete(id):
    entry=fish_Log.query.get_or_404(id)
    try:
        file = entry.image.replace("images/","")  
        location = app.config['UPLOAD_FOLDER']
        path = os.path.join(location, file)  
        os.remove(path)
        db.session.delete(entry)
        db.session.commit()
        flash("Entry Deleted")
        return redirect(url_for('home',username=session['user']))
    except Exception as e:
        flash(e)
        return redirect(url_for('home',username=session['user']))

@app.route("/home",methods=["POST","GET"])
def home() :
    # an error means the user is not signed in so they are directed to the login page
    try:
        if request.method=="POST":
            
            if (request.form['submit_button']=='submit'):
                a_id = accounts.query.filter(accounts.username==session['user'])
                a_id=a_id[0].id
                fishName= str(request.form["fish"])
                if(fishName==""):
                    flash("No fish name Inputed, please enter a fish name")
                    return redirect("home")
                d= str(request.form["date"])
                w= str(request.form["weight"])
                length= str(request.form["length"])
                lure= str(request.form["lure"])
                pic=(request.files["image"])
                if(pic.filename==""):
                    flash("No image chosen, please choose an image")
                    return redirect("home")
                elif(allowed_file(pic.filename)==False):
                    flash("File type not supported, supported file types are png, jpg, jpeg, webp, and jfif")
                    return redirect("home")
                    
                pic_filename=secure_filename(pic.filename)
                #adds uuid to each pic so each filename is unique when stored
                pic_name=str(uuid.uuid1())+"_"+pic_filename
                pic.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
                #if date or weight is empty they are marked as undefined
                if(d==""):
                    d="Not Specified"
                if(w==""):
                    w="Not Specified"
                if(length==""):
                    length="Not Specified"
                if(lure==""):
                    lure="Not Specified"
                    
                new_fish=fish_Log(
                    name=fishName,
                    image="images/"+str(pic_name),
                    date=d.strip(),
                    weight=w.strip(),
                    length=length.strip(),
                    lure=lure.strip(),
                    account_id=a_id,

                    )
                db.session.add(new_fish)
                db.session.commit()
                flash("Fish added Successfully")
                return redirect(url_for('home',username=session['user']))
          
            elif (request.form['submit_button']=='find_user'):
                user=str(request.form["user"])
                if(user==""):
                    flash("User input is blank, please input a username")
                    return redirect(url_for('home',username=session['user']))
                try:
                      return redirect(url_for('profile',user=user))
                except Exception as e:
                    
                    flash(e)
                    return redirect(url_for('home',username=session['user']))
                   
        else:
            
            fishList= fish_Log.query.filter(fish_Log.account_id == session['id'])
            numFish=fishList.count()
            return render_template("home.html",fishList=fishList,username=session['user'],numFish=numFish)

    except Exception as e:
        return redirect("/login")
        
@app.route("/profile/<user>",methods=["GET"])
def profile(user) :

    user=accounts.query.filter_by(username=user)
    try:
        
        userid=user[0].id
        user=user[0].username
        fishList= fish_Log.query.filter(fish_Log.account_id == userid)
        numFish=fishList.count()
        return render_template("profile.html",fishList=fishList,user=user,numFish=numFish)
    except:
        flash("could not find user")
        return redirect(url_for('home',username=session['user']))
if __name__== "__main__":
    app.run(debug=False)
