import json
from flask import Flask, request, jsonify, send_from_directory
import requests
import os
import uuid
from flask_cors import CORS
import base64, time
from urllib.parse import urlparse

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

def generate_variants(base_image, resolution, prompt):
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
        'aspect_ratio': aspect_ratio,
        'output_format': 'jpeg',
        'safety_tolerance': 2
    }
    try:
        imgStack = []
        for asp in "1:1", "16:9", "9:16":
            data['aspect_ratio'] = asp
            response = requests.post(BFL_API_URL, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            task_id = result['id']
            polling_url = result['polling_url']

            # --- Poll until image is ready ---
            for attempt in range(20):  # wait up to ~20s
                poll_resp = requests.get(polling_url, headers=headers)
                poll_resp.raise_for_status()
                poll_data = poll_resp.json()
                print(poll_data)

                if poll_data.get("result") is not None:
                    image_url = poll_data["result"].get("sample")
                    break
                elif poll_data.get("status") == "failed":
                    raise Exception("Image generation failed")
                time.sleep(1.0)
            else:
                raise Exception("Polling timed out")

            # --- Download and store the final image ---
            image_id = uuid.uuid4().hex + ".jpg"
            os.makedirs("images", exist_ok=True)
            image_path = os.path.join("images", image_id)

            img_resp = requests.get(image_url)
            img_resp.raise_for_status()

            with open(image_path, "wb") as f:
                f.write(img_resp.content)

            image_url = f"/images/{image_id}"
            imgStack.append(image_url)

        return {
            'facebook': {'url': imgStack[0], 'format': 'story', 'description': 'Facebook ad'},
            'instagram': {'url': imgStack[1], 'format': 'reel', 'description': 'Instagram ad'},
            'tiktok': {'url': imgStack[2], 'format': 'video', 'description': 'TikTok ad'}
        }

    except requests.exceptions.RequestException as e:
        print(f"Error calling BFL API: {e}")
        return {
            'facebook': {'url': None, 'format': 'story', 'description': 'Failed to generate'},
            'instagram': {'url': None, 'format': 'reel', 'description': 'Failed to generate'},
            'tiktok': {'url': None, 'format': 'video', 'description': 'Failed to generate'}
        }

def scrape_brand_tone(url):
    # TODO: Implement crawlee logic here
    return "Crawlee implementation needed"
    

def extract_with_markitdown(url):
    """Extract content using Microsoft's markitdown"""
    try:
        from markitdown import MarkItDown
        
        md = MarkItDown()
        result = md.convert_url(url)
        
        # Extract title from the first heading or use filename
        title = "No title found"
        lines = result.text_content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('# '):
                title = line[2:].strip()
                break
            elif line and not line.startswith('*') and len(line) > 10:
                # Use first substantial line as title
                title = line[:100] + "..." if len(line) > 100 else line
                break
        
        return {
            'success': True,
            'title': title,
            'content': result.text_content.strip(),
            'url': url,
            'method': 'markitdown'
        }
        
    except ImportError:
        raise Exception("markitdown not installed. Install with: pip install markitdown")
    except Exception as e:
        raise Exception(f"markitdown extraction failed: {str(e)}")

async def extract_with_crawlee(url):
    """Extract content using Crawlee"""
    try:
        from crawlee.playwright_crawler import PlaywrightCrawler, PlaywrightCrawlingContext
        
        extracted_data = {}
        
        async def handler(context: PlaywrightCrawlingContext) -> None:
            page = context.page
            
            # Wait for page to load
            await page.wait_for_load_state('networkidle')
            
            # Extract title
            title = await page.title()
            
            # Try to find main content using common selectors
            content_selectors = [
                'article',
                '[role="main"]',
                'main',
                '.post-content',
                '.entry-content',
                '.content',
                '.article-content',
                '.post-body'
            ]
            
            content = ""
            for selector in content_selectors:
                try:
                    element = await page.query_selector(selector)
                    if element:
                        content = await element.inner_text()
                        if content and len(content.strip()) > 100:
                            break
                except:
                    continue
            
            # Fallback to body if no main content found
            if not content or len(content.strip()) < 100:
                body = await page.query_selector('body')
                if body:
                    content = await body.inner_text()
            
            # Clean up content
            content = '\n'.join(line.strip() for line in content.split('\n') if line.strip())
            
            extracted_data['title'] = title or "No title found"
            extracted_data['content'] = content
            extracted_data['url'] = url
            extracted_data['method'] = 'crawlee'
        
        # Create crawler
        crawler = PlaywrightCrawler(
            request_handler=handler,
            headless=True,
            max_requests_per_crawl=1
        )
        
        # Run crawler
        await crawler.run([url])
        
        if not extracted_data:
            raise Exception("No data extracted")
        
        return {
            'success': True,
            **extracted_data
        }
        
    except ImportError:
        raise Exception("crawlee not installed. Install with: pip install crawlee[playwright]")
    except Exception as e:
        raise Exception(f"crawlee extraction failed: {str(e)}")

def extract_content(url):
    """Main extraction function that tries multiple methods"""
    
    # Validate URL
    parsed_url = urlparse(url)
    if not parsed_url.scheme or not parsed_url.netloc:
        return {'success': False, 'error': 'Invalid URL format'}
    
    # Try markitdown first (faster and cleaner for most content)
    try:
        return extract_with_markitdown(url)
    except Exception as markitdown_error:
        print(f"markitdown failed: {markitdown_error}")
        
        # Try crawlee as fallback (better for complex JS sites)
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(extract_with_crawlee(url))
            loop.close()
            return result
        except Exception as crawlee_error:
            print(f"crawlee failed: {crawlee_error}")
            
            return {
                'success': False, 
                'error': f'Both extraction methods failed. markitdown: {str(markitdown_error)}, crawlee: {str(crawlee_error)}'
            }

@app.route('/scrape_and_refine')
def scrape_and_refine():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Missing URL parameter"}), 400
    
    try:
        scraped_content = extract_content(url)
        
        # Refine the prompt using LiteLLM
        messages = [{"role": "system", "content": "You are a stable diffusion prompt engineer. Create a short image generation prompt to generate an advertising asset that could be used to promote the following blog post:"},
                    {"role": "user", "content": scraped_content['content']}]
        try:
            response = litellm.completion(
                model="openrouter/google/gemini-2.0-flash-exp:free", 
                messages=messages, 
                api_key=OPENROUTER_API_KEY)
            refined_prompt = response.choices[0].message.content
        except Exception as e:
            refined_prompt = f"Error generating refined prompt: {e}"

        return jsonify({"prompt": refined_prompt})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
  
@app.route('/api/extract')
def api_extract():
    """Extract content from URL via GET"""
    url = request.args.get('url')
    
    if not url:
        return jsonify({'success': False, 'error': 'URL parameter is required'})
    
    try:
        result = extract_content(url)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
def encode_image_to_data_uri(image_file):
    # Read the file into memory
    image_bytes = image_file.read()

    # Encode to base64
    encoded = base64.b64encode(image_bytes).decode('utf-8')
    return encoded

@app.route('/generate', methods=['POST'])
def generate():
    data = request.form  # Access form data instead of json
    
    base_image = request.files.get('image')
    if base_image:
        base_image = encode_image_to_data_uri(base_image)
    resolution = data.get('resolution', '512x512')
    context = data.get('context')
    prompt = data.get('prompt', "A fantastic image")
    ageRange = data.get('ageRange', '18-35')
    gender = data.get('gender', 'any')
    location = data.get('location', 'USA')
    interests = data.get('interests', 'any')
    freeformText = data.get('freeformText', '')
    prompt = f"{context} involving a person from or content culturally relevant to {location} {gender} gender, {interests} interests and {ageRange} years old. {freeformText}"

    variants = generate_variants(base_image, resolution, prompt)
    print(prompt)
    return jsonify({
        'media_kit': variants,
        'status': 'ready',
        'kit_id': 'reflexion_kit_20250621'
    })

if __name__ == '__main__':
    os.makedirs("images", exist_ok=True)
    app.run(debug=True, port=5000) 