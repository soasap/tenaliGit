#######   IMPORTS START HERE    #########
from flask import Flask, render_template, request, session
from flask import flash
from sqlalchemy import false, text, true
import templates.test_db.db_model.db_core_for_all
import re
#from templates.test_db.db_model.db_core_for_all import *
from datetime import datetime, timedelta
import templates.test_db.db_model.db_core_for_all as db_core_for_all

#######   INIT start HERE    #########

app = Flask(__name__)

app.secret_key = 'poola'
app.permanent_session_lifetime = timedelta(minutes=5)

#######   Page COde  start HERE    #########

# ---------   Login  Module ------------


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():

  if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
    email = request.form['email']
    password = request.form['password']
    vaid_flag = False  # data validation flag

    #print(".0 email : ", email, " password : ", password, " Session VAriable",
    #session["poola"])
    # Validate email and pw
    if len(email.strip()) == 0:
      print("0.01 The email is empty.")
      flash("Please Enter email address.")
      return render_template('/test_db/doc/db_test_login.html')
    else:
      print("0.02 The email is NOT empty.")
      vaid_flag = True

    if len(password.strip()) == 0:
      print("0.03 The password  is empty.")
      flash("Please Enter pasword.")
      return render_template('/test_db/doc/db_test_login.html')
    else:
      print("0.04 The password is NOT empty.")
      vaid_flag = True

    print("0.03 Valid flag True .")
    a = "select * from user where email ='"
    b = "' AND password = '"
    c = "'"
    s = a + email + b + password + c

    print("  1:  s : ", s)
    conn = db_core_for_all.getDBConnection()
    myDbQuery = conn.execute(text(s))
    myrow = myDbQuery.fetchone()
    print(" 2:   myrow", myrow)

    if myrow:
      print("Step   3: ")
      session['loggedin'] = True
      session['id'] = myrow.id
      session['name'] = myrow.name
      session['email'] = myrow.email
      return render_template('/test_db/doc/frag/db_test_index.html')
    else:
      flash("Invalid email or password.. please check and reenter")
  else:
    print("Step   4: ")
    #flash("Please enter correct email / password ")
    print("Step   4.1: message = ")
  return render_template('/test_db/doc/db_test_login.html')


# ---------   Logout  Module ------------
@app.route('/logout')
def logout():
  session.pop('loggedin', None)
  session.pop('id', None)
  session.pop('email', None)
  session.pop('name', None)
  #return redirect(url_for('login'))
  flash("logged out succesfully ....")
  return render_template('/test_db/doc/frag/db_test_logout.html')


@app.route('/enroll')
def enroll():
  return render_template('/test_db/doc/frag/db_test_reg.html')

  # ---------   REGISTER  Module ------------


@app.route('/register', methods=['GET', 'POST'])
def register():
  # Output message if something goes wrong...

  # Check if "username", "password" and "email" POST requests exist (user submitted form)
  if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
    print("  .oo1:  s : ")
    email = request.form['email']
    password = request.form['password']
    name = request.form['name']
    valid_flag = False  # data validation flag

    # Validate name email and pw
    if len(name.strip()) == 0:
      print("1.01 The name is empty.")
      flash("Please Enter Name ")
      return render_template('/test_db/doc/frag/db_test_reg.html')
    else:
      print("1.02 The email is NOT empty.")
      vaid_flag = True

    if len(email.strip()) == 0:
      print("1.01 The email is empty.")
      flash("Please Enter email address.")
      return render_template('/test_db/doc/frag/db_test_reg.html')
    else:
      print("1.02 The email is NOT empty.")
      vaid_flag = True

    if len(password.strip()) == 0:
      print("1.03 The password  is empty.")
      flash("Please Enter pasword.")
      return render_template('/test_db/doc/frag/db_test_reg.html')
    else:
      print("1.04 The password is NOT empty.")
      vaid_flag = True

      print("  password : ", password, "name : ", name, "email : ", email,
            "  Form NAme :", name)
      a = "select * from user where email ='"
      c = "'"
      s = a + email + c

      print("  11:  s : ", s)
      conn = db_core_for_all.getDBConnection()
      myDbQuery = conn.execute(text(s))
      myrow = myDbQuery.fetchone()

    if myrow:

      flash("Account already exists.. please login ")
      return render_template('/test_db/doc/db_test_login.html')
    elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
      print("Step   5: ")
      flash("Invalid email address ")
      return render_template('/doc/login_frag/db_test_reg.html')
    elif not name or not password or not email:
      print("Step   6: ")
      flash("Please fill out the form ")
      return render_template('/test_db/doc/frag/db_test_reg.html')
    else:
      print("Step   7: ")

      m = "insert into user (name, password, email) values ('"
      n = "'"
      l = "','"
      p = "')"
      k = m + name + l + password + l + email + p
      print("Query to insert : ", k)

      conn = db_core_for_all.getDBConnection()
      myDbQuery = conn.execute(text(k))
      conn.commit

      session['loggedin'] = True

      # Set login data to session
      session['name'] = name
      session['email'] = email

      flash(
          "You have successfully registered .. please login with your email and password "
      )
      return render_template('/test_db/doc/frag/db_test_index.html')

  elif request.method == 'POST':
    # Form is empty... (no POST data)
    flash("Please fill out the form")
  # Show registration form with message (if any)
  return render_template('/test_db/doc/frag/db_test_index.html')


#######   IP COde  start HERE    #########

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=False)
