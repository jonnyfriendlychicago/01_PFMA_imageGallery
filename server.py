from flaskApp import app

from flaskApp.controllers import image_ctrl, user_ctrl, interaction_ctrl

if __name__ == "__main__": 
    app.run(debug = True)