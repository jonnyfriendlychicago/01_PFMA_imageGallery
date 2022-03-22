from flaskApp.config.mysqlconnection import connectToMySQL

class Image_cls: 
    db = 'imageGallery_sch' # here, we are creating a reliable variable 'db' so that when we inevitably change the name of the db we are referencing, we only need to change this line to reflect that. 

    def __init__(self, data):
        self.id = data['id']
        self.imageTitle = data['imageTitle']
        self.imageInfo = data['imageInfo']
        self.filePath = data['filePath']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.user_id = data['user_id']
    
    @classmethod
    def getAll(cls): 
        q = 'select * from image;'
        result = connectToMySQL(cls.db).query_db(q)
        imageList = []
        for row in result: 
            imageList.append(cls(row))
        return imageList

    @classmethod
    def getOne(cls, data):
        q = "select * from image where id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(q, data)
        if len(result) <1:
            return False    
        return cls(result[0])

    @classmethod
    def save(cls, data):
        q = "insert into image (imageTitle, imageInfo, filePath, user_id) values (%(imageTitle)s, %(imageInfo)s, %(filePath)s, %(user_id)s); " 
        return connectToMySQL(cls.db).query_db(q, data)
    
    @classmethod
    def update(cls, data):
        q = "update image set filePath = %(filePath)s, imageTitle = %(imageTitle)s, imageInfo = %(imageInfo)s where id = %(id)s;" 
        return connectToMySQL(cls.db).query_db(q, data)
    
    @classmethod
    def delete(cls, data):
        q = "delete from image where id = %(id)s;"
        return connectToMySQL(cls.db).query_db(q, data)

            
