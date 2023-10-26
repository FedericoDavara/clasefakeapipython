from .. import db

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rate = db.Column(db.Numeric(precision=10,scale=2),nullable=False)
    count = db.Column(db.Integer)

    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'))
    producto = db.relationship('Producto', back_populates='rating')

    def __repr__(self):
        return '<Producto: %r %r %r>'% (self.rate, self.count)
    

    def to_json(self):
        rating_json = {
            'id': self.id,
            'rate': str(self.rate),
            'count': str(self.count),
        }
        return rating_json


    @staticmethod
    def from_json(rating_json):
        id = rating_json.get('id')
        rate = rating_json.get('rate')
        count = rating_json.get('contador')
        return Rating(id=id,
                    rate=rate,
                    count=count,
                    )