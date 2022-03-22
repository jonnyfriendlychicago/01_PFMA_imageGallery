from flaskApp.config.mysqlconnection import connectToMySQL
from flask import flash
from flaskApp.models import image_mod

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

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

        self.userImagesList = []

    # below is a cheeky little function to save some typing.  Think about how functions like this can be exploited in other ways. 
    def fullName(self):
        return (f"{self.firstName} {self.lastName}")

    @staticmethod
    def validate(user):
        isValid = True
        q = 'select * from user where email = %(email)s;'
        result = connectToMySQL(User_cls.db).query_db(q, user)
        if len(result) >= 1: # somewhat clumsy way (??) of saying, if one or more results!
            isValid = False
            flash("Email already in use.")
        
        # q_two = 'select * from user where userName = %(userName)s;'
        # result_two = connectToMySQL(User_cls.db).query_db(q_two, user)
        # if len(result_two) >= 1: # somewhat clumsy way (??) of saying, if one or more results!
        #     isValid = False
        #     flash("Username already in use.")

        if not EMAIL_REGEX.match(user['email']): 
            isValid = False
            flash("i=Invalid email address.")
        if len(user['firstName']) < 1: # orig code says 2 char, but 1 seems better to me.  Malcolm X !
            isValid = False
            flash("First name cannot be blank.")
        if len(user['lastName']) < 1: # orig code says 2 char, but 1 seems better to me.  Malcolm X !
            isValid = False
            flash("Last name cannot be blank.")
        # if len(user['password']) < 8:
        #     isValid = False
        #     flash("Password must be at least 8 characters, ")
        # if user['password'] != user['confirm']:
        #     isValid = False
        #     flash("Password entries must match.")
        return  isValid

    @classmethod
    def get_oneUser(cls, data):
        q = 'select * from user where id = %(user_id)s;'
        result = connectToMySQL(cls.db).query_db(q, data)
        if len(result) <1:
            return False
        return cls(result[0])

    @classmethod
    def get_allUser(cls, data):
        q = 'select * from user;'
        result = connectToMySQL(cls.db).query_db(q, data)
        userList = []
        for row in result:
            userList.append(cls(row))
        return userList

    # only used for login validation, as a rule    
    @classmethod
    def get_userEmail(cls, data):
        q = 'select * from user where email = %(email)s;'
        result = connectToMySQL(cls.db).query_db(q, data)
        if len(result) <1:
            return False
        return cls(result[0])

    @classmethod
    def saveUser(cls, data):
        # below is deliberately leaving out accessLevel... yes? 
        # also, orig code left OUT createdAt & updatedAt... which I'm adding now. 
        q = 'insert into user (userName, firstName, lastName, email, password, createdAt, updatedAt) values (%(userName)s,  %(firstName)s, %(lastName)s, %(email)s, %(password)s, NOW(), NOW() );'
        return connectToMySQL(cls.db).query_db(q, data)

    # need to discuss below and why not make this a working feature. 
    @classmethod
    def updateUser (cls, data):
        pass

    @classmethod
    def updateUserEmpType (cls, data):
        q = 'update user set accessLevel = 9 where id = %(id)s;'
        return connectToMySQL(cls.db).query_db(q, data)

    # need to discuss below and why not make this a working feature. 
    @classmethod
    def delete (cls, data):
        pass

    @classmethod
    def getUserImage(cls, data):
        q = 'select * from user left join image on user.id = image.user_id where user.id = %(user_id)s;'
        result = connectToMySQL(cls.db).query_db(q, data)
        userImageObj = cls (result[0])
        for row in result:
            # if row['image.id'] == None: 
            #     break
            imageData = {
                'id' : row['image.id']
                , 'imageTitle' : row['imageTitle']
                , 'imageInfo' : row['imageInfo']
                , 'filePath' : row['filePath']
                , 'createdAt' : row['image.createdAt']
                , 'updatedAt' : row['image.updatedAt']
                , 'user_id' : row['user_id']
            }
            userImageObj.userImagesList.append(image_mod.Image_cls(imageData))
        return userImageObj