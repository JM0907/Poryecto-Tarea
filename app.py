from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tareas.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False, default='incomplete')  

with app.app_context():
    db.create_all()

def search_tarea(tarea):
    tarea_existente = Tarea.query.filter_by(name=tarea).first()
    if tarea_existente:
        return render_template('tareas.html', tarea=tarea_existente)
    else:
        nueva_tarea = Tarea(name=tarea)  
        db.session.add(nueva_tarea)
        db.session.commit()
        return render_template('tareas.html', tarea=nueva_tarea)

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        tarea = request.form.get('tarea')
        estado = request.form.get('estado')
        if tarea:
            return search_tarea(tarea)
        elif estado == 'complete':
            tarea_name = request.form.get('tarea')
            tarea = Tarea.query.filter_by(name=tarea_name).first()
            tarea.state = 'complete'
            db.session.commit()
            return jsonify({'status': 'success'})
    return render_template('tareas.html', tarea=None)

@app.route("/insert_tarea/<tarea_name>")
def insert_tarea(tarea_name):
    tarea_existente = Tarea.query.filter_by(name=tarea_name).first()
    if tarea_existente:
        return 'La tarea ya existe en la base de datos'
    else:
        nueva_tarea = Tarea(name=tarea_name)
        db.session.add(nueva_tarea)
        db.session.commit()
        return f'Tarea "{tarea_name}" agregada a la base de datos'

if __name__ == "__main__":
    app.run(debug=True)
