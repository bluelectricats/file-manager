from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    extension = db.Column(db.String(10), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    path = db.Column(db.String(200), nullable=False)
    created_on = db.Column(db.String(200))
    changed_on = db.Column(db.String(200))
    commentary = db.Column(db.Text)
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'extension': self.extension,
            'size': self.size,
            'path': self.path,
            'created_on': self.created_on,
            'changed_on': self.changed_on,
            'commentary': self.commentary
            }
