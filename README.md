# Mapillary-Image-Tool
![image](https://user-images.githubusercontent.com/50364307/131366962-d3fb574c-b5dc-44cd-bf94-fd28e157d887.png)

Part of code is adapted from [cbeddow](https://gist.github.com/cbeddow/79d68aa6ed0f028d8dbfdad2a4142cf5)'s work
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
- Increase image resolution
- Add markers of image available on the map
