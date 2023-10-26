from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import ProductoModel, RatingModel

class Producto(Resource):
    def get(self,id):
        producto = db.session.query(ProductoModel).get_or_404(id)
        return producto.to_json()
    
    def delete(self,id):
        producto = db.session.query(ProductoModel).get_or_404(id)
        db.session.delete(producto)
        db.session.commit()
        return {'message': 'El producto fue borrado con exito'}, 204
        
    def put(self, id):
        producto = db.session.query(ProductoModel).get_or_404(id)
        if not producto:
            return {'message': 'El producto no fue encontrado'}, 404
        
        data = request.get_json()
        if 'title' in data:
            producto.titulo = data['title']
        if 'price' in data:
            producto.precio_compra = data['price']
        if 'description' in data:
            producto.description = data['description']
        if 'category' in data:
            producto.categoria = data['category']
        if 'image' in data:
            producto.url_imagen = data['image']

        rating_data = data.get('rating')
        if rating_data:
            if producto.rating:
                producto.rating.rate = rating_data.get('rate')
                producto.rating.count = rating_data.get('count')
            else:
                rating = RatingModel(
                    rate=rating_data.get('rate'),
                    count=rating_data.get('count')
                )
                producto.rating = rating
        db.session.commit()
        return producto.to_json(), 200

    

class Productos(Resource):
    def get(self):
        productos = db.session.query(ProductoModel)

        minimo_precio = request.args.get('Minimoprecio')
        maximo_precio = request.args.get('Maximoprecio')

        if minimo_precio:
            try:
                minimo_precio = float(minimo_precio)
                productos = productos.filter(ProductoModel.precio_compra >= minimo_precio)
            except ValueError:
                return {'message': 'El parámetro ingresado minimo_precio debe ser un número válido'}, 400

        if maximo_precio:
            try:
                maximo_precio = float(maximo_precio)
                productos = productos.filter(ProductoModel.precio_compra <= maximo_precio)
            except ValueError:
                return {'message': 'El parámetro ingresado maximo_precio debe ser un número válido'}, 400

        productos = productos.all()

        return jsonify([producto.to_json() for producto in productos])





    def post(self):
        data = request.get_json()
        producto_data = {
            "titulo": data.get('title'),
            "precio_compra": data.get('price'),
            "description": data.get('description'),
            "categoria": data.get('category'),
            "url_imagen": data.get('image'),
        }
        producto = ProductoModel.from_json(producto_data)
        rating_data = data.get('rating')
        if rating_data:
            rating = RatingModel(
                rate=rating_data.get('rate'),
                count=rating_data.get('count')
            )
            producto.rating = rating
            db.session.add(rating)
        db.session.add(producto)
        db.session.commit()
        return producto.to_json(), 201
    