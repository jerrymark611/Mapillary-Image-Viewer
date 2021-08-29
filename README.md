# Mapillary-Analysis-Tool

## Prerequisites
- Python3
- fastapi
- starlette
- mercantile
- vt2geojson
- Jinja2

## Usage
Run the command below to start the server
```
uvicorn server:app --reload --port 8080
```

Then open http://localhost:8080/ using browser

Operation:
1. Drag-and-drop to render geojson on the map
2. Click on the map to get panoramic image from Mapillary

## Test Environment
Windows 10
## TODO
- Click to get the nearest image from Mapillary
- Increase image resolution
- Add marker of images available on the map
