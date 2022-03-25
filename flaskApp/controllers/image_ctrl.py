from email.mime import image
from flaskApp import app
from flask import Flask, render_template, redirect, session, request, flash
from flaskApp.models import user_mod 
from flaskApp.models import image_mod
from flaskApp.models import interaction_mod

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
        , getSessionUser = user_mod.User_cls.getSessionUser(data) # this is what always *minimally* populates the header section  correctly
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
        , getSessionUser = user_mod.User_cls.getSessionUser(data) 
        , getOneImageOneUser = image_mod.Image_cls.getOneImageOneUser(data)
        # , dsp_get_oneUser = user_mod.User_cls.get_oneUser(data) 
        , getOneImage = image_mod.Image_cls.getOneImage(data)   
        , getOneImageAllInterAllUser = image_mod.Image_cls.getOneImageAllInterAllUser(data)
    )


@app.route('/image/<int:image_id>/edit/')
def editImage(image_id): 
    if 'session_user_id' not in session: 
        flash("You must be logged in to access this site.")
        return redirect('/')
    data = {
        'session_user_id': session['session_user_id']
        , 'image_id': image_id
    }
    getOneImage = image_mod.Image_cls.getOneImage(data)
    if session['session_user_id'] != getOneImage.user_id:
        flash("You must be the creator of an image to edit the image.")
        return redirect(f'/image/{image_id}/')
    else: 
        return render_template(
        'imageEdit.html' 
        , getOneUser = user_mod.User_cls.getOneUser(data)
        , getOneImage = getOneImage
    )

@app.route('/image/<int:image_id>/update/', methods=['POST'])
def updateImage(image_id): 
    data = {
        'session_user_id': session['session_user_id']
        , 'image_id': image_id
        , 'filePath': request.form['filePath']
        , 'imageTitle': request.form['imageTitle']
        , 'imageInfo': request.form['imageInfo'] 
    }
    updateImage = image_mod.Image_cls.update(data)
    return redirect(f'/image/{image_id}/')

@app.route('/image/<int:image_id>/delete/')
def deleteImage(image_id): 
    if 'session_user_id' not in session: 
        flash("You must be logged in to access this site.")
        return redirect('/')
    data = {
        'session_user_id': session['session_user_id']
        , 'image_id': image_id
    }
    imageRecord = image_mod.Image_cls.getOneImage(data)
    if session['session_user_id'] != imageRecord.user_id:
        flash("You must be the creator of an image to delete it.")
        return redirect('/image/<int:image_id>//')
    else: 
        image_mod.Image_cls.deleteImage(data)
        flash("Image deleted.  POOF!  GONE!  And all comments/interactions got whacked, too.")
        return redirect ('/dashboard/')

