from pyzbar.pyzbar import decode
from PIL import Image

class QrParser:
    f = "t.jpeg"
    qrs = decode(Image.open(f))
    url = qrs[0].data
