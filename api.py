from flask import Flask, request, send_from_directory, redirect, url_for
import cStringIO

import interestingizer
from PIL import Image

import md5
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

TMP_DIR = "./tmp"
ITEMS_BASE = "./images/"
items = [Image.open(os.path.join(ITEMS_BASE, filename)).convert("RGBA") for filename in os.listdir(ITEMS_BASE)]


@app.route("/ping")
def ping():
    return "OK"


def cache_image(pil_img, key):
    global TMP_DIR
    with open(os.path.join(TMP_DIR, key), "w+") as fd:
        pil_img.save(fd, 'JPEG', quality=70)
    return key


@app.route("/cache/<key>")
def cache(key):
    global TMP_DIR
    return send_from_directory(TMP_DIR, key, mimetype='image/jpeg')


@app.route("/interestingize", methods=["POST",])
def interestingize():
    image_raw = request.environ['body_copy']
    if image_raw:
        try:
            image = Image.open(cStringIO.StringIO(image_raw))
            key = md5.md5(image_raw).hexdigest()
        except IOError:
            return "Could not decode image", 500

        item = random.choice(items).copy()

        try:
            better_image = interestingizer.interestingize(image, item)
            key = cache_image(better_image, key)
            return redirect(url_for('cache', key=key))
        except:
            return "Could not interestingize", 500
    else:
        return "Must provide image in post body", 500


if __name__ == "__main__":
    app.debug = True
    app.run()
