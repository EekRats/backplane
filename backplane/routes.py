from flask import render_template, redirect, url_for, request
from . import db
from .models import Component, System
from .forms import ComponentForm, SystemForm
from flask import current_app as app

@app.route('/')
def index():
    query = request.args.get('q', '')
    if query:
        components = Component.query.filter(
            db.or_(
                Component.part_id.ilike(f'%{query}%'),
                Component.name.ilike(f'%{query}%'),
                Component.type.ilike(f'%{query}%'),
                Component.manufacturer.ilike(f'%{query}%')
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
    if form.validate_on_submit():
        new = Component(
            part_id=form.part_id.data,
            name=form.name.data,
            type=form.type.data,
            manufacturer=form.manufacturer.data,
            specs=form.specs.data,
            location=form.location.data,
            status=form.status.data,
            notes=form.notes.data,
            system=form.system_id.data
        )
        db.session.add(new)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_component.html', form=form)

@app.route('/component/<int:component_id>')
def view_component(component_id):
    component = Component.query.get_or_404(component_id)
    return render_template('view_component.html', component=component)

@app.route('/edit/<int:component_id>', methods=['GET', 'POST'])
def edit_component(component_id):
    component = Component.query.get_or_404(component_id)
    form = ComponentForm(obj=component)
    if form.validate_on_submit():
        form.populate_obj(component)
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