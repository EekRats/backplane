from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired

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
        ('SYSTEM', 'SYSTEM'),
        ('PERIPHERAL', 'PERIPHERAL'),
        ('OTHER', 'OTHER')
    ], validators=[DataRequired()])
    manufacturer = StringField('Manufacturer')
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
    submit = SubmitField('Add Component')