import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'your-key-here'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'backplane.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    MAX_CONTENT_LENGTH = 1024 * 1024 * 1024 # 1GB. Probably don't need a limit, but idk, the docs showed how to do a limit.
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'txt', 'sh', 'exe', 'iso', 'img', 'ima', 'bin'}
    TYPE_LABELS = {
        'BIOS': 'BIOS Chip',
        'CASE': 'Case/Chassis',
        'FAN': 'Case Fan',
        'CPU': 'CPU',
        'CFAN': 'CPU Cooler',
        'MOBO': 'Motherboard',
        'PSU': 'Power Supply',
        'CD': 'CD',
        'FLP5': '5.25\" Floppy Disk',
        'FLP3': '3.5\" Floppy Disk',
        'FDD5': '5.25\" Floppy Drive',
        'FDD3': '3.5\" Floppy Drive',
        'FLSH': 'Flash',
        'HDD': 'Hard Drive',
        'JAZ': 'Jaz Drive',
        'SUPR': 'SuperDisk LS-120',
        'STOR': 'Storage',
        'TAPE': 'Tape',
        'ZIP': 'Zip Disk',
        'ADAP': 'Adapter Card',
        'CAPT': 'Capture Card',
        'FW': 'Firewire',
        'LAN': 'LAN Card',
        'MODM': 'Modem',
        'PRLL': 'Parallel',
        'RAID': 'RAID Card',
        'SCSI': 'SCSI',
        'SERL': 'Serial',
        'SNDC': 'Sound Card',
        'GPU': 'Video Card',
        'WIFI': 'WiFi Adapter',
        'KBD1': 'PS/2 Keyboard',
        'KBD2': 'AT Keyboard',
        'KBD3': 'USB Keyboard',
        'MOS1': 'PS/2 Mouse',
        'MOS2': 'Serial Mouse',
        'MOS3': 'USB Mouse',
        'CRT': 'CRT Monitor',
        'FLTS': 'Flatscreen Monitor',
        'SPK': 'Speaker',
        'TV': 'TV',
        'PRPH': 'Peripheral',
        'BATT': 'Battery',
        'CORD': 'Cable/Cord/Connector',
        'LPTP': 'Laptop/Embedded',
        'OTHR': 'Other/Misc.',
        'UNKN': 'Unknown',
    }