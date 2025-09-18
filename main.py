from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from google.cloud import storage
from google.cloud import sql
import psycopg2
from datetime import datetime, timedelta
import uuid

app = Flask(__name__)

# CORS Configuration - This fixes the main issue
CORS(app, 
     origins=['https://cyberchicmodels-frontend.vercel.app'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization'],
     supports_credentials=True)

# Database configuration
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', '34.72.97.207'),
    'database': os.environ.get('DB_NAME', 'cyberchicmodels'),
    'user': os.environ.get('DB_USER', 'postgres'),
    'password': os.environ.get('DB_PASSWORD', 'CyberChic2024!'),
    'port': os.environ.get('DB_PORT', '5432')
}

# Google Cloud Storage configuration
GCS_BUCKET = 'cyberchicmodels-media'
storage_client = storage.Client()

def get_db_connection():
    """Get database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'CyberChicModels API is running',
        'cors_enabled': True,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/models', methods=['GET', 'POST'])
def handle_models():
    """Handle models API"""
    if request.method == 'GET':
        try:
            conn = get_db_connection()
            if not conn:
                return jsonify({'error': 'Database connection failed'}), 500
            
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, nationality, ethnicity, gender, age, height, weight, 
                       bio, hobbies, specialties, is_featured, is_new, is_coming, 
                       is_popular, price_usd, status, created_at
                FROM models 
                WHERE status = 'active'
                ORDER BY created_at DESC
            """)
            
            models = []
            for row in cursor.fetchall():
                models.append({
                    'id': row[0],
                    'name': row[1],
                    'nationality': row[2],
                    'ethnicity': row[3],
                    'gender': row[4],
                    'age': row[5],
                    'height': row[6],
                    'weight': row[7],
                    'bio': row[8],
                    'hobbies': row[9],
                    'specialties': row[10],
                    'is_featured': row[11],
                    'is_new': row[12],
                    'is_coming': row[13],
                    'is_popular': row[14],
                    'price_usd': float(row[15]) if row[15] else 0,
                    'status': row[16],
                    'created_at': row[17].isoformat() if row[17] else None
                })
            
            cursor.close()
            conn.close()
            
            return jsonify({
                'models': models,
                'count': len(models)
            })
            
        except Exception as e:
            return jsonify({'error': f'Failed to fetch models: {str(e)}'}), 500
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            
            conn = get_db_connection()
            if not conn:
                return jsonify({'error': 'Database connection failed'}), 500
            
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO models (name, nationality, ethnicity, gender, age, height, weight, 
                                  bio, hobbies, specialties, is_featured, is_new, is_coming, 
                                  is_popular, price_usd, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                data.get('name'),
                data.get('nationality'),
                data.get('ethnicity'),
                data.get('gender'),
                data.get('age'),
                data.get('height'),
                data.get('weight'),
                data.get('bio'),
                data.get('hobbies'),
                data.get('specialties'),
                data.get('is_featured', False),
                data.get('is_new', True),
                data.get('is_coming', False),
                data.get('is_popular', False),
                data.get('price_usd', 0),
                'active'
            ))
            
            model_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            conn.close()
            
            return jsonify({
                'message': 'Model created successfully',
                'model_id': model_id
            }), 201
            
        except Exception as e:
            return jsonify({'error': f'Failed to create model: {str(e)}'}), 500

@app.route('/api/styles', methods=['GET', 'POST'])
def handle_styles():
    """Handle styles API"""
    if request.method == 'GET':
        try:
            conn = get_db_connection()
            if not conn:
                return jsonify({'error': 'Database connection failed'}), 500
            
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, category, description, colors, sizes, price_usd, 
                       is_featured, status, created_at
                FROM styles 
                WHERE status = 'active'
                ORDER BY created_at DESC
            """)
            
            styles = []
            for row in cursor.fetchall():
                styles.append({
                    'id': row[0],
                    'name': row[1],
                    'category': row[2],
                    'description': row[3],
                    'colors': row[4],
                    'sizes': row[5],
                    'price_usd': float(row[6]) if row[6] else 0,
                    'is_featured': row[7],
                    'status': row[8],
                    'created_at': row[9].isoformat() if row[9] else None
                })
            
            cursor.close()
            conn.close()
            
            return jsonify({
                'styles': styles,
                'count': len(styles)
            })
            
        except Exception as e:
            return jsonify({'error': f'Failed to fetch styles: {str(e)}'}), 500
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            
            conn = get_db_connection()
            if not conn:
                return jsonify({'error': 'Database connection failed'}), 500
            
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO styles (name, category, description, colors, sizes, price_usd, 
                                  is_featured, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                data.get('name'),
                data.get('category'),
                data.get('description'),
                json.dumps(data.get('colors', [])),
                json.dumps(data.get('sizes', [])),
                data.get('price_usd', 0),
                data.get('is_featured', False),
                'active'
            ))
            
            style_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            conn.close()
            
            return jsonify({
                'message': 'Style created successfully',
                'style_id': style_id
            }), 201
            
        except Exception as e:
            return jsonify({'error': f'Failed to create style: {str(e)}'}), 500

@app.route('/api/hero-slides', methods=['GET', 'POST'])
def handle_hero_slides():
    """Handle hero slides API"""
    if request.method == 'GET':
        try:
            conn = get_db_connection()
            if not conn:
                return jsonify({'error': 'Database connection failed'}), 500
            
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, title, subtitle, button_text, button_link, description, 
                       background_color, display_order, is_active, is_featured, created_at
                FROM hero_slides 
                WHERE is_active = true
                ORDER BY display_order ASC
            """)
            
            slides = []
            for row in cursor.fetchall():
                slides.append({
                    'id': row[0],
                    'title': row[1],
                    'subtitle': row[2],
                    'button_text': row[3],
                    'button_link': row[4],
                    'description': row[5],
                    'background_color': row[6],
                    'display_order': row[7],
                    'is_active': row[8],
                    'is_featured': row[9],
                    'created_at': row[10].isoformat() if row[10] else None
                })
            
            cursor.close()
            conn.close()
            
            return jsonify({
                'slides': slides,
                'count': len(slides)
            })
            
        except Exception as e:
            return jsonify({'error': f'Failed to fetch hero slides: {str(e)}'}), 500
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            
            conn = get_db_connection()
            if not conn:
                return jsonify({'error': 'Database connection failed'}), 500
            
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO hero_slides (title, subtitle, button_text, button_link, 
                                       description, background_color, display_order, 
                                       is_active, is_featured)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                data.get('title'),
                data.get('subtitle'),
                data.get('button_text'),
                data.get('button_link'),
                data.get('description'),
                data.get('background_color', '#667eea'),
                data.get('display_order', 1),
                data.get('is_active', True),
                data.get('is_featured', False)
            ))
            
            slide_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            conn.close()
            
            return jsonify({
                'message': 'Hero slide created successfully',
                'slide_id': slide_id
            }), 201
            
        except Exception as e:
            return jsonify({'error': f'Failed to create hero slide: {str(e)}'}), 500

@app.route('/api/upload-url', methods=['POST'])
def generate_upload_url():
    """Generate signed URL for direct GCS upload"""
    try:
        data = request.get_json()
        filename = data.get('filename')
        content_type = data.get('content_type', 'image/jpeg')
        
        # Generate unique filename
        unique_filename = f"{uuid.uuid4()}_{filename}"
        
        # Generate signed URL
        bucket = storage_client.bucket(GCS_BUCKET)
        blob = bucket.blob(unique_filename)
        
        url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(minutes=15),
            method="PUT",
            content_type=content_type
        )
        
        return jsonify({
            'upload_url': url,
            'file_path': unique_filename,
            'public_url': f'https://storage.googleapis.com/{GCS_BUCKET}/{unique_filename}'
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to generate upload URL: {str(e)}'}), 500

@app.route('/api/images/confirm', methods=['POST'])
def confirm_image_upload():
    """Confirm image upload and save metadata to database"""
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO images (entity_type, entity_id, image_type, file_path, 
                              public_url, description, display_order)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            data.get('entity_type'),  # 'model', 'style', 'hero_slide'
            data.get('entity_id'),
            data.get('image_type'),   # 'thumbnail', 'gallery', 'hero', etc.
            data.get('file_path'),
            data.get('public_url'),
            data.get('description'),
            data.get('display_order', 1)
        ))
        
        image_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            'message': 'Image metadata saved successfully',
            'image_id': image_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Failed to save image metadata: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
