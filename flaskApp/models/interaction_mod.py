from flaskApp.config.mysqlconnection import connectToMySQL
from flaskApp.models import user_mod
from flaskApp.models import image_mod

class Interaction_cls: 
    db = 'imageGallery_sch' # here, we are creating a reliable variable 'db' so that when we inevitably change the name of the db we are referencing, we only need to change this line to reflect that. 

    def __init__(self, data):
        self.id = data['id']
        self.comment = data['comment']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.user_id = data['user_id']
        self.image_id = data['image_id']

    @classmethod
    def saveInteraction(cls, data):
        q = "insert into interaction (comment, user_id, image_id, createdAt, updatedAt) values (%(comment)s, %(session_user_id)s, %(image_id)s, NOW(), NOW() ); " 
        return connectToMySQL(cls.db).query_db(q, data)
    
    @classmethod
    def deleteInteraction(cls, data):
        q = "delete from interaction where id = %(interaction_id)s;"
        return connectToMySQL(cls.db).query_db(q, data)

    @classmethod
    def getOneInteraction(cls, data):
        q = "select * from interaction where id = %(interaction_id)s;"
        result = connectToMySQL(cls.db).query_db(q, data)
        if len(result) <1:
            return False
        return cls(result[0])
