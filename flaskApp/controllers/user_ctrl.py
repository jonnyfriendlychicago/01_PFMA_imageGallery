from flaskApp import app
from flask import Flask, render_template, redirect, session, request, flash

from flask_bcrypt import Bcrypt

from flaskApp.models.user_mod import User_cls

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'user_id' not in session: # this whole user_Id check needs to happen on every page that should be requiring a successful login
        return render_template('index.html')
    else:     
        # flash("You are already logged in.  You have been redirected to your home page.")
        return redirect('/userTypeRouting/') 

@app.route('/login/', methods = ['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    user = User_cls.get_userEmail(data) # checks if this email in the DB

    if not user: 
        flash("No account exists with that email address.")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Password incorrect.")
        return redirect('/')
    session['user_id'] = user.id
    # flash("Your are now logged in")
    return redirect('/userTypeRouting/')

@app.route('/register/', methods = ['POST'])
def register():
    isValid = User_cls.validate(request.form)
    if not isValid:
        return redirect('/') # don't worry about msgs, b/c that's already handled with the flash on that classMethod
    newUser = {
        'userName': request.form['userName'], 
        'email': request.form['email'], 
        'firstName': request.form['firstName'], 
        'lastName': request.form['lastName'], 
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    user_id = User_cls.saveUser(newUser)
    # print("variable 'user_id' in the /register/ route:")
    # print(user_id)
    if not user_id: 
        flash("Our apologies.  Our system seems to be experiencing technical issues.  Please call our office at 123.456.7890 for further assistance.")
        return redirect('/')
    session['user_id'] = user_id
    flash("New Account created.")
    return redirect('/userTypeRouting/')

@app.route('/userTypeRouting/')
def userTypeRouting():
    if 'user_id' not in session: # this whole user_Id check needs to happen on every page that should be requiring a successful login
        flash("Please login to access this site.")
        return redirect('/')
    data = {
        "user_id": session['user_id']
    }
    return redirect('/dashboard/')
    # creating code to maker certain users an employee upon reaching this page.
    # NEED MORE EXPLANATION ON BELOW PLEASE ::: simple: just to prove that the two diff emp levels actually works
    # theUser = User_cls.get_oneUser(data)  
    # loggedInUser = User_cls.get_oneUser(data)  
    
    # if loggedInUser.id ==1:
    #     # if loggedInUser.accessLevel == 9:
    #     if loggedInUser.accessLevel == None:
    #         User_cls.updateUserEmpType(data)
    #         flash("User access updated to Employee (Level 9)")
    #         return redirect ('/airlines/')
    #     else: 
    #         return redirect ('/airlines/')
    
    # else: 
    #     get_booking = User_cls.get_userBookingFlightAirline(data)
    #     print("************* all booking from controller: ", get_booking)
    #     return render_template(
    #         'dashboard.html'
    #         , display_get_oneUser = User_cls.get_oneUser(data)
    #         , display_get_booking = get_booking
    #     )

    # return render_template(
    #         'dashboard.html'
    #         , display_get_oneUser = User_cls.get_oneUser(data)
    #         # , display_get_booking = get_booking
    #     )

""" moved dashbord below to image_ctrl.py
@app.route('/dashboard/')
def dashboard(): 
    if 'user_id' not in session: # this whole user_Id check needs to happen on every page that should be requiring a successful login
        flash("Please login to access this site.")
        return redirect('/')
    data = {
        "user_id": session['user_id']
    }
    return render_template(
        'dashboard.html'
        , dsp_get_oneUser = User_cls.get_oneUser(data)
        # , display_get_booking = get_booking
        , dsp_get_allRecipe = recipe_mod.Recipe_cls.get_allRecipe()
    )
"""

@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/')

# @app.route('/users/')
# def users():
#     if 'user_id' not in session: # this whole user_Id check needs to happen on every page that should be requiring a successful login
#         flash("You must be logged in to view this page.")
#         return redirect('/')
#     data = {
#         "id": session['user_id']
#     }
#     get_oneUser = User_cls.get_oneUser(data)  
#     if get_oneUser.access == 9:
#         return render_template(
#             'users.html'
#             , display_get_oneUser = get_oneUser
#             , display_allUsers = User_cls.get_allUser()
#         )
#     else: 
#         flash("You are not authorized to view the Users Management page.")
#         return redirect('/dashboard/')

# @app.route('/users/<int:user_id>/createEmployee/')
# def createEmployee(user_id):
#     data = {
#         'id': user_id
#     }
#     User_cls.updateUserEmpType(data)
#     flash("User updated to employee level")
#     return redirect('/users/')