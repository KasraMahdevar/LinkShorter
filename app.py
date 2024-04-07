import os

from flask import *
from DataBase.DB import db
from Components.LinkShorter import LinkShorter
from Components.LoadURL import LoadURL

app = Flask(__name__)

DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://ufg46e7jsgavhc:p3d4c6a06549f968d59d460d6f46ecd005d0f47b03ce05b9c4573ee500a9aea02@c2dr1dq7r4d57i.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com:5432/d7f8m9fppo3lm7')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


# Routing
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/shorten_link', methods=['POST'])
def shorten_link():
    if request.method == 'GET':
        return redirect(url_for('index'))
    else:
        old_url = request.form.get('url')
        hostname = request.host
        # remove Port from URL
        # if ':' in hostname:
        #     hostname = hostname.split(':')[0]

        link_shorter = LinkShorter(old_url, hostname)
        # default value of length = 7
        new_url = link_shorter.short_url(length_of_url=10)
        return render_template('index.html', new_url=new_url)


@app.route('/<string:path>')
def load_url(path: str):
    hostname = request.host
    full_url = hostname + '/' + path
    loader = LoadURL(url=full_url)
    old_url = loader.load()
    if old_url == 'not found':
        error = 'URL not found!'
        return render_template('index.html', error=error)
    elif old_url == 'expired':
        error = 'URL Expired !!'
        return render_template('index.html', error=error)

    return redirect(old_url)


# before Requests processed
@app.before_request
def create_db():
    db.create_all()
    # db.drop_all()


if __name__ == '__main__':
    app.run()
