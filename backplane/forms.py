from flask_wtf import FlaskForm
from .models import System
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField

class ComponentForm(FlaskForm):
    part_id = StringField('Part ID', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    type = SelectField('Type', choices=[
        ('CPU', 'CPU'),
        ('GPU', 'GPU'),
        ('RAM', 'RAM'),
        ('MOBO', 'MOBO'),
        ('SOUNDCARD', 'SOUNDCARD'),
        ('MODEM', 'MODEM'),
        ('LAN', 'LAN'),
        ('STORAGE', 'STORAGE'),
        ('CD', 'CD'),
        ('FLOPPYDSK', 'FLOPPYDSK'),
        ('FLOPPYDRV', 'FLOPPYDRV'),
        ('KEYBOARD', 'KEYBOARD'),
        ('MOUSE', 'MOUSE'),
        ('MONITOR', 'MONITOR'),
        ('PERIPHERAL', 'PERIPHERAL'),
        ('OTHER', 'OTHER')
    ], validators=[DataRequired()])
    manufacturer = StringField('Manufacturer')
    year = StringField('Year/Date')
    specs = TextAreaField('Specs')
    location = StringField('Location')
    status = SelectField('Status', choices=[
        ('In Use', 'In Use'),
        ('In Storage', 'In Storage'),
        ('Spare', 'Spare'),
        ('Broken', 'Broken'),
        ('Unknown', 'Unknown')
    ])
    notes = TextAreaField('Notes')

    def get_systems():
        return System.query.order_by(System.name).all()
    
    system_id = QuerySelectField(
        'Assigned System',
        query_factory=get_systems,
        allow_blank=True,
        get_label='name'
    )

    submit = SubmitField('Add Component')

class SystemForm(FlaskForm):
    name = StringField('System Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    location = StringField('Location')
    notes = TextAreaField('Notes')
    submit = SubmitField('Add System')