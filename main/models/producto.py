from .. import db

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255),nullable=False)
    precio_compra = db.Column(db.Numeric(precision=10,scale=2),nullable=False)
    description = db.Column(db.String(255))
    categoria = db.Column(db.String(255))
    url_imagen = db. Column(db.String(255))

    rating = db.relationship('Rating', uselist=False, back_populates='producto', cascade='all, delete-orphan')

    def __repr__(self):
        return '<Producto: %r %r %r %r %r>'% (self.titulo, self.precio_compra, self.description, self.categoria, self.url_imagen)
    

    def to_json(self):
        producto_json = {
            'id': self.id,
            'titulo': str(self.titulo),
            'precio_compra': str(self.precio_compra),
            'description': str(self.description),
            'categoria': str(self.categoria),
            'url_imagen': str(self.url_imagen),

        }
        return producto_json


    @staticmethod
    def from_json(producto_json):
        id = producto_json.get('id')
        titulo = producto_json.get('titulo')
        precio_compra = producto_json.get('precio_compra')
        description = producto_json.get('description')
        categoria = producto_json.get('categoria')
        url_imagen = producto_json.get('url_imagen')
        return Producto(id=id,
                    titulo=titulo,
                    precio_compra=precio_compra,
                    description=description,
                    categoria=categoria,
                    url_imagen=url_imagen
                    )