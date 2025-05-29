from flask_wtf import FlaskForm
from .models import System
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField

ALL_TYPE_CHOICES = [
    ('BIOS', 'BIOS Chip'),
    ('CASE', 'Case/Chassis'),
    ('FAN', 'Case Fan'),
    ('CPU', 'CPU'),
    ('CFAN', 'CPU Cooler'),
    ('MOBO', 'Motherboard'),
    ('PSU', 'Power Supply'),
    ('CD', 'CD'),
    ('FLP5', '5.25" Floppy Disk'),
    ('FLP3', '3.5" Floppy Disk'),
    ('FDD5', '5.25" Floppy Drive'),
    ('FDD3', '3.5" Floppy Drive'),
    ('FLSH', 'Flash'),
    ('HDD', 'Hard Drive'),
    ('JAZ', 'Jaz Drive'),
    ('SUPR', 'SuperDisk LS-120'),
    ('STOR', 'Storage'),
    ('TAPE', 'Tape'),
    ('ZIP', 'Zip Disk'),
    ('ADAP', 'Adapter Card'),
    ('CAPT', 'Capturecard'),
    ('FW', 'Firewire'),
    ('LAN', 'LAN Card'),
    ('MODM', 'Modem'),
    ('PRLL', 'Parallel'),
    ('RAID', 'RAID Card'),
    ('SCSI', 'SCSI'),
    ('SERL', 'Serial'),
    ('SNDC', 'Sound Card'),
    ('GPU', 'Video Card'),
    ('WIFI', 'WiFi Adapter'),
    ('KBD1', 'PS/2 Keyboard'),
    ('KBD2', 'AT Connector Keyboard'),
    ('KBD3', 'USB Keyboard'),
    ('MOS1', 'PS/2 Mouse'),
    ('MOS2', 'Serial Mouse'),
    ('MOS3', 'USB Mouse'),
    ('CRT', 'CRT Monitor'),
    ('FLTS', 'Flatscreen Monitor'),
    ('SPK', 'Speaker'),
    ('TV', 'TV'),
    ('PRPH', 'Peripheral'),
    ('BATT', 'Battery'),
    ('CORD', 'Cable/Cord/Connector'),
    ('LPTP', 'Laptop/Embedded'),
    ('OTHR', 'Other/Misc.'),
    ('UNKN', 'Unknown'),
]

class ComponentForm(FlaskForm):
    TYPE_GROUPS = [
        ('Core Hardware', [
            ('BIOS', 'BIOS Chip'),
            ('CASE', 'Case/Chassis'),
            ('FAN', 'Case Fan'),
            ('CPU', 'CPU'),
            ('CFAN', 'CPU Cooler'),
            ('MOBO', 'Motherboard'),
            ('PSU', 'Power Supply'),
        ]),
        ('Storage Devices', [
            ('CD', 'CD'),
            ('FLP5', '5.25" Floppy Disk'),
            ('FLP3', '3.5" Floppy Disk'),
            ('FDD5', '5.25" Floppy Drive'),
            ('FDD3', '3.5" Floppy Drive'),
            ('FLSH', 'Flash'),
            ('HDD', 'Hard Drive'),
            ('JAZ', 'Jaz Drive'),
            ('SUPR', 'SuperDisk LS-120'),
            ('STOR', 'Storage'),
            ('TAPE', 'Tape'),
            ('ZIP', 'Zip Disk'),
        ]),
        ('Expansion Cards', [
            ('ADAP', 'Adapter Card'),
            ('CAPT', 'Capturecard'),
            ('FW', 'Firewire'),
            ('LAN', 'LAN Card'),
            ('MODM', 'Modem'),
            ('PRLL', 'Parallel'),
            ('RAID', 'RAID Card'),
            ('SCSI', 'SCSI'),
            ('SERL', 'Serial'),
            ('SNDC', 'Sound Card'),
            ('GPU', 'Video Card'),
            ('WIFI', 'WiFi Adapter'),
        ]),
        ('Input Devices', [
            ('KBD1', 'PS/2 Keyboard'),
            ('KBD2', 'AT Connector Keyboard'),
            ('KBD3', 'USB Keyboard'),
            ('MOS1', 'PS/2 Mouse'),
            ('MOS2', 'Serial Mouse'),
            ('MOS3', 'USB Mouse'),
        ]),
        ('Output Devices', [
            ('CRT', 'CRT Monitor'),
            ('FLTS', 'Flatscreen Monitor'),
            ('SPK', 'Speaker'),
            ('TV', 'TV'),
        ]),
        ('Peripherals', [
            ('PRPH', 'Peripheral'),
        ]),
        ('Miscellaneous', [
            ('BATT', 'Battery'),
            ('CORD', 'Cable/Cord/Connector'),
            ('LPTP', 'Laptop/Embedded'),
            ('OTHR', 'Other/Misc.'),
            ('UNKN', 'Unknown'),
        ]),
    ]

    flat_type_choices = [(val, label) for group, items in TYPE_GROUPS for val, label in items]
    part_id = StringField('Part ID', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])

    type = SelectField(
        'Type',
        choices=flat_type_choices,
        validators=[DataRequired()]
    )

    manufacturer = StringField('Manufacturer')
    year = StringField('Year/Date')
    interface = StringField('Interface (PCI/AGP/IDE/etc)')
    specs = TextAreaField('Specs')
    serial_number = StringField('Serial Number')
    location = StringField('Location')
    status = SelectField('Status', choices=[
        ('In Use', 'In Use'),
        ('In Storage', 'In Storage'),
        ('Spare', 'Spare'),
        ('Broken', 'Broken'),
        ('Unknown', 'Unknown')
    ])
    condition = SelectField('Condition', choices=[
        ('New', 'New'),
        ('Like New', 'Like New'),
        ('Used', 'Used'),
        ('Good', 'Good'),
        ('Poor', 'Poor'),
        ('For Parts', 'For Parts'),
    ])
    notes = TextAreaField('Notes')
    tags = StringField('Tags (CSV)')

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