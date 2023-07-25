
from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///fish.sqlite3'
db = SQLAlchemy(app)
class fishLog(db.Model):
   id = db.Column('fish_id', db.Integer, primary_key = True)
   name= db.Column('name' ,db.String(50))
def __init__(self, name, city, addr,pin):
   self.name = name
 
db.create_all()
@app.route("/",)
def login() :
        return render_template("login.html")
    
@app.route("/home",methods=["POST","GET"])
def home() :
    if request.method=="POST":
        fishName= str(request.form["fish"])
        new_fish=fishLog(
            name=fishName
            )
        db.session.add(new_fish)
        db.session.commit()
        return redirect('/home')
    else:
        fishList= fishLog.query
        return render_template("home.html",fishList=fishList)
    
if __name__== "__main__":
    app.run(debug=False)