from flask import Flask, render_template, request, redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from jinja2 import Template


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3309/doto'
db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    duedate = db.Column(db.Date, default=datetime.now().date())
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/about',methods = ['GET'])
def about_fun():
    return render_template('about.html', data="ssS")


@app.route('/task',methods = ['GET'])
def task_fun():
    allTodo = Todo.query.all()
    return render_template('task.html', allTodo=allTodo)

@app.route('/',methods = ['GET','POST'])
def main_fun():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        duedate = request.form['duedate']
        if title == "":
            return  render_template('error.html', data="Please enter task details before saving !")
        if duedate == "":
            duedate = datetime.now().date()
        todo = Todo(title=title, desc=desc, duedate=duedate)
        db.session.add(todo)
        db.session.commit()
        
    

    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        duedate = request.form['duedate']
        if duedate == "":
            duedate = datetime.now().date()
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        todo.duedate = duedate
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/task")  
  

if __name__ == '__main__':
    app.run(debug=True)
