from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///happiness.db'

db = SQLAlchemy(app)

class HappinessTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    suicide_rank = db.Column(db.Integer, nullable=False)
    happiness_rank = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String(255), nullable=False)
    gdp = db.Column(db.Float, nullable=False)
    life_expectancy = db.Column(db.Float, nullable=False)
    freedom = db.Column(db.Float, nullable=False)
    generosity = db.Column(db.Float, nullable=False)

@app.route('/', methods=["GET"])
def home():
    return render_template("home.html")

@app.route('/about', methods=["GET"])
def about():
    return render_template("about.html")

@app.route('/table', methods=["GET"])
def table():
    table = HappinessTable.query.all()
    d = []
    for row in table:
        row_as_dict = {
            "suicide_rank": row.suicide_rank,
            "happiness_rank": row.happiness_rank,
            "country": row.country,
            "gdp": row.gdp,
            "life_expectancy": row.life_expectancy,
            "freedom": row.freedom,
            "generosity": row.generosity
        }
        d.append(row_as_dict)
    return render_template("table.html", data=d)

@app.route('/api', methods=["GET"])
def api_route():
    table = HappinessTable.query.all()
    d = []
    for row in table:
        row_as_dict = {
            "suicide_rank": row.suicide_rank,
            "happiness_rank": row.happiness_rank,
            "country": row.country,
            "gdp": row.gdp,
            "life_expectancy": row.life_expectancy,
            "freedom": row.freedom,
            "generosity": row.generosity
        }
        d.append(row_as_dict)
    return jsonify(d)
                
if __name__ == '__main__':
    app.run(debug=True)