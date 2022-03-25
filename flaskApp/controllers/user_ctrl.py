from flaskApp import app
from flask import Flask, render_template, redirect, session, request, flash

from flask_bcrypt import Bcrypt

# from flaskApp.models.user_mod import User_cls
from flaskApp.models import user_mod
from flaskApp.models import image_mod
from flaskApp.models import interaction_mod

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'session_user_id' not in session: # this whole user_Id check needs to happen on every page that should be requiring a successful login
        return render_template('index.html')
    else:     
        return redirect('/userTypeRouting/') 

@app.route('/register/', methods = ['POST'])
def register():
    isValid = user_mod.User_cls.validateRegistration(request.form)
    if not isValid:
        return redirect('/') # don't worry about msgs, b/c that's already handled with the flash on that classMethod
    data = {
        'userName': request.form['userName'], 
        'email': request.form['email'], 
        'firstName': request.form['firstName'], 
        'lastName': request.form['lastName'], 
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    newUserId = user_mod.User_cls.saveUser(data)
    if not newUserId: # this if basically means: somehow, that save just didn't work, so we are dropping the save/create process and returning you to login. 
        flash("Our apologies.  Our system seems to be experiencing technical issues.  Please call our office at 123.456.7890 for further assistance.")
        return redirect('/')
    session['session_user_id'] = newUserId # saveUser classmethod returns the id of the newly created user. set that as the session_user_id immediamente
    flash("New Account created.")
    return redirect('/userTypeRouting/')

@app.route('/login/', methods = ['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    user = user_mod.User_cls.get_userEmail(data) # checks if this email in the DB; get_userEmail class method returns the entire class; that's why the ".id" a few lines down is required.
    if not user: 
        flash("No account exists with that email address.")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Password incorrect.")
        return redirect('/')
    session['session_user_id'] = user.id # this needs to exist as such because what's being retuned by get_userEmail is a class, not a single id value
    # session['session_user_id'] = user
    return redirect('/userTypeRouting/')

@app.route('/userTypeRouting/')
def userTypeRouting():
    if 'session_user_id' not in session: # this whole user_Id check needs to happen on every page that should be requiring a successful login
        flash("Please login to access this site.")
        return redirect('/')
    data = {
        "session_user_id": session['session_user_id']
    }
    return redirect('/dashboard/')

    """ all of below exists to either auto upgrade certain user accounts OR route users of certain types to pages other than dashboard.  Implement as needed."""
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

@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/')

""" all of below is set up to manage users.  activate this functionality as needed."""
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

@app.route('/dashboard/')
def dashboard(): 
    if 'session_user_id' not in session: 
        flash("Please login to access this site.")
        return redirect('/')
    data = {
        "session_user_id": session['session_user_id']
    }
    return render_template(
        'dashboard.html'
        , getSessionUser = user_mod.User_cls.getSessionUser(data) 
        # below line is my big get-all, for repurposing as needed. 
        , getAllImageAllUser = image_mod.Image_cls.getAllImageAllUser()
    )

@app.route('/dashboardClassic/')
def dashboardClassic(): 
    if 'session_user_id' not in session: 
        flash("Please login to access this site.")
        return redirect('/')
    data = {
        "session_user_id": session['session_user_id']
    }
    return render_template(
        'dashboardClassic.html'
        , getSessionUser = user_mod.User_cls.getSessionUser(data) 
        , getAllImageAllUser = image_mod.Image_cls.getAllImageAllUser()
    )

@app.route('/profile/<int:user_id>/')
def profile(user_id): 
    if 'session_user_id' not in session: 
        flash("Please login to access this site.")
        return redirect('/')
    data = {
        "session_user_id": session['session_user_id']
        , "user_id": user_id
    }
    return render_template(
        'profile.html'
        , getSessionUser = user_mod.User_cls.getSessionUser(data) # just built 7:19pm tues
        , getOneUser = user_mod.User_cls.getOneUser(data)
        # , dsp_getUserImage = user_mod.User_cls.getUserImage(data)
        , getAllImageOneUser = image_mod.Image_cls.getAllImageOneUser(data)
    )

@app.route('/profile/<int:user_id>/edit/')
def profileEdit(user_id): 
    if 'session_user_id' not in session: 
        flash("You must be logged in to access this site.")
        return redirect('/')
    data = {
        # "user_id": session['user_id']
        'session_user_id': session['session_user_id']
        , 'user_id': user_id
        # , 'userName': request.form['userName']
        # , 'email': request.form['email']
        # , 'firstName': request.form['firstName']
        # , 'lastName': request.form['lastName']
    }
    getOneUser = user_mod.User_cls.getOneUser(data)
    if session['session_user_id'] != getOneUser.id:
        flash("You can only edit your own profile.")
        return redirect(f'/profile/{user_id}/')
    return render_template(
        'profileEdit.html'
        # , dsp_get_oneUser = user_mod.User_cls.get_oneUser(data)
        , getSessionUser = user_mod.User_cls.getSessionUser(data) # just built 7:19pm tues
        , getOneUser = getOneUser
        # , dsp_getUserImage = user_mod.User_cls.getUserImage(data)
    )

@app.route('/profile/<int:user_id>/update/', methods =['POST'])
def profileUpdate(user_id):
    data = {
        'user_id': user_id
        , 'userName': request.form['userName']
        , 'email': request.form['email']
        , 'firstName': request.form['firstName']
        , 'lastName': request.form['lastName'] 
    }
    updateProfile = user_mod.User_cls.updateUser(data)
    return redirect(f'/profile/{user_id}/')