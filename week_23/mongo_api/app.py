from flask import Flask, render_template
from flask_pymongo import PyMongo 

app = Flask(__name__)

#setup mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/shows_db"
mongo = PyMongo(app)

#connect to connection
tv_shows = mongo.db.tv_shows

#READ
@app.route("/")
def index():
    #find all items in db and save to variable
    all_shows = list(tv_shows.find())
    print(all_shows)

    return render_template("index.html",data=all_shows)

#CREATE
@app.route("/insert")
def insert_tvshow():
    #dictionary for new data
    show_name = input('What is the show name?')
    seasons = input('Number of seasons?')
    duration = input('How long is each episode?')
    year = input('What year did it come out?')

    post_data = {'name': show_name,
                'season': seasons,
                'duration': duration,
                'year': year,
                }
    tv_shows.insert_one(post_data)

    return render_template("index.html",data=post_data)

#UPDATE
@app.route("/update")
def update_tvshow():
    show_name = input('What is the show name you want to update?')
    seasons = input('Number of seasons?')
    duration = input('How long is each episode?')
    year = input('What year did it come out?')

    update_show = {'name': show_name}

    post_data = {'$set': {'name': show_name, 
                 'seasons': seasons,
                 'duration': duration,
                 'year': year,
            }}
    tv_shows.update_one(update_show, post_data)
    return render_template("index.html",data=post_data)

#DELETE
@app.route("/delete")
def del_tvshow():
    show_name = input('What is the show name you want to delete?')
    
    post_data = {'name':show_name}
    tv_shows.delete_one(post_data)
    return render_template("index.html",data=post_data)

if __name__ == "__main__":
    app.run(debug=True)