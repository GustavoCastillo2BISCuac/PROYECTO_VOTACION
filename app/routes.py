from flask import render_template, redirect, url_for, jsonify, send_file, session, request
from app.models import Admin, PollingPerson, Section, Vote, PartySection, Party
from app import app, db
from app.pdf_modifier import add_text_to_template
import os

TEMPLATE_PDF_PATH = os.path.join(app.root_path, "static", "files", "template.pdf")
OUTPUT_PDF_PATH = os.path.join(app.root_path, "static", "files", "output.pdf")

# PDF
@app.route('/get_votes_pdf/<int:section_id>')
def create_votes_pdf(section_id):
    try:
        column_cursor = 527
        txts = []
        
        for i in range(10):
            party_counter = PartySection.query.filter_by(party_id=(i+1)).first()
            if party_counter:
                party_counter = party_counter.counter
            else:
                party_counter = 0
            
            txts.append({"x": 100, "y": column_cursor, "content": str(party_counter)})
            column_cursor -= 30

        add_text_to_template(TEMPLATE_PDF_PATH, txts, OUTPUT_PDF_PATH)

        return send_file(OUTPUT_PDF_PATH, as_attachment=True)
    except Exception as e:
        return str(e), 500

# VOTING SYSTEM
@app.route('/')
def index():
    if 'voting_person' in session:
        return render_template('vote.html', parties=Party.query.all())
    return render_template('index.html')

@app.route("/vote_register", methods=['POST'])
def logout_vote():
    if request.form['other_party'] != "":
        from_parties = Party.query.filter_by(party_candidate_name=request.form['other_party']).first()

        if from_parties:
            new_parties_section = PartySection.query.filter_by(section_id=int(session['voting_person_section']), party_id=from_parties.party_id).first()
            
            if new_parties_section:
                new_parties_section.counter = new_parties_section.counter + 1
                db.session.commit()
            else:                
                new_party_section = PartySection(party_id=from_parties.party_id, section_id=int(session['voting_person_section']), counter=1)
                db.session.add(new_party_section)
                db.session.commit()
        else:
            new_party = Party(party_candidate_name=request.form['other_party'], party_name="")
            db.session.add(new_party)
            db.session.commit()

            find_party = Party.query.filter_by(party_candidate_name=request.form['other_party']).first()

            new_party_section = PartySection(section_id=int(session['voting_person_section']), party_id=find_party.party_id ,counter=1)
            db.session.add(new_party_section)
            db.session.commit()

        session.pop("voting_person", None)
        session.pop("voting_person_section", None)

        render_template('index.html')
        return redirect(url_for("index"))

    new_vote = Vote(section_id=int(session['voting_person_section']), person_id=session['voting_person'])
    db.session.add(new_vote)
    db.session.commit()

    new_parties_section = PartySection.query.filter_by(section_id=int(session['voting_person_section']), party_id=request.form['party_selection']).first()

    if new_parties_section:
        new_parties_section.counter = new_parties_section.counter + 1
        db.session.commit()
    else: 
        is_party = Party.query.filter_by(party_id=int(request.form['party_selection'])).first()
        if is_party:
            new_party_section = PartySection(party_id=request.form['party_selection'], section_id=int(session['voting_person_section']), counter=1)
            db.session.add(new_party_section)
            db.session.commit()

    session.pop("voting_person", None)
    session.pop("voting_person_section", None)

    render_template('index.html')
    return redirect(url_for("index"))

@app.route('/', methods=['POST'])
def vote_login():
    person_id = request.form['person_id']
    section_id = request.form['section_id']

    user_voted = Vote.query.filter_by(person_id=person_id).first()
    if user_voted:
        render_template("index.html")
        print("El usuario ya ha votado")
        return redirect(url_for("index"))

    session['voting_person'] = person_id
    session['voting_person_section'] = section_id
    return render_template("vote.html", parties=Party.query.all())


# PUBLIC ADMINISTRATION ADMIN OR POLLING PEOPLE
@app.route("/public_admin")
def public_admin():
    if 'main' in session:
        if session["main"]["login_type"] == "admin":
            parties = Party.query.all()
            polling_people = PollingPerson.query.all()
            parties_section = PartySection.query.all()

            parties_voting = {}
            for party_counter in parties_section:
                party_id = party_counter.party_id
                counter = party_counter.counter

                party = Party.query.filter_by(party_id=party_counter.party_id).first()
                party_name = party.party_name
                party_candidate_name = party.party_candidate_name

                if party_id in parties_voting:
                    parties_voting[party_id]["counter"] += counter
                else:
                    parties_voting[party_id] = {
                        "counter": counter,
                        "party_name": party_name,
                        "party_candidate_name":party_candidate_name
                    }            
            return render_template('admin.html', parties=parties, polling_people=polling_people, parties_voting=parties_voting)
        elif session["main"]["login_type"] == "polling":
            polling_user = PollingPerson.query.filter_by(person_id=session["main"]["person_id"]).first()
            parties_section = PartySection.query.filter_by(section_id=polling_user.section_id).all()
            
            section_info = Section.query.filter_by(section_id=polling_user.section_id).first()
            parties_section_formated = []

            for party_section in parties_section:
                party_info = Party.query.filter_by(party_id=party_section.party_id).first()
                
                parties_section_formated.append({
                    "section_info":{
                        "section_id":section_info.section_id,
                        "section_description":section_info.section_description
                    },
                    "party_info":{
                        "party_id":party_info.party_id,
                        "party_name":party_info.party_name,
                        "party_candidate_name":party_info.party_candidate_name
                    },
                    "counter":party_section.counter
                })
                    
            return render_template('polling.html', parties_section_formated=parties_section_formated, section_info=section_info)
    
    return render_template("main_login.html")

@app.route("/logout_public_admin", methods=['POST'])
def logout_public_admin():
    session.pop("main", None)
    render_template('main_login.html')
    return redirect(url_for("main_login"))

@app.route('/public_admin', methods=['POST'])
def main_login():
    if request.method == 'POST':
        person_id = request.form['person_id']
        password = request.form['password']

        admin_data = Admin.query.filter_by(person_id=person_id).first()
        polling_person = PollingPerson.query.filter_by(person_id=person_id).first()

        if admin_data and admin_data.pwd == password:
            session['main'] = {
                    "person_id": request.form['person_id'],
                    "login_type": "admin"
                }
            return redirect(url_for("public_admin"))
        elif polling_person and polling_person.pwd == password:
            session['main'] = {
                    "person_id": request.form['person_id'],
                    "login_type": "polling"
                }
            return redirect(url_for("public_admin"))
        return jsonify({"status": 404, "reason": "Invalid credentials"})

@app.route('/create-party', methods=['POST'])
def create_party():
    party_name = request.form['party-name']
    party_candidate_name = request.form['party-candidate-name']

    new_party = Party(party_candidate_name=party_candidate_name, party_name=party_name)
    db.session.add(new_party)
    db.session.commit()

    return redirect(url_for("public_admin"))

@app.route('/create-polling-person', methods=['POST'])
def create_polling_person():
    person_id = request.form['person_id']
    section_id = request.form['section_id']
    person_name = request.form['person_name']
    pwd = request.form['pwd']

    new_polling_person = PollingPerson(person_id=person_id, section_id=section_id, person_name=person_name, pwd=pwd)
    db.session.add(new_polling_person)
    db.session.commit()

    return redirect(url_for("public_admin"))


@app.route('/edit-party/<int:party_id>', methods=['GET', 'POST'])
def edit_party(party_id):
    if request.method == 'GET':
        if 'main' in session:
            party = Party.query.filter_by(party_id=party_id).first()
            return render_template('edit_party.html', party=party)
        return redirect(url_for("public_admin"))
    elif request.method == 'POST':
        party = Party.query.filter_by(party_id=party_id).first()
        if party:
            party.party_name = request.form['party-name']
            party.party_candidate_name = request.form['party-candidate-name']            
            db.session.commit()

        return redirect(url_for("public_admin"))
    return jsonify({"code": "403", "reason": "Invalid Access"})

@app.route('/delete-party/<int:party_id>', methods=['GET'])
def delete_party(party_id):
    party = Party.query.filter_by(party_id=party_id).first()
    if party:
        db.session.delete(party)
        db.session.commit()

    #Eliminamos los votos que generaron para ese partido en Parties_Section
    parties_section = PartySection.query.filter_by(party_id=party_id).all()
    
    for party_section in parties_section:
        db.session.delete(party_section)
    db.session.commit()

    return redirect(url_for("public_admin"))

@app.route('/edit-polling/<string:polling_id>', methods=['GET', 'POST'])
def edit_polling(polling_id):
    if request.method == 'GET':
        if 'main' in session:
            polling_user = PollingPerson.query.filter_by(person_id=polling_id).first()
            return render_template('edit_polling.html', polling_user=polling_user)
        return redirect(url_for("public_admin"))
    elif request.method == 'POST':
        polling = PollingPerson.query.filter_by(person_id=polling_id).first()
        if polling:
            polling.section_id = request.form['section_id']
            polling.person_name = request.form['person_name']
            polling.pwd = request.form['pwd']            
            db.session.commit()

        return redirect(url_for("public_admin"))
    return jsonify({"code": "403", "reason": "Invalid Access"})

@app.route('/delete-polling/<string:polling_id>', methods=['GET'])
def delete_polling(polling_id):
    polling_person = PollingPerson.query.filter_by(person_id=polling_id).first()
    if polling_person:
        db.session.delete(polling_person)
        db.session.commit()
    return redirect(url_for("public_admin")) 