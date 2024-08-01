# set up the Blueprint: let the code that there a punch of  routes associated 
from flask import Blueprint, render_template, request, flash, redirect, url_for
from  flask_login import login_required, current_user 
from . import db
from .models import Note, B2


view = Blueprint('view', __name__)


@view.route("/", methods=['GET','POST'])
@login_required # login required to access the home page
def home():
    def save_commit(): # Function to save changes
        db.session.add(new_note)
        db.session.commit()
        flash('Note added', category='success')
        return redirect(url_for('auth.receipt'))

    
    if request.method == 'POST': 
        building = request.form.get('building')
        unites = request.form.get('unites')
        service_type = request.form.get('service')
        price = request.form.get('price')
        note = request.form.get('note')

        if len(note) <= 1:
            flash('Note is too short!', category='error')
        else:
            if building == '1':
                new_note = Note(data=note, unites=unites, service_type=service_type, price=price, user_id=current_user.id) 
                save_commit()
            elif building == '2':
                new_note =B2(data=note, unites=unites, service_type=service_type, price=price, user_id=current_user.id) 
                save_commit()
    else: 
        pass
    return render_template("home.html", user=current_user, css_files='footere')

