from flask import Flask, render_template, request, flash, redirect, url_for
from utils.cesar import cesar, decesar
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "super-mns-riz-crousty"
# Configuration de SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://cesar:avecesar@localhost/cesar'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://:inmemory:'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de SQLAlchemy (ORM)
db = SQLAlchemy(app)

# Définition du modèle 
class HistoryEntry(db.Model):
    __tablename__ = 'history'

    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(10), nullable=False)
    message = db.Column(db.Text, nullable=False)
    key = db.Column(db.Integer, nullable=False)
    result = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, action: str, message: str, key: int, result: str):
        self.action = action
        self.message = message
        self.key = key
        self.result = result

    def __repr__(self):
        return f"HistoryEntry('{self.action}', '{self.message}', '{self.key}', '{self.result}')"

# Création de la table dans SQLite
with app.app_context():
  db.create_all()

# Routes
@app.route("/", methods=["GET", "POST"])
def home():
  result = (None, None)
  default_values = {
    "action": "encode",
    "message": "",
    "key": "",
  }

  if request.method == "POST":
    has_error = False
    key = 0 # evite les érreurs de linter
  
    try:
      key = int(request.form.get("key", "1").strip())
    except: 
      has_error = True
      flash("La clé est invalide (entier attedu)", "error")
    
    message = request.form.get("message", "").strip()
    if not message: 
      has_error = True
      flash("Veuillez saisir un message à (dé)chiffrer", "error")
    
    action = request.form.get("action", "").strip()
    if action not in ["encode", "decode"]:
      has_error = True
      flash("L'action est invalide", "error")

    if not has_error:
      if action == "encode":
        result = (message, cesar(message, key))
      else: 
        result = (message, decesar(message, key))

      # Enregistrement dans la base de données
      entry = HistoryEntry(action=action, message=message, key=key, result=result[1])
      db.session.add(entry)
      db.session.commit()
      
    default_values = {
      "action": action, 
      "key": str(key),
      "message": result[1] if result[1] else "",
    }

  return render_template("index.html", result=result, default_values=default_values)

@app.route("/history")
def history():
  entries = HistoryEntry.query.all()
  return render_template("history.html", entries=entries)

@app.route("/delete-history/<int:entry_id>")
def delete_history(entry_id):
  entry = HistoryEntry.query.get(entry_id)
  if not entry:
    flash("Entrée d'historique non trouvée", "error")
    return redirect(url_for("history"))
  
  db.session.delete(entry)
  db.session.commit()
  
  flash("Entrée d'historique supprimée avec succès", "success")
  return redirect(url_for("history"))
  

if __name__ == "__main__":
  app.run(debug=True)
