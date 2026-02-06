# FlyerForge API 🎨

AI-powered flyer and poster generation API for businesses.

## Features

- 🎨 **7 Design Styles** - Modern, Corporate, Playful, Minimal, Bold, Elegant, Retro
- 📐 **6 Output Sizes** - Social media, A4 print, posters
- ⚡ **Fast Generation** - ~3-4 seconds per image
- 🎯 **Customizable** - Brand colors, taglines, custom elements

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set your API key
cp .env.example .env
# Edit .env with your Pollinations API key

# Run the server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/flyers/generate` | Generate a flyer |
| GET | `/api/v1/flyers/styles` | List available styles |
| GET | `/api/v1/flyers/sizes` | List available sizes |
| GET | `/health` | Health check |

## Generate Flyer

**Request:**
```json
POST /api/v1/flyers/generate

{
  "business_name": "Coffee Corner",
  "tagline": "Fresh brews daily!",
  "style": "modern",
  "size": "social_square",
  "primary_color": "#8B4513"
}
```

**Response:**
```json
{
  "success": true,
  "image_url": "data:image/jpeg;base64,/9j/4AAQ...",
  "provider": "pollinations",
  "generation_time_ms": 3500
}
```

## Styles

| Style | Description |
|-------|-------------|
| `modern` | Clean, minimalist design |
| `corporate` | Professional, business-focused |
| `playful` | Fun, colorful, approachable |
| `minimal` | Ultra-simple with white space |
| `bold` | High contrast, impactful |
| `elegant` | Sophisticated, luxury feel |
| `retro` | Vintage, nostalgic aesthetic |

## Sizes

| Size | Dimensions | Use Case |
|------|------------|----------|
| `social_square` | 1024x1024 | Instagram, Facebook |
| `social_portrait` | 1024x1280 | Instagram portrait |
| `social_story` | 768x1365 | Stories |
| `a4_portrait` | 768x1024 | Printable flyers |
| `a4_landscape` | 1024x768 | Horizontal banners |
| `poster` | 1024x1536 | Large format |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `POLLINATIONS_API_KEY` | Yes | Your Pollinations.ai API key |

## License

MIT
