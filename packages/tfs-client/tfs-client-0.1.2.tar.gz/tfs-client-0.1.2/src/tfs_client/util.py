import base64
import os
from .http import predict

def read64(path: str) -> str:
  """Read an image as URL-safe base64"""
  with open(path, 'rb') as f:
    bytes = f.read()
    return base64.urlsafe_b64encode(bytes).decode()
  
def box_path(player: int = 0, ply: int = 0, images_path: str = './images'):
  """Box path (use with `cit images`)"""
  return os.path.join(images_path, 'boxes', f'boxes-{player}-{ply}.jpg')

async def box_predict(player: int = 0, ply: int = 0, images_path: str = './images', host: str = 'http://localhost', port: int = 8501, endpoint: str = '/v1/models/ocr:predict'):
  """Predict a box from `cit images` (use `cit ocr` to start the container)"""
  img = read64(box_path(player, ply, images_path))
  return await predict([img])

async def boxes_predict(player: int = 0, plys: list[int] = range(16), images_path: str = './images', host: str = 'http://localhost', port: int = 8501, endpoint: str = '/v1/models/ocr:predict'):
  """Predict boxes from `cit images` (use `cit ocr` to start the container)"""
  imgs = [read64(box_path(player, ply, images_path)) for ply in plys]
  return await predict(imgs)
