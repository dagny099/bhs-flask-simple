from app import app
from flask import render_template, request, redirect

@app.route('/')
def index():
  return render_template('public/index.html')

@app.route('/about')
def about():
  return """<h1 style='color: red;'>I'm a red H1 heading!</h1>
  <p>This is some text in a paragraph tag</p>
  <code>Flask is <em>awesome</em></code>
  """
#  return render_template('public/about.html')

@app.route('/around', methods=["GET", "POST"])
def around():
    if request.method=="POST":
        req = request.form
        missing = list()
        for k, v in req.items():
            if v =="":
                missing.append(k)
        if missing:
            feedback = f"Missing fields for {', '.join(missing)}"
            return render_template('public/around.html', feedback=feedback)

        username = req["username"]
        email = req["email"]
        password = req["password"]
        print(f"username is: {username}, email is: {email}, and password is: {password}")
        return redirect(request.url)
    return render_template('public/around.html')

@app.route('/hello/<name>')
def hello_name(name):
  return 'Hello %s!!' % name

