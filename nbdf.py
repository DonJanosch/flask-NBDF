from flask import Flask, render_template, url_for
app = Flask(__name__)

posts = [
    {
        'author':'John Doe',
        'title':'Blog Post 1',
        'content':'First post content',
        'date_posted': '01.01.2019',
    },
    {
        'author':'Jan Macenka',
        'title':'Wirklich wichtig',
        'content':'Den hund noch füttern',
        'date_posted': '01.01.2019',
    },
]

@app.route('/')
@app.route('/home')
def hello():
    return render_template('index.html',posts=posts, title='test')

@app.route('/about')
def about():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True) # TODO: Remove Debug!
