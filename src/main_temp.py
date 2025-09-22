from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Mock data for testing
MOCK_MODELS = [
    {
        "id": 47,
        "slug": "aria-valen",
        "name": "Aria Valen",
        "thumbnail_url": "https://storage.googleapis.com/cyberchicmodels-media/models/thumbnails/47-aria-valen-thumbnail.webp"
    },
    {
        "id": 57,
        "slug": "camila-huaman", 
        "name": "Camila Huaman",
        "thumbnail_url": "https://storage.googleapis.com/cyberchicmodels-media/models/thumbnails/57-camila-huaman-thumbnail.webp"
    },
    {
        "id": 56,
        "slug": "elara-vey",
        "name": "Elara Vey", 
        "thumbnail_url": "https://storage.googleapis.com/cyberchicmodels-media/models/thumbnails/56-elara-vey-thumbnail.webp"
    },
    {
        "id": 49,
        "slug": "freja-madsen",
        "name": "Freja Madsen",
        "thumbnail_url": "https://storage.googleapis.com/cyberchicmodels-media/models/thumbnails/49-freja-madsen-thumbnail.webp"
    },
    {
        "id": 52,
        "slug": "layal-n",
        "name": "Layal N",
        "thumbnail_url": "https://storage.googleapis.com/cyberchicmodels-media/models/thumbnails/52-layal-n-thumbnail.webp"
    }
]

MOCK_IMAGES = {
    47: [
        {
            "id": 1,
            "model_id": 47,
            "collection": "Main",
            "image_url": "https://storage.googleapis.com/cyberchicmodels-media/models/images/47-aria-valen/main/aria_main_001.webp"
        },
        {
            "id": 2, 
            "model_id": 47,
            "collection": "Editorial",
            "image_url": "https://storage.googleapis.com/cyberchicmodels-media/models/images/47-aria-valen/editorial/aria_editorial_001.webp"
        }
    ]
}

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "message": "CyberChicModels API is running"
    })

@app.route('/api/models', methods=['GET'])
def get_models():
    return jsonify(MOCK_MODELS)

@app.route('/api/models/<int:model_id>/images', methods=['GET'])
def get_model_images(model_id):
    images = MOCK_IMAGES.get(model_id, [])
    return jsonify(images)

@app.route('/api/models/<slug>', methods=['GET'])
def get_model_by_slug(slug):
    model = next((m for m in MOCK_MODELS if m['slug'] == slug), None)
    if not model:
        return jsonify({"error": "Model not found"}), 404
    
    # Add images to the model
    model_with_images = model.copy()
    model_with_images['images'] = MOCK_IMAGES.get(model['id'], [])
    
    return jsonify(model_with_images)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
