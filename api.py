from flask import (Flask, request, send_from_directory, redirect, url_for,
                   render_template, abort)

import interestingizer
from PIL import Image
from StringIO import StringIO
import requests

import json
import md5
import random
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16Mb upload file limit

TMP_DIR = "./tmp"
ANIMALS = ["cow", "cat"]
ITEMS_BASES = dict([(a, os.path.join("./images/", a)) for a in ANIMALS])
items = dict([(a, [Image.open(os.path.join(bp, filename)).convert("RGBA")
                                 for filename in os.listdir(bp)])
                                 for a, bp in ITEMS_BASES.iteritems()])


@app.route("/ping")
def ping():
    return "OK"


def cache_image(pil_img):
    key = md5.md5(pil_img.tostring()).hexdigest()
    with open(os.path.join(TMP_DIR, key), "w+") as fd:
        pil_img.save(fd, 'JPEG', quality=70)
    return key


@app.route("/cache/<key>")
def cache(key):
    return send_from_directory(TMP_DIR, key, mimetype='image/jpeg')


@app.route("/test")
def index():
    return render_template("index.html")


@app.route("/interestingize", methods=["POST", "GET"])
@app.route("/interestingize/<animal>", methods=["POST", "GET"])
def interestingize(animal="cow"):
    if animal not in ANIMALS:
        abort(404)
    if request.method == "POST":
        image_raw = request.files.get("image")
        if image_raw is None:
            return "Must provide image in form field 'image'", 500

        try:
            image = Image.open(image_raw)
        except IOError:
            return "Could not decode image", 500

    else:
        url = request.values.get("src", None)
        if url is None:
            return redirect(url_for("index"))

        r = requests.get(url)
        if r.status_code != requests.codes.ok:
            r.raise_for_status()

        try:
            image = Image.open(StringIO(r.content))
        except IOError:
            return "Could not decode image", 500

    item = random.choice(items[animal]).copy()
    try:
        better_image = interestingizer.interestingize(image, item)
    except Exception, e:
        print "Could not run interestingize algorithm: %s" % e
        return "Could not interestingize", 500

    key = cache_image(better_image)

    new_url = url_for('cache', key=key)
    if request.method == "POST":
        return json.dumps(new_url)

    return redirect(new_url)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
