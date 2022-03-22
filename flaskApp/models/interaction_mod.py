from flaskApp.config.mysqlconnection import connectToMySQL

class Interaction_cls: 
    db = 'imageGallery_sch' # here, we are creating a reliable variable 'db' so that when we inevitably change the name of the db we are referencing, we only need to change this line to reflect that. 

    def __init__(self, data):
        self.id = data['id']
        self.comment = data['comment']
        # self.filePath = data['filePath']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.user_id = data['user_id']
        self.image_id = data['image_id']
    
    @classmethod
    def getAll(cls): 
        q = 'select * from interaction;'
        result = connectToMySQL(cls.db).query_db(q)
        interactionList = []
        for row in result: 
            interactionList.append(cls(row))
        return interactionList

    @classmethod
    def getOne(cls, data):
        q = "select * from interaction where id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(q, data)
        if len(result) <1:
            return False    
        return cls(result[0])

    @classmethod
    def save(cls, data):
        q = "insert into interaction (comment, user_id, image_id) values (%(comment)s, %(user_id)s, %(image_id)s; " 
        return connectToMySQL(cls.db).query_db(q, data)
    
    @classmethod
    def update(cls, data):
        q = "update interaction set comment = %(comment)s  where id = %(id)s;" 
        return connectToMySQL(cls.db).query_db(q, data)
    
    @classmethod
    def delete(cls, data):
        q = "delete from interaction where id = %(id)s;"
        return connectToMySQL(cls.db).query_db(q, data)

            
