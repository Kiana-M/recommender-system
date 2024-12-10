from flask import Flask, request, jsonify
from src.model import recommend_products

app = Flask(__name__)

@app.route('/recommend', methods=['GET'])
def recommend():
    product_id = request.args.get('product_id')
    num_recommendations = int(request.args.get('num_recommendations', 5))
    recommendations = recommend_products(product_id, num_recommendations)
    return jsonify({'recommended_products': recommendations})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)