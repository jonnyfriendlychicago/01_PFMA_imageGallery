# from email.mime import image
from flaskApp import app
from flask import Flask, render_template, redirect, session, request, flash
from flaskApp.models import user_mod 
from flaskApp.models import image_mod
from flaskApp.models import interaction_mod




@app.route('/interaction/create/<int:image_id>/', methods = ['POST'])
def createInteraction(image_id): 
    if 'session_user_id' not in session: 
        flash("You must be logged in to access this site.")
        return redirect('/')
    data = {
        'session_user_id': session['session_user_id']
        , 'image_id' : image_id
        , 'comment': request.form['comment']
    }
    interaction_mod.Interaction_cls.saveInteraction(data)
    return redirect(f'/image/{image_id}/')




"""


@app.route('/image/add/')
def addImage():
    if 'session_user_id' not in session: 
        flash("You must be logged in to access this site.")
        return redirect('/')
    data = {
        'session_user_id': session['session_user_id']
        # , 'user_id': user_id
    }
    return render_template(
        'imageAdd.html' 
        , dsp_getSessionUser = user_mod.User_cls.getSessionUser(data) # this is what always *minimally* populates the header section  correctly
        # , dsp_get_oneUser = user_mod.User_cls.get_oneUser(data) 
    )

@app.route('/image/create/<int:returnToUserId>/', methods = ['POST'])
def createImage(returnToUserId):
    data = {
        'user_id': session['session_user_id']
        , 'imageTitle': request.form['imageTitle']
        , 'imageInfo': request.form['imageInfo']        
        , 'filePath': request.form['filePath']
        # , 'returnToUserId' : returnToUserId
    }
    image_mod.Image_cls.save(data)
    return redirect(f'/profile/{returnToUserId}/')


@app.route('/image/<int:image_id>/')
def viewImage(image_id): 
    if 'session_user_id' not in session: # this whole user_Id check needs to happen on every page that should be requiring a successful login
        flash("You must be logged in to access this site.")
        return redirect('/')
    data = {
        "session_user_id": session['session_user_id']
        , 'image_id': image_id
    }
    return render_template(
        'imageView.html'
        , dsp_getSessionUser = user_mod.User_cls.getSessionUser(data) 
        , getOneImageOneUser = image_mod.Image_cls.getOneImageOneUser(data)
        # , dsp_get_oneUser = user_mod.User_cls.get_oneUser(data) 
        # , getOneImage = image_mod.Image_cls.getOneImage(data)   
    )


@app.route('/recipe/<int:image_id>/edit/')
def editImage(image_id): 
    if 'user_id' not in session: 
        flash("You must be logged in to access this site.")
        return redirect('/')
    data = {
        'user_id': session['user_id']
        , 'image_id': image_id
        , 'imageTitle': request.form['imageTitle']
        , 'imageInfo': request.form['imageInfo']
        
    }
    get_oneImage = image_mod.Image_cls.getOne(data)
    if session['user_id'] != get_oneImage.user_id:
        flash("You must be the creator of an image to edit the image.")
        return redirect('/')
    else: 
        return render_template(
        'imageEdit.html' 
        , dsp_get_oneUser = user_mod.User_cls.get_oneUser(data)
        , dsp_get_oneImage = get_oneImage
    )

@app.route('/recipe/<int:image_id>/update/', methods=['POST'])
def updateImage(image_id): 
    data = {
        'user_id': session['user_id']
        , 'image_id': image_id
        , 'filePath': request.form['filePath']
    }
    updateImage = image_mod.Image_cls.update(data)
    return redirect(f'/image/{image_id}/')

@app.route('/recipe/<int:image_id>/delete/')
def deleteImage(image_id): 
    if 'user_id' not in session: 
        flash("You must be logged in to access this site.")
        return redirect('/')
    data = {
        'user_id': session['user_id']
        , 'image_id': image_id
    }
    get_oneImage = image_mod.Image_cls.get_one(data)
    if session['user_id'] != get_oneImage.user_id:
        flash("You must be the creator of an image to delete it.")
        return redirect('/dashboard/')
    else: 
        image_mod.Image_cls.delete(data)
        flash("Recipe deleted.  POOF!  GONE!")
        return redirect ('/dashboard/')

"""