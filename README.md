# Mapillary-Image-Tool

## Prerequisites
- Python3
- fastapi
- starlette
- mercantile
- vt2geojson
- Jinja2

## Usage
Download this repository and run the command below to start the server
```
uvicorn server:app --reload --port 8080
```

Then open http://localhost:8080/ using browser to complete authentication

Operation:
- Drag-and-drop to render geojson on the map
- Click on the map to get panoramic image from Mapillary

## Test Environment
Windows 10
## TODO
- Click to get the nearest image from Mapillary
- Increase image resolution
- Add marker of images available on the map
