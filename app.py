from flask import Flask, render_template, request, redirect
from cs50 import SQL
from helpers import fun

app = Flask(__name__)
db = SQL("sqlite:///questions.db")

N = 0
LEVEL = 1
SCORE = 0
CORRECT_STREAK = 0
WRONG_STREAK = 0
Q_NO = 0
LIFE = 3

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/quiz", methods=["GET","POST"])
def quiz():
    if request.method == "GET":
        return redirect("/")
    else:
        global N
        global LEVEL
        global SCORE
        global CORRECT_STREAK
        global WRONG_STREAK
        global Q_NO
        global LIFE

        mode = request.form.get("mode")
        if mode == "ten":
            N = 10
            return redirect("/game")
        elif mode == "twenty":
            N = 20
            return redirect("/game")
        elif mode == "survival":
            N = 7176
            return redirect("/survival")
        else:
            N = 0
            return redirect("/")



@app.route("/game", methods=["GET","POST"])
def game():
    global N
    global LEVEL
    global SCORE
    global CORRECT_STREAK
    global WRONG_STREAK
    global Q_NO
    color = ""

    # Re-initialize score and level for new game
    if request.method == "GET":
        if N == 0:
            return redirect("/")
        SCORE = 0
        LEVEL = 1
        CORRECT_STREAK = 0
        Q_NO = 0

    else:
        print(f"{request.form.get('ans')} vs {request.form.get('a')}")
        if request.form.get("ans") == request.form.get("a"):

            color = "green"
            CORRECT_STREAK += 1
            if LEVEL == 1:
                SCORE += 1
            elif LEVEL == 2:
                SCORE += 2
            elif LEVEL == 3:
                SCORE += 4
            else:
                SCORE += 6
        else:

            color = "red"
            CORRECT_STREAK = 0
            if not LEVEL == 1:
                LEVEL -= 1

        if CORRECT_STREAK == 3:
            if not LEVEL == 4:
                LEVEL += 1
                CORRECT_STREAK = 0


    if N > 0:
        Q_NO += 1
        N -= 1
        if LEVEL == 1:
            x = fun("easy_cap", 35)
            print(f"Q: {x[0]}  A:{x[1]}")
            return render_template("quiz.html", x=x, q=Q_NO, s=SCORE, l=LEVEL, c=color)
        elif LEVEL == 2:
            x = fun("med_cap", 25)
            print(f"Q: {x[0]}  A:{x[1]}")
            return render_template("quiz.html", x=x, q=Q_NO, s=SCORE, l=LEVEL, c=color)
        elif LEVEL == 3:
            x = fun("hard_cap", 36)
            print(f"Q: {x[0]}  A:{x[1]}")
            return render_template("quiz.html", x=x, q=Q_NO, s=SCORE, l=LEVEL, c=color)
        else:
            x = fun("god_cap", 89)
            print(f"Q: {x[0]}  A:{x[1]}")
            return render_template("quiz.html", x=x, q=Q_NO, s=SCORE, l=LEVEL, c=color)

    else:
        return render_template("score.html", score=SCORE)


@app.route("/survival", methods=["GET","POST"])
def survival():
    global N
    global LEVEL
    global SCORE
    global CORRECT_STREAK
    global WRONG_STREAK
    global Q_NO
    global LIFE
    color = ""

    # Re-initialize score and level for new game
    if request.method == "GET":
        SCORE = 0
        LEVEL = 1
        CORRECT_STREAK = 0
        Q_NO = 0
        LIFE = 3

    else:
        print(f"{request.form.get('ans')} vs {request.form.get('a')}")
        if request.form.get("ans") == request.form.get("a"):

            color = "green"
            CORRECT_STREAK += 1
            if LEVEL == 1:
                SCORE += 1
            elif LEVEL == 2:
                SCORE += 2
            elif LEVEL == 3:
                SCORE += 4
            else:
                SCORE += 6
        else:

            color = "red"
            CORRECT_STREAK = 0
            LIFE -= 1
            if not LEVEL == 1:
                LEVEL -= 1

        if CORRECT_STREAK == 3:
            if not LEVEL == 4:
                LEVEL += 1
                CORRECT_STREAK = 0

        if LIFE < 1:
            return render_template("score.html", score=SCORE)



    if N == 7176:
        Q_NO += 1
        if LEVEL == 1:
            x = fun("easy_cap", 35)
            print(f"Q: {x[0]}  A:{x[1]}")
            return render_template("survival.html", x=x, q=Q_NO, s=SCORE, l=LEVEL, life=LIFE, c=color)
        elif LEVEL == 2:
            x = fun("med_cap", 25)
            print(f"Q: {x[0]}  A:{x[1]}")
            return render_template("survival.html", x=x, q=Q_NO, s=SCORE, l=LEVEL, life=LIFE, c=color)
        elif LEVEL == 3:
            x = fun("hard_cap", 36)
            print(f"Q: {x[0]}  A:{x[1]}")
            return render_template("survival.html", x=x, q=Q_NO, s=SCORE, l=LEVEL, life=LIFE, c=color)
        else:
            x = fun("god_cap", 89)
            print(f"Q: {x[0]}  A:{x[1]}")
            return render_template("survival.html", x=x, q=Q_NO, s=SCORE, l=LEVEL, life=LIFE, c=color)

    else:
        return redirect("/high_score")



@app.route("/score", methods=["GET","POST"])
def score():

    if request.method == "GET":
        return redirect("/high_scores")

    else:
        global Q_NO
        global SCORE
        name = request.form.get("name")

        if name == "":
            name = "Anon"

        if N == 7176:
            db.execute("INSERT INTO survival (name,score) VALUES (?,?)", name, SCORE)
            return redirect("/high_scores")
        else:
            if Q_NO == 10:
                db.execute("INSERT INTO ten (name,score) VALUES (?,?)", name, SCORE)
            if Q_NO == 20:
                db.execute("INSERT INTO twenty (name,score) VALUES (?,?)", name, SCORE)
            return redirect("/high_scores")


@app.route("/high_scores")
def high_scores():
    ten = db.execute("SELECT name,score FROM ten ORDER BY score DESC, id DESC LIMIT 20")
    twenty = db.execute("SELECT name,score FROM twenty ORDER BY score DESC, id DESC LIMIT 20")
    survival = db.execute("SELECT name,score FROM survival ORDER BY score DESC, id DESC LIMIT 20")
    db.execute("DELETE FROM ten WHERE id NOT IN (SELECT id FROM ten ORDER BY score DESC, id DESC LIMIT 20)")
    db.execute("DELETE FROM twenty WHERE id NOT IN (SELECT id FROM twenty ORDER BY score DESC, id DESC LIMIT 20)")
    db.execute("DELETE FROM survival WHERE id NOT IN (SELECT id FROM survival ORDER BY score DESC, id DESC LIMIT 20)")
    return render_template("high_scores.html", ten=ten, twenty=twenty, survival=survival)