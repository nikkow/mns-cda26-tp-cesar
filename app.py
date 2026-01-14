from flask import Flask, render_template, request, flash
from utils.cesar import cesar, decesar

app = Flask(__name__)
app.secret_key = "super-mns-riz-crousty"

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

    default_values = {
      "action": action, 
      "key": str(key),
      "message": result[1] if result[1] else "",
    }

  return render_template("index.html", result=result, default_values=default_values)

if __name__ == "__main__":
  app.run(debug=True)