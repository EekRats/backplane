from . import db

component_tags = db.Table('component_tags',
                          db.Column('component_id', db.Integer, db.ForeignKey('component.id')),
                          db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
class System(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(100))
    notes = db.Column(db.Text)
    components = db.relationship('Component', backref='system', lazy=True)

class Component(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    manufacturer = db.Column(db.String(50))
    year = db.Column(db.String(20))
    specs = db.Column(db.Text)
    location = db.Column(db.String(100))
    status = db.Column(db.String(50))
    notes = db.Column(db.Text)
    tags = db.relationship('Tag', secondary=component_tags, backref='components')
    system_id = db.Column(db.Integer, db.ForeignKey('system.id'))