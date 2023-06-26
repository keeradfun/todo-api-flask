class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(100),nullable=False)
    username = db.Column(db.String(200),nullable=False)
    password = db.Column(db.String(200),nullable=False)
    tasks = db.relationship("Task",backref="user",lazy="dynamic")
    def __repr__(self):
        return self.username
    
    # @staticmethod

    

# class Task(db.model):
#     id = db.Column(db.Iteger,primary_key=True)
#     user_id = db.Column(db.Integer,db.ForeignKey("user.id"))
#     task_text = db.Column(db.String(200),nullable=False)
