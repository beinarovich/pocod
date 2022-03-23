from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key = True) # Уникальный идентификатор
    title = db.Column(db.String(150), nullable = False) # Название статьи
    intro = db.Column(db.String(350), nullable = False) # Краткая аннотация к статье
    text = db.Column(db.Text, nullable = False) # Текст статьи
    tag = db.Column(db.String(30), nullable = False) # Тематика статьи
    author = db.Column(db.String(40), nullable = False) # ФИО автора статьи
    date = db.Column(db.DateTime, default = datetime.utcnow())  # Дата создания статьи
    
    def __repr__(self):
        return 'Article %r' % self.id 

@app.route('/')
@app.route('/index')
def index():
    articles = Article.query.order_by(Article.id).all()
    return render_template("index.html", articles=articles)

@app.route('/success_create')
def sc():
    return render_template("success_create.html")

@app.route('/fall_create')
def fc():
    return render_template("fall_create.html")

@app.route('/success_delete')
def sd():
    return render_template("success_delete.html")

@app.route('/fall_delete')
def fd():
    return render_template("fall_delete.html")

@app.route('/success_edit')
def se():
    return render_template("success_edit.html")

@app.route('/<int:id>/fall_edit')
def fe(id):
    article = Article.query.get(id)
    return render_template("fall_edit.html", article = article)

@app.route('/create', methods = ['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        tag = request.form['tag']
        author = request.form['author']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, tag=tag, author=author, intro=intro, text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/success_create')
        except:
            return redirect('/fall_create')
    else:
        return render_template("create.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/<int:id>')
def detail(id):
    article = Article.query.get(id)
    return render_template("article.html", article=article)

@app.route('/<int:id>/delete')
def delete(id):
    article = Article.query.get_or_404(id)
    try:
            db.session.delete(article)
            db.session.commit()
            return redirect('/success_delete')
    except:
            return redirect('/fall_delete')

@app.route('/<int:id>/edit', methods = ['POST', 'GET'])
def edit(id): 
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.tag = request.form['tag']
        article.author = request.form['author']
        article.intro = request.form['intro']
        article.text = request.form['text']
      
        try:
            db.session.commit()
            return redirect("/success_edit")
        except:
            return redirect('/fall_edit', article = article)
    else:
        return render_template("edit.html", article = article)

if __name__ == "__main__":
     app.run(debug=True)