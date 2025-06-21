import json
from flask import Flask, request, jsonify, send_from_directory
import requests
import os
import uuid
from flask_cors import CORS
from markitdown import MarkItDown
import litellm
from bs4 import BeautifulSoup

app = Flask(__name__, static_folder='fe')
CORS(app)

BFL_API_KEY = os.environ.get('BFL_API_KEY')
BFL_API_URL = 'https://api.bfl.ai/v1/flux-kontext-max'
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('fe', path)

@app.route('/images/<image_id>')
def serve_image(image_id):
    return send_from_directory('images', image_id)

def generate_variants(base_image, resolution, prompt="A fantastic image"):
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
    try:
        response = requests.get(url)
        response.raise_for_status()
        md = MarkItDown(response.text)
        return md
    except Exception as e:
        print(f"Error scraping URL: {e}")
        return ""

@app.route('/scrape_and_refine')
def scrape_and_refine():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Missing URL parameter"}), 400
    
    try:
        scraped_content = scrape_brand_tone(url)
        if not scraped_content:
            return jsonify({"error": "Failed to scrape content from URL"}), 500

        # Refine the prompt using LiteLLM
        messages = [{"role": "system", "content": "You are a marketing expert.  Create a short prompt (max 20 words) to generate an image that reflects the brand in the following text:"},
                    {"role": "user", "content": scraped_content}]
        try:
            response = litellm.completion(model="openrouter/google/gemini-2.0-flash-exp:free", messages=messages, api_key=OPENROUTER_API_KEY)
            refined_prompt = response.choices[0].message.content
        except Exception as e:
            refined_prompt = f"Error generating refined prompt: {e}"

        return jsonify({"prompt": refined_prompt})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate', methods=['POST'])
def generate():
    data = request.form  # Access form data instead of json
    
    base_image = data.get('image', 'baseline.png')
    resolution = data.get('resolution', '1080x1920')
    prompt = data.get('prompt', "A fantastic image")
    
    variants = generate_variants(base_image, resolution, prompt)
    
    return jsonify({
        'media_kit': variants,
        'status': 'ready',
        'kit_id': 'reflexion_kit_20250621'
    })

if __name__ == '__main__':
    os.makedirs("images", exist_ok=True)
    app.run(debug=True, port=5000)