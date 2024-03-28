from flask import Flask,render_template,request,redirect,url_for,session
import mysql.connector
mydb=mysql.connector.connect(host="localhost",user="root",password="system",database="codegnan")
with mysql.connector.connect(host="localhost",user="root",password="system",database="codegnan"):
    cursor=mydb.cursor(buffered=True)
    cursor.execute("create table if not exists registerform(username varchar(50) primary key,mobile varchar(20)unique,email varchar(50) unique,address varchar(50),password varchar(20))")
    cursor.execute("create table if not exists login(username varchar(50),password varchar(40))") 
app=Flask(__name__)
app.secret_key="my secretkey is too secret"
@app.route("/")
def home():
    return render_template('hompage.html')
@app.route("/reg",methods=['POST','GET'])
def register():
    if request.method=='POST':
        username=request.form['username']
        mobile=request.form['mobile']
        address=request.form['address']
        email=request.form['email']
        password=request.form['password']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('insert into registerform values(%s,%s,%s,%s,%s)',[username,mobile,email,address,password])
        mydb.commit()
        cursor.close()
    return render_template('register.html')
@app.route("/login",methods=['POST','GET'])
def login():
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*)from registerform where username=%s && password=%s',[username,password])
        data=cursor.fetchone()[0]
        print(data)
        mydb.commit()
        cursor.close()
        if data==1:
            session['username']=username
            if not session.get(session['username']):
                session[session['username']]={}
            return redirect(url_for('home'))
        else:
            return "invalid username and password"
    return render_template("login.html")
@app.route('/logout')
def logout():
    if session.get('username'):
        session.pop('username')
    return redirect(url_for('login'))
@app.route('/admin')
def admin():
    return render_template('admin.html')
@app.route('/posts',methods=['GET','POST'])
def posts():
    if request.method=="POST":
        title=request.form.get("title")
        content=request.form.get("content")
        slug=request.form.get("slug")
        print(title)
        print(content)
        print(slug)
        cursor=mydb.cursor(buffered=True)
        cursor.execute('INSERT INTO posts(title,content,slug) VALUES(%s,%s,%s)',(title,content,slug))
        mydb.commit()
        cursor.close()
    return render_template('posts.html')
@app.route('/viewpost')
def viewpost():
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select * from posts')
    posts=cursor.fetchall()
    cursor.close()
    return render_template('viewpost.html',posts=posts)
@app.route('/delete_post/<int:id>',methods=['POST'])
def delete_post(id):
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select * from posts where id=%s',(id,))
    post=cursor.fetchone()
    cursor.execute('DELETE FROM posts where id=%s',(id,))
    mydb.commit()
    cursor.close()
    return redirect(url_for('viewpost'))    
@app.route('/update_post/<int:id>',methods=['GET','POST'])
def update_post(id):
    if request.method=="POST":
        title=request.form.get("title")
        content=request.form.get("content")
        slug=request.form.get("slug")
        print(title)
        print(content)
        print(slug)
        cursor=mydb.cursor(buffered=True)
        cursor.execute('UPDATE posts SET title=%s,content=%s,slug=%s WHERE id=%s',(title,content,slug,id))
        mydb.commit()
        cursor.close()
        return redirect(url_for('viewpost'))
    else:
        cursor = mydb.cursor(buffered=True)
        cursor.execute('select * from posts where id=%s',(id,))
        post=cursor.fetchone()
        cursor.close()
        return render_template('update.html',post=post)
app.run()