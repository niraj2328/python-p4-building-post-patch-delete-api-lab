#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    bakeries_serialized = [bakery.to_dict() for bakery in bakeries]
    return jsonify(bakeries_serialized)

@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH'])
def get_or_update_bakery(id):
    bakery = Bakery.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify(bakery.to_dict())
    elif request.method == 'PATCH':
        for attr, value in request.form.items():
            setattr(bakery, attr, value)
        db.session.commit()
        return jsonify(bakery.to_dict())

@app.route('/baked_goods', methods=['GET', 'POST'])
def get_or_create_baked_goods():
    if request.method == 'GET':
        baked_goods_query = BakedGood.query.all()
        baked_goods_serialized = [bg.to_dict() for bg in baked_goods_query]
        return jsonify(baked_goods_serialized)
    elif request.method == 'POST':
        new_baked_good = BakedGood(
            name=request.form.get('name'),
            price=request.form.get('price'),
            bakery_id=request.form.get('bakery_id')
        )
        db.session.add(new_baked_good)
        db.session.commit()
        return jsonify(new_baked_good.to_dict()), 201

@app.route('/baked_goods/by_price')
def get_baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price).all()
    baked_goods_by_price_serialized = [bg.to_dict() for bg in baked_goods_by_price]
    return jsonify(baked_goods_by_price_serialized)

@app.route('/baked_goods/most_expensive')
def get_most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    return jsonify(most_expensive.to_dict())

@app.route('/baked_goods/<int:id>', methods=['GET', 'DELETE'])
def get_or_delete_baked_good(id):
    baked_good = BakedGood.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify(baked_good.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(baked_good)
        db.session.commit()
        return jsonify({'delete_successful': True, 'message': 'Baked good deleted'})

if __name__ == '__main__':
    app.run(port=5555, debug=True)
