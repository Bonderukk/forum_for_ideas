from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Hobby, PostLike
from . import db
import json

views = Blueprint("views", __name__)


@views.route("/wallofhobbies")
def wall():
    like_system = Hobby.query.all()
    system_list = []
    for i in like_system:
        i.zaradenie = True
        system_list.append(int(i.likes))
    print(system_list)

    zoznam_id = []
    for i in range(len(system_list)):
        najviac = max(system_list)
        prvy = Hobby.query.filter_by(likes=najviac, zaradenie=True).first()
        system_list.remove(najviac)
        # zoznam_id.append(int(prvy.id))
        zoznam_id.append(prvy)
        prvy.zaradenie = False
        # print(system_list, "SYSTEM LIST")
        # print(zoznam_id)

    db.session.commit()
    return render_template("wallofhobbies.html", user=current_user,
                           all_hobbies=Hobby.query.all(), zoradovaci_zoznam=zoznam_id)


@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        note = request.form.get("note")

        if len(note) < 1:
            flash("Note is too short!", category="error")

        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added!", category="success")
    return render_template("home.html", user=current_user)


@views.route("/hobby", methods=["GET", "POST"])
@login_required
def hobby():
    if request.method == "POST":
        hob = request.form.get("hobby")
        tit = request.form.get("hobbytitle")

        if len(hob) < 1:
            flash("Too short!", category="error")

        else:
            new_hob = Hobby(data=hob, title=tit, likes=0, user_id=current_user.id)
            # new_like = PostLike()
            db.session.add(new_hob)
            db.session.commit()
            flash("Hobby added to our database!", category="success")
    return render_template("hobby.html", user=current_user)


psycho = None


@views.route("/wallofhobbies", methods=["GET", "POST"])
@login_required
def like():
    if request.method == "POST":

        psycho = request.form.get("idecko")
        result = Hobby.query.filter_by(id=psycho).first()

        test_like = PostLike.query.filter_by(user_id=current_user.id, post_id=result.id).first()

        if test_like == None:
            novy_like = PostLike(user_id=current_user.id, post_id=result.id)
            db.session.add(novy_like)
            db.session.commit()
            print(novy_like.post_id, "VYTVORIL SA NOVY", novy_like.user_id)

        else:
            if test_like.user_id == current_user.id and test_like.post_id == result.id:
                db.session.delete(test_like)
                db.session.commit()

                print("VYMAZAL SA NOVY")

        total_likes = PostLike.query.filter_by(post_id=result.id).count()
        print(total_likes, "TESTTESTTEST")
        result.likes = total_likes

        like_system = Hobby.query.all()
        system_list = []
        for i in like_system:
            i.zaradenie = True
            system_list.append(int(i.likes))
        print(system_list)

        zoznam_id = []
        for i in range(len(system_list)):
            najviac = max(system_list)
            prvy = Hobby.query.filter_by(likes=najviac, zaradenie=True).first()
            print(prvy, "MFKIN TEEEEEESDT")
            system_list.remove(najviac)
            # zoznam_id.append(int(prvy.id))
            zoznam_id.append(prvy)
            prvy.zaradenie = False
            print(system_list, "SYSTEM LIST")
            print(zoznam_id)

        db.session.commit()

    return render_template("wallofhobbies.html", user=current_user, new_likes=result.likes,
                           all_hobbies=Hobby.query.all(), zoradovaci_zoznam=zoznam_id, nahrada=True)


@views.route("/delete-note", methods=["POST"])
def delete_note():
    note = json.loads(request.data)
    noteId = note["noteId"]
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})
