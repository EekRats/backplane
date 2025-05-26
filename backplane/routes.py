from flask import render_template, redirect, url_for, request
from . import db
from .models import Component
from .forms import ComponentForm
from flask import current_app as app

@app.route('/')
def index():
    components = Component.query.all()
    return render_template('index.html', components=components)

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
            notes=form.notes.data
        )
        db.session.add(new)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_component.html', form=form)

@app.route('/component/<int:component_id>')
def view_component(component_id):
    component = Component.query.get_or_404(component_id)
    return render_template('view_component.html', component=component)