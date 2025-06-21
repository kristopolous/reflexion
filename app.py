import json
from flask import Flask, request, jsonify, send_from_directory
import requests
import os
import uuid
from flask_cors import CORS

app = Flask(__name__, static_folder='fe')
CORS(app)

BFL_API_KEY = os.environ.get('BFL_API_KEY')
BFL_API_URL = 'https://api.bfl.ai/v1/flux-kontext-max'

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('fe', path)

@app.route('/images/<image_id>')
def serve_image(image_id):
    return send_from_directory('images', image_id)

def generate_variants(base_image, resolution, brand_tone, prompt="A fantastic image"):
    """Generate platform-specific variants using Black Forest Labs API"""
    aspect_ratio = "1:1"  # Default aspect ratio
    if resolution:
        width, height = map(int, resolution.split('x'))
        if width > height:
            aspect_ratio = "16:9"
        elif height > width:
            aspect_ratio = "9:16"

    headers = {
        'Content-Type': 'application/json',
        'x-key': BFL_API_KEY
    }
    data = {
        'prompt': prompt,
        'input_image': base_image,
        'seed': 42,
        'aspect_ratio': aspect_ratio,
        'output_format': 'jpeg',
        'safety_tolerance': 2
    }

    try:
        response = requests.post(BFL_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        task_id = result['id']
        polling_url = result['polling_url']

        # Placeholder: Implement polling logic to get the final image URL
        # For simplicity, generate a mock image and save it to the images directory
        image_id = uuid.uuid4().hex + ".jpg"
        mock_image_path = os.path.join("images", image_id)
        os.makedirs("images", exist_ok=True)
        with open(mock_image_path, "wb") as f:
            f.write(requests.get("https://picsum.photos/400/400").content) # Save a placeholder image

        image_url = f"/images/{image_id}"

        return {
            'facebook': {'url': image_url, 'format': 'story', 'description': 'Facebook ad'},
            'instagram': {'url': image_url, 'format': 'reel', 'description': 'Instagram ad'},
            'tiktok': {'url': image_url, 'format': 'video', 'description': 'TikTok ad'}
        }

    except requests.exceptions.RequestException as e:
        print(f"Error calling BFL API: {e}")
        return {
            'facebook': {'url': None, 'format': 'story', 'description': 'Failed to generate'},
            'instagram': {'url': None, 'format': 'reel', 'description': 'Failed to generate'},
            'tiktok': {'url': None, 'format': 'video', 'description': 'Failed to generate'}
        }

def scrape_brand_tone(url):
    if not url:
        return None
    if os.path.exists(url):
        with open(url, 'r') as f:
            content = f.read()
        return {'tone': 'file-based', 'keywords': ['from', 'local']}
    else:
        try:
            response = requests.get(url)
            return {'tone': 'web-scraped', 'keywords': ['from', 'url']}
        except:
            return {'tone': 'default', 'keywords': ['default']}

@app.route('/generate', methods=['POST'])
def generate():
    data = request.form  # Access form data instead of json
    
    base_image = data.get('image', 'baseline.png')
    resolution = data.get('resolution', '1080x1920')
    url = data.get('url')
    demographic = data.get('demographic')
    prompt = data.get('prompt', "A fantastic image")
    
    if demographic is not None:
        with open('demo.json', 'r') as f:
            demos = json.load(f)
        selected_demo = demos[demographic]
        brand_tone = {'tone': selected_demo['tone'], 'keywords': selected_demo['visual_keywords']}
    elif url:
        brand_tone = scrape_brand_tone(url)
    else:
        brand_tone = None
    
    variants = generate_variants(base_image, resolution, brand_tone, prompt)
    
    return jsonify({
        'media_kit': variants,
        'status': 'ready',
        'kit_id': 'reflexion_kit_20250621'
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)