import os
import sys
from flask import Flask, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'asdf#FGSgvasgf$5$WGT') # Use environment variable for secret key

# Configure Google Cloud SQL (PostgreSQL) connection
DB_USER = os.environ.get('DB_USER', 'cyberchic-admin')
DB_PASS = os.environ.get('DB_PASS', '_;,aGyNq1]}3=i4:')
DB_NAME = os.environ.get('DB_NAME', 'cyberchicmodels-db')
CLOUD_SQL_CONNECTION_NAME = os.environ.get('CLOUD_SQL_CONNECTION_NAME', 'cyberchicmodels-ai:us-central1:cyberchicmodels-db') # project_id:region:instance_id

# Use psycopg2 for PostgreSQL connection
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@/{DB_NAME}?host=/cloudsql/{CLOUD_SQL_CONNECTION_NAME}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app) # Enable CORS for all routes

# Define ModelImageCollection for SQLAlchemy
class ModelImageCollection(db.Model):
    __tablename__ = 'model_image_collections'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_id = db.Column(db.Integer, db.ForeignKey('models.id'), nullable=False) # Changed to Integer
    collection_type = db.Column(db.String(50), nullable=False)  # 'main', 'editorial', 'commercial', 'runway'
    image_urls = db.Column(db.Text)  # Comma-separated URLs

# Define Model for SQLAlchemy
class Model(db.Model):
    __tablename__ = 'models'
    id = db.Column(db.Integer, primary_key=True) # Changed to Integer
    slug = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    tagline = db.Column(db.String(255))
    nationality = db.Column(db.String(100))
    ethnicity = db.Column(db.String(100))
    gender = db.Column(db.String(50))
    age = db.Column(db.Integer)
    height = db.Column(db.String(50))
    weight = db.Column(db.String(50))
    bio = db.Column(db.Text)
    hobbies = db.Column(db.Text)
    specialties = db.Column(db.Text) # Stored as comma-separated string or JSON string
    thumbnail_url = db.Column(db.String(255))
    is_new = db.Column(db.Boolean, default=False)
    is_popular = db.Column(db.Boolean, default=False)
    is_coming_soon = db.Column(db.Boolean, default=False)
    price_usd = db.Column(db.Float)

    def to_dict(self):
        # Get image collections for this model
        collections = ModelImageCollection.query.filter_by(model_id=self.id).all()
        collections_dict = {}
        for collection in collections:
            collections_dict[f"{collection.collection_type}_photos"] = collection.image_urls.split(',') if collection.image_urls else []
        
        result = {
            'id': self.id,
            'slug': self.slug,
            'name': self.name,
            'tagline': self.tagline,
            'nationality': self.nationality,
            'ethnicity': self.ethnicity,
            'gender': self.gender,
            'age': self.age,
            'height': self.height,
            'weight': self.weight,
            'bio': self.bio,
            'hobbies': self.hobbies,
            'specialties': self.specialties.split(',') if self.specialties else [],
            'thumbnail_url': self.thumbnail_url,
            'is_new': self.is_new,
            'is_popular': self.is_popular,
            'is_coming_soon': self.is_coming_soon,
            'price_usd': self.price_usd,
        }
        
        # Add image collections
        result.update(collections_dict)
        return result

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'CyberChicModels API is running'}), 200

# API endpoint to get all models
@app.route('/api/models', methods=['GET'])
def get_models():
    try:
        models = Model.query.all()
        return jsonify([model.to_dict() for model in models])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Root endpoint
@app.route('/models', methods=['GET'])
def get_models_alt():
    return get_models()

# Initialize database tables
def init_db():
    try:
        with app.app_context():
            db.create_all()
            print("Database tables created successfully")
    except Exception as e:
        print(f"Database initialization error: {e}")

# Initialize database when module is imported
init_db()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

