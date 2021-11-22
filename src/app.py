from flask import *
import sys
sys.path.append('C:Users\rootuser\Desktop')
import sqlite3
import tweepy
from textblob import TextBlob
app = Flask(_name_)
app.config["DEBUG"] = True
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
cons_key = "zJQyiylJYFuutBTOzomm2ZgDc"
cons_sec = "gPXYZSZ7jVqjTOIG48p4CYzs7fx9fmaWHFPnmSMp4DF10Bla3D"
acc_token = "1269151933559762945-wZYKQZRbSRaTuDkxW29PnLVaTUJmea"
acc_sec = "uGyK2OpmhiCyE20b7D0b26adNOosmdDT0FPmtCsLjHqqt"
auth = tweepy.OAuthHandler(cons_key, cons_sec)
auth.set_access_token(acc_token, acc_sec)
api = tweepy.API(auth)
@app.route('/')
def hello_world():
return render_template('home1.html')
@app.route('/signup', methods=['GET', 'POST'])
def home():
msg = None;
if(request.method == "POST"):
if(request.form["username"]!= "" and request.form["password"]!= ""):
username = request.form["username"]
password = request.form["password"]
conn = sqlite3.connect("signup.db")
c = conn.cursor()
c.execute("INSERT INTO person VALUES('"+username+"', '"+password+"')")
flash("Account created successfully!!!!! Now you can Login")
conn.commit()
conn.close()
return redirect(url_for('hello_world'))
else:
flash("you can't create account")
return render_template("signup.html",msg=msg)
@app.route("/login", methods=['GET', 'POST'])
def login():
if request.method == 'POST':
username = request.form["username"]
password = request.form["password"]
with sqlite3.connect("signup.db") as db:
cursor = db.cursor()
find_user = ("SELECT * FROM person WHERE username = ? AND password = ?")
cursor.execute(find_user,[(username),(password)])
results = cursor.fetchall()
if results:
for i in results:
flash("Login successfull")
return redirect(url_for('hello123'))
else:
flash("Invalid username or password!!!!!Try Again")
return redirect(url_for('login'))
return render_template("login.html")
@app.route('/home')
def hello123():
return render_template('home.html')
positive1=[]
@app.route('/results', methods=['GET', 'POST'])
def show_result():
if request.method == 'POST':
result = request.form['keyword']
neutral, positive, negative = 0, 0, 0
tweetData = {}
id=0
tweets = api.search(q="#"+result, count=100, rpp=1500)
for tweet in tweets:
blob = TextBlob(tweet.text)
polarity = blob.sentiment.polarity
if polarity == 0:
tweetData[id] = {
'text': tweet.text,
'polarity': round(polarity, 2),
}
neutral += 1
elif polarity > 0:
tweetData[id] = {
'text': tweet.text,
'polarity': round(polarity, 2),
}
positive += 1
elif polarity < 0:
tweetData[id] = {
'text': tweet.text,
'polarity': round(polarity, 2),
}
negative += 1
id += 1
if (positive > negative) and (positive > neutral):
outcome = 'positive'
msg = "Outcome: Over the analysis the result falls on a positive edge. :)"
elif (negative > neutral):
outcome = 'negative'
msg = "Outcome: Over the analysis the result falls on the negative edge. :("
else:
outcome = 'neutral'
msg = "Outcome: Over the analysis, the results are claimed to be neutral. :| "
values = [positive, negative, neutral]
positive1.append(values[0])
labels = ["positive", "negative", "neutral"]
return render_template('result.html', msg=msg, labels=labels, values=values, keyword=result, 
outcome=outcome, tweetData=tweetData)
app.run()
