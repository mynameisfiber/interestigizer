from flask import Flask, request, send_file
import cStringIO

import interestingizer
from PIL import Image

import random
import os

app = Flask(__name__)

class WSGICopyBody(object):
    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        length = environ.get('CONTENT_LENGTH', '0')
        length = 0 if length == '' else int(length)

        body = environ['wsgi.input'].read(length)
        environ['body_copy'] = body
        environ['wsgi.input'] = cStringIO.StringIO(body)

        # Call the wrapped application
        app_iter = self.application(environ, 
                                    self._sr_callback(start_response))

        # Return modified response
        return app_iter

    def _sr_callback(self, start_response):
        def callback(status, headers, exc_info=None):

            # Call upstream start_response
            start_response(status, headers, exc_info)
        return callback

app.wsgi_app = WSGICopyBody(app.wsgi_app)

items_base = "./images/"
items = [Image.open(os.path.join(items_base, filename)).convert("RGBA") for filename in os.listdir(items_base)]

@app.route("/ping")
def ping():
    return "OK"

def serve_pil_image(pil_img):
    img_io = cStringIO.StringIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

@app.route("/interestingize", methods=["POST",])
def interestingize():
    #image_raw = request.data
    image_raw = request.environ['body_copy']
    if image_raw:
        try:
            image = Image.open(cStringIO.StringIO(image_raw))
        except IOError:
            return "Could not decode image", 500

        item = random.choice(items).copy()

        try:
            better_image = interestingizer.interestingize(image, item)
            return serve_pil_image(better_image)
        except:
            return "Could not interestingize", 500
    else:
        return "Must provide image in post body", 500


if __name__ == "__main__":
    app.debug = True
    app.run()
