from flask import render_template, redirect, url_for
from .form import ItemForm
from .model import Todo, db
from . import todo_br


@todo_br.route('/todo', methods=['GET', 'POST'])
def todo():
    form = ItemForm()
    todo_list = db.session.query(Todo).all()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        new_todo = Todo(title=title, description=description, complete=False)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for("todo_br.todo"))
    return render_template('todo.html', todo_list=todo_list, form=form)


@todo_br.route("/update/<int:todo_id>")
def update(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("todo_br.todo"))


@todo_br.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("todo_br.todo"))
