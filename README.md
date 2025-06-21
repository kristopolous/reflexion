# Reflexion - AI-Powered Creative Variant System

## Overview
Reflexion is a Flask-based API that generates platform-specific ad creatives for Facebook, Instagram, and TikTok. It accepts a base image, target resolution, and optionally a blog post or website URL to extract brand tone.

## Features
- Generates background and layout variants
- Creates CTA overlays and type treatments
- Produces style remixes based on scraped brand tone
- Outputs format-aware renderings for different platforms
- Bundles outputs into ready-to-test media kits

## Implementation Decisions
- Used Flask for its simplicity and ease of deployment
- Implemented placeholder functions for image generation and brand tone scraping
- Included CORS for cross-origin requests
- Created a single `/generate` endpoint for the core functionality
- Used JSON for request/response format
- Added basic error handling for missing parameters

## Future Improvements
- Implement actual AI image generation logic (currently using placeholder URLs)
- Add support for local file paths in brand tone analysis (blog.txt and demo.json)
- Include image manipulation libraries for real transformations
- Add support for more input formats and output platforms
- Implement media kit storage and retrieval

## Getting Started
1. Install dependencies: `pip install flask pillow flask_cors`
2. Run the app: `python app.py`
3. Send POST requests to `http://localhost:5000/generate` with the required JSON payload