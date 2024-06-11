from app import db

class Admin(db.Model):
    __tablename__ = 'admins'
    person_id = db.Column(db.String(255), primary_key=True)
    pwd = db.Column(db.String(255), nullable=False)

class PollingPerson(db.Model):
    __tablename__ = 'polling_people'
    person_id = db.Column(db.String(255), primary_key=True)
    section_id = db.Column(db.Integer, nullable=False)
    person_name = db.Column(db.String(255))
    pwd = db.Column(db.String(255), nullable=False)

class Section(db.Model):
    __tablename__ = 'sections'
    section_id = db.Column(db.Integer, primary_key=True)
    section_description = db.Column(db.String(255), nullable=False)

class Vote(db.Model):
    __tablename__ = 'votes'
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, nullable=False)
    person_id = db.Column(db.String(255), nullable=False)

class PartySection(db.Model):
    __tablename__ = 'parties_section'
    section_id = db.Column(db.Integer, db.ForeignKey('sections.section_id'), primary_key=True)
    party_id = db.Column(db.Integer, primary_key=True)
    counter = db.Column(db.Integer)

class Party(db.Model):
    __tablename__ = 'parties'
    party_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    party_name = db.Column(db.String(255), nullable=False)
    party_candidate_name = db.Column(db.String(255), nullable=False)
