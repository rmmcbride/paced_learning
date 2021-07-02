from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from datetime import datetime
import pandas as pd

from bokeh.embed import components
from bokeh.plotting import figure, output_file
from bokeh.models import ColumnDataSource

app = Flask(__name__)
app.config.from_pyfile('config.py')


engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], future=True)
Session = sessionmaker(bind=engine, future=True)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class CardModel(db.Model):
    __tablename__ = 'card'

    id = db.Column(db.Integer(), primary_key=True)
    topic = db.Column(db.String())
    question = db.Column(db.String())
    answer = db.Column(db.String())
    difficulty = db.Column(db.Integer())
    last_date = db.Column(db.Date)
    score = db.Column(db.Integer())

    def __init__(self, topic, question, answer, difficulty, last_date, score):
        self.id = None
        self.topic = topic
        self.question = question
        self.answer = answer
        self.difficulty = difficulty
        self.last_date = last_date
        self.score = score


def update_card_ranks(diff, num_days):
    """
    Updates all scores before we finish
    :return:
    """
    # start of with a simple score
    return diff + diff * num_days


def get_topics():
    with Session() as session:
        res = session.query(CardModel.topic).distinct()
    topics = []
    for row in res:
        topics.append(row[0])
    return topics


@app.route('/question', methods=['POST', 'GET'])
def get_question():
    topic = request.form["topic"].strip()
    with Session() as session:
        card = session.query(CardModel).where(
            CardModel.topic == topic).order_by(CardModel.score.desc()).first()
    return render_template("question.html", question=card.question.strip(), topic=topic.strip(), id=card.id)


@app.route('/answer', methods=['POST', 'GET'])
def get_answer():
    card_id = request.form["question_id"]
    with Session() as session:
        card = session.query(CardModel).where(CardModel.id == card_id).first()
    return render_template("answer.html", answer=card.answer.strip(), topic=request.form["topic"].strip(), id=card.id)


@app.route('/difficulty', methods=['POST', 'GET'])
def update_card_score():
    diff = request.form["difficulty"]
    access_date = datetime.date(datetime.now())
    card_id = request.form["id"]
    with Session() as session:
        card = session.query(CardModel).where(CardModel.id == card_id).first()
        card.last_date = access_date
        card.difficulty = diff
        # Update the card difficulty, its last access date and score
        current = datetime.date(datetime.now())
        card.score = update_card_ranks(card.difficulty, (current - card.last_date).days)
        session.add(card)
        session.commit()
    return render_template("review.html", topics=get_topics())


@app.route('/review')
def render():
    topics = get_topics()
    return render_template("review.html", topics=topics)


@app.route('/add', methods=['POST', 'GET'])
def begin_adding_card():
    return render_template("add.html")


@app.route('/add_card', methods=['POST', 'GET'])
def add_card():
    # Set the difficulty and num days to a relatively high value to give a new card a relatively high rank and thus
    # more likely to be reviewed again after adding it
    default_difficulty = 5
    default_num_days = 10
    # TODO: Add some type checking
    with Session() as session:
        card = CardModel(topic=request.form['topic'],
                         question=request.form['question'].strip(),
                         answer=request.form['answer'].strip(),
                         difficulty=default_difficulty,
                         last_date=datetime.date(datetime.now()),
                         score=update_card_ranks(default_difficulty, default_num_days))
        session.add(card)
        session.commit()
    return render_template("contents.html")


@app.route('/edit', methods=['POST', 'GET'])
def edit_card():
    card_id = request.form['id']
    with Session() as session:
        card = session.query(CardModel).where(CardModel.id == card_id).first()
    return render_template("edit.html", id=card.id, topic=card.topic.strip(), question=card.question.strip(),
                           answer=card.answer.strip(), difficulty=card.difficulty)


@app.route('/submit', methods=['POST', 'GET'])
def update_card():
    card_id = request.form["id"]
    with Session() as session:
        card = session.query(CardModel).where(CardModel.id == card_id).first()
        card.topic = request.form['topic'].strip()
        card.question = request.form['question'].strip()
        card.answer = request.form['answer'].strip()
        card.difficulty = request.form['difficulty']
        card.last_date = datetime.date(datetime.now())
        current = datetime.date(datetime.now())
        card.score = update_card_ranks(card.difficulty, (current - card.last_date).days)
        session.add(card)
        session.commit()
    return render_template("contents.html")


def get_difficulty_rating_data():
    num = func.count('*').label('c')
    with Session() as session:
        res = session.query(CardModel.difficulty, num).group_by(CardModel.difficulty)

    diff = []
    num = []
    for each in res:
        diff.append(each[0])
        num.append(each[1])
    actual = pd.DataFrame(data={'difficulty': diff, 'count': num})

    difficulty_score_map = {'5': 'Very Hard',
                            '4': 'Hard',
                            '3': 'OK',
                            '2': 'Easy',
                            '1': 'Very Easy'}
    diff_map = pd.DataFrame.from_dict(difficulty_score_map, orient='index')
    diff_map = diff_map.reset_index()
    diff_map.columns = ['difficulty', 'category']
    diff_map['difficulty'] = diff_map['difficulty'].astype('int')
    diff_final = diff_map.merge(actual, how='left')
    diff_final = diff_final.fillna(0)
    diff_final['count'] = diff_final['count'].astype(int)
    return diff_final


def get_plot_data(df):
    output_file('vbar.html')
    source = ColumnDataSource(df)

    p = figure(x_range=list(df["category"]), plot_width=400, plot_height=400)
    p.vbar(x="category", width=0.5, bottom=0,
           top="count", source=source, color="firebrick")
    return p


@app.route('/performance', methods=['POST', 'GET'])
def get_summary_stats():
    diff_data = get_difficulty_rating_data()
    plot_data = get_plot_data(diff_data)
    with Session() as session:
        num_cards = session.query(CardModel.id).count()
    with Session() as session:
        rev_date = session.query(func.max(CardModel.last_date)).first()

    script, div = components(plot_data)

    return render_template("performance.html", review_date=rev_date[0].strftime("%d %b %Y"), num_cards=num_cards,
                           the_div=div, the_script=script)


@app.route('/contents')
def render_contents():
    current = datetime.date(datetime.now())
    with Session() as session:
        # Update the card ranks
        # TODO: Improve the approach below
        cards = session.query(CardModel).all()
        for card in cards:
            card.score = update_card_ranks(card.difficulty, (current - card.last_date).days)
            session.add(card)
            session.commit()
    return render_template("contents.html")


@app.route('/')
def home():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
