from flaskApp.config.mysqlconnection import connectToMySQL
from flaskApp.models import user_mod
from flaskApp.models import interaction_mod

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
        
        self.createdByUser = None
        self.InteractionSolutionVar = None

        self.InteractionsOnImageList = [] #added, trying to do method like the learn platform tells me to. 

    @classmethod
    def getAllImageOneUser(cls, data): 
        q = 'select * from image where user_id = %(user_id)s order by createdAt desc;'
        result = connectToMySQL(cls.db).query_db(q, data)
        imageList = []
        for row in result: 
            imageList.append(cls(row))
        return imageList
    
    """
    @classmethod
    def getAllImageAllUser(cls): 
        q = 'select * from image order by createdAt desc;'
        result = connectToMySQL(cls.db).query_db(q)
        imageList = []
        for row in result: 
            imageList.append(cls(row))
        return imageList
    
    """

    # below perfected with help of Caden; 5pm 3/23/2022
    @classmethod
    def getAllImageAllUser(cls):
        q = 'select * from image left join user on image.user_id = user.id order by image.createdAt desc;'
        result = connectToMySQL(cls.db).query_db(q)
        # print(result)
        allImageAllUserList = []
        for row in result:
            # begin the boilerplate for table data we're joining/grabbing with next line
            userImageObj = cls (row)
            #dont forget: below dataset needs to include ALL fields in the table we are left joining to
            userData = {
                'id' : row['user.id']
                , 'userName' : row['userName']
                , 'email' : row['email']
                , 'firstName' : row['firstName']
                , 'lastName' : row['lastName']
                , 'password' : row['password']
                , 'accessLevel' : row['accessLevel']
                , 'createdAt' : row['user.createdAt']
                , 'updatedAt' : row['user.updatedAt']
            }           
            oneUser = user_mod.User_cls(userData)
            userImageObj.createdByUser = oneUser
            # end boilerplate 

            allImageAllUserList.append(userImageObj)

        return allImageAllUserList

    #below is editted version of above; goal: just ONE image and it's user data.  it works, but could make this a lot simpler with refactored approach; get back to that later. 
    @classmethod
    def getOneImageOneUser(cls, data):
        q = 'select * from image left join user on image.user_id = user.id where image.id = %(image_id)s;'
        result = connectToMySQL(cls.db).query_db(q, data)
        # print(result)
        allImageAllUserList = []
        for row in result:
            # begin the boilerplate for table data we're joining/grabbing with next line
            userImageObj = cls (row)
            userData = {
                'id' : row['user.id']
                , 'userName' : row['userName']
                , 'email' : row['email']
                , 'firstName' : row['firstName']
                , 'lastName' : row['lastName']
                , 'password' : row['password']
                , 'accessLevel' : row['accessLevel']
                , 'createdAt' : row['user.createdAt']
                , 'updatedAt' : row['user.updatedAt']
            }           
            oneUser = user_mod.User_cls(userData)
            userImageObj.createdByUser = oneUser
            # end boilerplate 

            # for add'l tables/objects, next line stays, except NOW add on the othe objects to the parenthesis, preceded by comma 
            allImageAllUserList.append(userImageObj)

        return allImageAllUserList

    @classmethod
    def getOneImage(cls, data):
        q = "select * from image where id = %(image_id)s;"
        result = connectToMySQL(cls.db).query_db(q, data)
        if len(result) <1:
            return False    
        return cls(result[0])

    @classmethod
    def save(cls, data):
        q = "insert into image (imageTitle, imageInfo, filePath, user_id, createdAt, updatedAt) values (%(imageTitle)s, %(imageInfo)s, %(filePath)s, %(user_id)s, NOW(), NOW() ); " 
        return connectToMySQL(cls.db).query_db(q, data)
    
    @classmethod
    def update(cls, data):
        q = "update image set filePath = %(filePath)s, imageTitle = %(imageTitle)s, imageInfo = %(imageInfo)s where id = %(id)s;" 
        return connectToMySQL(cls.db).query_db(q, data)
    
    @classmethod
    def deleteImage(cls, data):
        q = "delete from image where id = %(image_id)s;"
        return connectToMySQL(cls.db).query_db(q, data)

# working on interations display here!
    @classmethod
    def getOneImageAllInterAllUser(cls, data):
        q = "select * from image left join interaction on image.id = interaction.image_id left join user on interaction.user_id = user.id where image.id = %(image_id)s order by interaction.createdAt desc;"
        result = connectToMySQL(cls.db).query_db(q, data)
        getOneImageAllInterAllUserList = []
        for row in result:
            userImageObj = cls (row)
            
            # begin repurpose
            interactionData = {
                'id' : row['interaction.id']
                , 'comment' : row['comment']
                , 'createdAt' : row['interaction.createdAt']
                , 'updatedAt' : row['interaction.updatedAt']
                , 'user_id' : row['interaction.user_id']
                , 'image_id' : row['image_id']
            }           
            someVariable = interaction_mod.Interaction_cls(interactionData)
            userImageObj.InteractionSolutionVar = someVariable
            # end repurpose 
            
            # begin the boilerplate for table data we're joining/grabbing with next line
            userData = {
                'id' : row['user.id']
                , 'userName' : row['userName']
                , 'email' : row['email']
                , 'firstName' : row['firstName']
                , 'lastName' : row['lastName']
                , 'password' : row['password']
                , 'accessLevel' : row['accessLevel']
                , 'createdAt' : row['user.createdAt']
                , 'updatedAt' : row['user.updatedAt']
            }           
            oneUser = user_mod.User_cls(userData)
            userImageObj.createdByUser = oneUser
            # end boilerplate 

            # for add'l tables/objects, next line stays, except NOW add on the othe objects to the parenthesis, preceded by comma 
            getOneImageAllInterAllUserList.append(userImageObj)
            # print(getOneImageAllInterAllUserList[0].InteractionSolutionVar.id)
        return getOneImageAllInterAllUserList

