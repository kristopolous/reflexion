# Reflexion API Reference

## Base URL
`http://localhost:5000`

## Endpoints

### POST /generate
**Description:** Generate platform-specific ad creatives from a base image and optional brand context.

**Request Body:**
```json
{
  "image": "https://example.com/base-image.jpg",
  "resolution": "1080x1920",
  "url": "https://brand-website.com"
}
```

**Parameters:**
- `image` (optional): Base image URL for creative generation (default: baseline.png)
- `resolution` (optional): Target resolution (default: "1080x1920")
- `url` (optional): Website/blog URL or local file path (blog.txt) to extract brand tone from
- `demographic` (optional): Index in demo.json to use demographic-specific tone

**Response:**
```json
{
  "media_kit": {
    "facebook": {
      "url": "https://generated-creative.com/fb-variant",
      "format": "story"
    },
    "instagram": {
      "url": "https://generated-creative.com/ig-variant",
      "format": "reel"
    },
    "tiktok": {
      "url": "https://generated-creative.com/tt-variant",
      "format": "video"
    }
  },
  "status": "ready",
  "kit_id": "reflexion_kit_20250621"
}
```

**Error Responses:**
- `400 Bad Request`: Missing base image URL
- `500 Internal Server Error`: Generation failure (not yet implemented)

## Testing
Use curl to test:
```bash
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"image": "https://picsum.photos/1080/1920"}'