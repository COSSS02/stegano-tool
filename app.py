from flask import Flask, render_template, request, send_file
from stegano import encode_string, decode_string
from os import path

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/encode')
def encode():
    if path.exists('static/encoded.png'):
        image = 'static/encoded.png'
    else:
        image = None

    return render_template('encode.html', encoded_image=image)


@app.route('/decode')
def decode():
    if path.exists('static/upload_decode.png'):
        image = 'static/upload_decode.png'
    else:
        image = None

    if path.exists('static/decoded.txt'):
        file = open('static/decoded.txt', 'r')
        message = file.read()
        file.close()
    else:
        message = None

    return render_template('decode.html', decoded_image=image,
                           decoded_text=message)


@app.route('/image/encode', methods=['POST'])
def encode_image():
    image = request.files['file']
    message = request.form['message']
    image.save('static/upload_encode.png')

    encode_string(image, message, 'static/encoded.png')

    return send_file('static/encoded.png', mimetype='image/png')


@app.route('/image/decode', methods=['POST'])
def decode_image():
    image = request.files['file']
    image.save('static/upload_decode.png')

    decode_string(image, 'static/decoded.txt')

    file = open('static/decoded.txt', 'r')
    message = file.read()
    file.close()
    return message


@app.route('/image/last/encoded')
def display_encoded():
    if path.exists('static/encoded.png'):
        return send_file('static/encoded.png', mimetype='image/png')
    else:
        return 'No image was uploaded to encode'


@app.route('/image/last/decoded')
def display_decoded():
    if path.exists('static/decoded.txt'):
        file = open('static/decoded.txt', 'r')
        message = file.read()
        file.close()
        return message
    else:
        return 'No image was decoded yet'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
