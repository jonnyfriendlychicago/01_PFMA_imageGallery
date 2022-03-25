from flaskApp.config.mysqlconnection import connectToMySQL
from flask import flash
from flaskApp.models import image_mod

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z -]+$') #WORKS!
USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9]+$') #WORKS!

class User_cls: 
    db = 'imageGallery_sch'

    def __init__(self, data): 
        self.id = data['id']
        self.userName = data['userName']
        self.email = data['email']
        self.firstName = data['firstName']
        self.lastName = data['lastName']
        self.password = data['password']
        self.accessLevel = data['accessLevel']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']

        # self.userImagesList = []

    # below is a cheeky little function to save some typing.  Think about how functions like this can be exploited in other ways. 
    def fullName(self):
        return (f"{self.firstName} {self.lastName}")

    @staticmethod
    def validateRegistration(registrationForm):
        isValid = True

        q = 'select * from user where email = %(email)s;'
        result = connectToMySQL(User_cls.db).query_db(q, registrationForm)
        if len(result) >= 1: 
            isValid = False
            flash("Email already in use.")
        
        q = 'select * from user where userName = %(userName)s;'
        result_two = connectToMySQL(User_cls.db).query_db(q, registrationForm)
        if len(result_two) >= 1: 
            isValid = False
            flash("Username already in use.")

        if not EMAIL_REGEX.match(registrationForm['email']): 
            isValid = False
            flash("Invalid email address.")
        
        if not USERNAME_REGEX.match(registrationForm['userName']): 
            isValid = False
            flash("User name required.  Only letters and numbers allowed.")

        # the "len" check below on firstname and lastName is already handled by the NAME_REGEX check

        # if len(registrationForm['firstName']) < 1: # orig code says 2 char, but 1 seems better to me.  Malcolm X !
        #     isValid = False
        #     flash("First name required.")
        
        if not NAME_REGEX.match(registrationForm['firstName']): 
            isValid = False
            flash("First name required.  Only letters, spaces and hypen/dash/- allowed.")

        # if len(registrationForm['lastName']) < 1: # orig code says 2 char, but 1 seems better to me.  Malcolm X !
        #     isValid = False
        #     flash("Last name required.")
        
        if not NAME_REGEX.match(registrationForm['lastName']): 
            isValid = False
            flash("Last name required.  Only letters, spaces and hypen/dash/- allowed.")

        if len(registrationForm['password']) < 1: # pop this up for EXAM!!!!!
            isValid = False
            flash("Password required.  Must be at least 8 characters.")
        
        if registrationForm['password'] != registrationForm['confirm']:
            isValid = False
            flash("Password entries must match.")
        return  isValid

    @staticmethod
    def validateProfileEdit(profileEditForm):
        isValid = True
        # not gonna allow edits to email or username right now, b/c validation there will be more complex:
        # assume user doens't want to change email addy, just "resubmit" the existing email addy.
        # well, there will be one and only one record in the db with that email addy already: this very user!
        # which means, the validation on email will always fail.
        # in order to make this work, need the validation to check: is there any OTHER user with this email addy already? 

        if not NAME_REGEX.match(profileEditForm['firstName']): 
            isValid = False
            flash("First name required.  Only letters, spaces and hypen/dash/- allowed.")

        # if len(registrationForm['lastName']) < 1: # orig code says 2 char, but 1 seems better to me.  Malcolm X !
        #     isValid = False
        #     flash("Last name required.")
        
        if not NAME_REGEX.match(profileEditForm['lastName']): 
            isValid = False
            flash("Last name required.  Only letters, spaces and hypen/dash/- allowed.")

        # leaving off password update/validation for now, same reason: more complexity.
        # password update probably ought to be handled with sep edit module if for this reason alone.
        
    @classmethod
    def getSessionUser(cls, data):
        q = 'select * from user where id = %(session_user_id)s;'
        result = connectToMySQL(cls.db).query_db(q, data)
        if len(result) <1:
            return False
        return cls(result[0])
    
    @classmethod
    def getOneUser(cls, data):
        q = 'select * from user where id = %(user_id)s;'
        result = connectToMySQL(cls.db).query_db(q, data)
        if len(result) <1:
            return False
        return cls(result[0])

    # not using below with this build yet
    @classmethod
    def get_allUser(cls, data):
        q = 'select * from user;'
        result = connectToMySQL(cls.db).query_db(q, data)
        userList = []
        for row in result:
            userList.append(cls(row))
        return userList

    # only used for login validation, as a rule.  leave funny "get_" name for now  
    @classmethod
    def get_userEmail(cls, data):
        q = 'select * from user where email = %(email)s;'
        result = connectToMySQL(cls.db).query_db(q, data)
        if len(result) <1:
            return False
        return cls(result[0])

    @classmethod
    def saveUser(cls, data):
        q = 'insert into user (userName, firstName, lastName, email, password, createdAt, updatedAt) values (%(userName)s,  %(firstName)s, %(lastName)s, %(email)s, %(password)s, NOW(), NOW() );'
        return connectToMySQL(cls.db).query_db(q, data)

    @classmethod
    def updateUser (cls, data):
        """
        q = "update user set userName = %(userName)s, email = %(email)s, firstName = %(firstName)s, lastName = %(lastName)s where id = %(user_id)s;" 
        """
        # whacked above, b/c we stepping back from allowing edits to username or email for now
        q = "update user set firstName = %(firstName)s, lastName = %(lastName)s where id = %(user_id)s;" 
        return connectToMySQL(cls.db).query_db(q, data)

    # not using below with this build yet
    @classmethod
    def updateUserEmpType (cls, data):
        q = 'update user set accessLevel = 9 where id = %(id)s;'
        return connectToMySQL(cls.db).query_db(q, data)

    # need to discuss below and why not make this a working feature. 
    @classmethod
    def delete (cls, data):
        pass
    
    """ below is junk we started working on"""
    # @classmethod
    # def getUserImageXXX(cls, data):
    #     q = 'select * from user left join image on user.id = image.user_id where user.id = %(user_id)s;'
    #     result = connectToMySQL(cls.db).query_db(q, data)
    #     userImageObj = cls (result[0])
    #     for row in result:
    #         # if row['image.id'] == None: 
    #         #     break
    #         imageData = {
    #             'id' : row['image.id']
    #             , 'imageTitle' : row['imageTitle']
    #             , 'imageInfo' : row['imageInfo']
    #             , 'filePath' : row['filePath']
    #             , 'createdAt' : row['image.createdAt']
    #             , 'updatedAt' : row['image.updatedAt']
    #             , 'user_id' : row['user_id']
    #         }
    #         userImageObj.userImagesList.append(image_mod.Image_cls(imageData))
    #     return userImageObj
