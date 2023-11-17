from flask import render_template, redirect, url_for, flash, Blueprint

from . import feedback_br
from .form import FeedbackForm
from .model import db, Feedback
from app.views import base


@feedback_br.route("/feedback", methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    feedbacks = db.session.query(Feedback).all()
    if form.validate_on_submit():
        username = form.username.data
        feedback_msg = form.feedback.data
        if username and feedback_msg:
            db.session.add(Feedback(username=username, feedback=feedback_msg))
            db.session.commit()
            flash("Feedback is added!", category="success")
        else:
            flash("Feedback isn't added!", category="danger")
        return redirect(url_for("feedback_br.feedback"))
    return render_template('feedback.html', feedbacks=feedbacks, form=form, base=base)

