
import os
import json
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

# Database configuration
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "CyberChic2024")
DB_HOST = os.environ.get("DB_HOST", "34.72.97.207")
DB_NAME = os.environ.get("DB_NAME", "cyberchicmodels")

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# --- Database Models ---
class Model(db.Model):
    __tablename__ = 'models'
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    thumbnail_url = db.Column(db.String(255))

    def to_dict(self):
        return {
            "id": self.id,
            "slug": self.slug,
            "name": self.name,
            "thumbnail_url": self.thumbnail_url
        }

class ModelImage(db.Model):
    __tablename__ = 'model_images'
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('models.id'), nullable=False)
    collection = db.Column(db.String(255))
    image_url = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "model_id": self.model_id,
            "collection": self.collection,
            "image_url": self.image_url
        }

# --- API Endpoints ---
@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "message": "CyberChicModels API is running"
    })

@app.route('/api/models', methods=['GET'])
def get_models():
    try:
        models = Model.query.all()
        return jsonify([model.to_dict() for model in models])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/models/<int:model_id>/images', methods=['GET'])
def get_model_images(model_id):
    try:
        images = ModelImage.query.filter_by(model_id=model_id).all()
        return jsonify([image.to_dict() for image in images])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/models/<slug>', methods=['GET'])
def get_model_by_slug(slug):
    try:
        model = Model.query.filter_by(slug=slug).first()
        if not model:
            return jsonify({"error": "Model not found"}), 404
        
        images = ModelImage.query.filter_by(model_id=model.id).all()
        
        model_data = model.to_dict()
        model_data['images'] = [image.to_dict() for image in images]
        
        return jsonify(model_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)

