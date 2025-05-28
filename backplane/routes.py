from flask import render_template, redirect, url_for, request
from . import db
from .models import Component, System, Tag
from .forms import ComponentForm, SystemForm
from flask import current_app as app
import os, math

# this and DummyForm needed due to CSRF token issue.
# need to render {{ form.hiddentag() }} every time that
# we use a <form method="POST">.
# This is due to Flask-WTF write-protecting to block CSRF attacks, using a hidden token
from flask_wtf import FlaskForm

class DummyForm(FlaskForm):
    pass

# for handling commas-eperated tags for items
def process_tags(tag_string):
    tag_names = [t.strip().lower() for t in tag_string.split(',') if t.strip()]
    tags = []
    for name in tag_names:
        tag = Tag.query.filter_by(name=name).first()
        if not tag:
            tag = Tag(name=name)
            db.session.add(tag)
        tags.append(tag)
    return tags

@app.route('/')
def index():
    query = request.args.get('q', '')
    if query:
        from sqlalchemy import func
        like = f"%{query.lower()}%"
        components = Component.query.filter(
            db.or_(
                func.lower(Component.part_id).like(like),
                func.lower(Component.name).like(like),
                func.lower(Component.type).like(like),
                func.lower(Component.manufacturer).like(like),
                func.lower(Component.specs).like(like),
                func.lower(Component.status).like(like),
                func.lower(Component.location).like(like),
                Component.tags.any(func.lower(Tag.name).like(like))
            )
        ).all()
    else:
        components = Component.query.all()
    return render_template('index.html', components=components, query=query)
    #components = Component.query.all()
    #return render_template('index.html', components=components)

@app.route('/add', methods=['GET', 'POST'])
def add_component():
    form = ComponentForm()
    
    # only autofilling the component ID on the the initilal GET
    if request.method == 'GET':
        default_type = form.type.data or 'CPU'
        prefix = default_type.upper()
        used = Component.query.with_entities(Component.part_id).filter(
            Component.part_id.like(f"{prefix}-%")
        ).all()
        used_numbers = set()
        for (part_id,) in used:
            try:
                num = int(part_id.split("-")[1])
                used_numbers.add(num)
            except (IndexError, ValueError):
                continue
        i = 1
        while i in used_numbers:
            i += 1
        form.part_id.data = f"{prefix}-{i:04}"
    from flask import flash
    if form.validate_on_submit():
        existing = Component.query.filter_by(part_id=form.part_id.data).first()
        if existing:
            flash(f"A component with Part ID '{form.part_id.data}' already exists. Choose a different ID.", "error")
            return render_template('add_component.html', form=form)
        new = Component(
            part_id=form.part_id.data,
            name=form.name.data,
            type=form.type.data,
            manufacturer=form.manufacturer.data,
            year=form.year.data,
            specs=form.specs.data,
            location=form.location.data,
            status=form.status.data,
            notes=form.notes.data,
            system=form.system_id.data
        )
        new.tags = process_tags(form.tags.data)
        db.session.add(new)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_component.html', form=form)

@app.route('/component/<int:component_id>')
def view_component(component_id):
    component = Component.query.get_or_404(component_id)
    folder = os.path.join(app.config['UPLOAD_FOLDER'], f'components/{component.id}')
    files = os.listdir(folder) if os.path.exists(folder) else []
    return render_template('view_component.html', component=component, files=files, form=DummyForm())

@app.route('/edit/<int:component_id>', methods=['GET', 'POST'])
def edit_component(component_id):
    component = Component.query.get_or_404(component_id)
    form = ComponentForm(obj=component)
    if request.method == 'GET':
        form.tags.data = ', '.join(tag.name for tag in component.tags)
    if form.validate_on_submit():
        component.part_id = form.part_id.data
        component.name = form.name.data
        component.type = form.type.data
        component.manufacturer = form.manufacturer.data
        component.year = form.year.data
        component.specs = form.specs.data
        component.location = form.location.data
        component.status = form.status.data
        component.notes = form.notes.data
        component.system = form.system_id.data
        component.tags = process_tags(form.tags.data)

        db.session.commit()
        return redirect(url_for('view_component', component_id=component.id))

    return render_template('edit_component.html', form=form, component=component)

@app.route('/delete/<int:component_id>', methods=['GET'])
def delete_component(component_id):
    component = Component.query.get_or_404(component_id)
    db.session.delete(component)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_system', methods=['GET', 'POST'])
def add_system():
    form = SystemForm()
    if form.validate_on_submit():
        new = System(
            name=form.name.data,
            description=form.description.data,
            location=form.location.data,
            notes=form.notes.data
        )
        db.session.add(new)
        db.session.commit()
        return redirect(url_for('list_systems'))
    return render_template('add_system.html', form=form)

@app.route('/systems')
def list_systems():
    systems = System.query.all()
    return render_template('list_systems.html', systems=systems)

@app.route('/system/<int:system_id>')
def view_system(system_id):
    system = System.query.get_or_404(system_id)
    folder = os.path.join(app.config['UPLOAD_FOLDER'], f'systems/{system.id}')
    files = os.listdir(folder) if os.path.exists(folder) else []
    return render_template('view_system.html', system=system, files=files, form=DummyForm())

@app.route('/edit_system/<int:system_id>', methods=['GET', 'POST'])
def edit_system(system_id):
    system = System.query.get_or_404(system_id)
    form = SystemForm(obj=system)
    if form.validate_on_submit():
        form.populate_obj(system)
        db.session.commit()
        return redirect(url_for('list_systems'))
    return render_template('edit_system.html', form=form, system=system)

@app.route('/delete_system/<int:system_id>', methods=['GET'])
def delete_system(system_id):
    system = System.query.get_or_404(system_id)
    # turns out we actually need to *unassign* the components before deleting...
    # otherwise the DB breaks and everything freaks out (kinda)
    for c in system.components:
        c.system = None
    db.session.delete(system)
    db.session.commit()
    return redirect(url_for('list_systems'))

@app.route('/next_part_id/<string:component_type>')
def next_part_id(component_type):
    prefix = component_type.upper()
    existing_ids = Component.query.with_entities(Component.part_id).filter(
        Component.part_id.like(f'{prefix}-%')
    ).all()

    used_numbers = set()
    for (part_id,) in existing_ids:
        try:
            number = int(part_id.split('-')[1])
            used_numbers.add(number)
        except (IndexError, ValueError):
            continue
    i = 1
    while i in used_numbers:
        i += 1
    next_id = f"{prefix}-{i:04}"
    return {'next_id': next_id}

@app.route('/upload_component_file/<int:component_id>', methods=['POST'])
def upload_component_file(component_id):
    from werkzeug.utils import secure_filename
    from flask import flash
    component = Component.query.get_or_404(component_id)

    files = request.files.getlist('file')
    saved = []
    for file in files:
        #if file and allowed_file(file.filename):
        if file:
            filename = secure_filename(file.filename)
            folder = os.path.join(app.config['UPLOAD_FOLDER'], f'components/{component.id}')
            os.makedirs(folder, exist_ok=True)
            filepath = os.path.join(folder, filename)
            file.save(filepath)
            saved.append(filename)

    flash(f"Uploaded {len(saved)} files.")
    return redirect(url_for('view_component', component_id=component.id))

@app.route('/download_component_file/<int:component_id>/<filename>')
def download_component_file(component_id, filename):
    from flask import send_from_directory
    folder = os.path.join(app.config['UPLOAD_FOLDER'], f'components/{component_id}')
    return send_from_directory(folder, filename, as_attachment=True)

@app.route('/upload_system_file/<int:system_id>', methods=['POST'])
def upload_system_file(system_id):
    from werkzeug.utils import secure_filename
    from flask import flash
    system = System.query.get_or_404(system_id)

    files = request.files.getlist('file')
    saved = []
    for file in files:
        #if file and allowed_file(file.filename):
        if file:
            filename = secure_filename(file.filename)
            folder = os.path.join(app.config['UPLOAD_FOLDER'], f'systems/{system.id}')
            os.makedirs(folder, exist_ok=True)
            filepath = os.path.join(folder, filename)
            file.save(filepath)
            saved.append(filename)

    flash(f"Uploaded {len(saved)} files.")
    return redirect(url_for('view_system', system_id=system.id))
    
@app.route('/download_system_file/<int:system_id>/<filename>')
def download_system_file(system_id, filename):
    from flask import send_from_directory
    folder = os.path.join(app.config['UPLOAD_FOLDER'], f'systems/{system_id}')
    return send_from_directory(folder, filename, as_attachment=True)

@app.route('/tags/<string:tag_name>')
def components_by_tag(tag_name):
    tag = Tag.query.filter_by(name=tag_name.lower()).first_or_404()
    components = tag.components
    return render_template('components_by_tag.html', tag=tag, components=components)

@app.route('/tags')
def tag_cloud():
    from sqlalchemy import func
    tag_counts = db.session.query(
        Tag.name, func.count(Component.id)
    ).join(Component.tags).group_by(Tag.name).all()

    tags = [{'name': name, 'count': count} for name, count in tag_counts]
    return render_template('tag_cloud.html', tags=tags, math=math)