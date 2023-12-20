from flask import Flask, render_template, request, send_file
import requests
from PIL import Image
from io import BytesIO
import base64

app = Flask(__name__)

def download_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        try:
            image = download_image(url)

            # Convert image to bytes
            img_byte_arr = BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

            # Convert image bytes to base64-encoded string
            img_str = base64.b64encode(img_byte_arr).decode('utf-8')

            return render_template('index.html', image=img_str, error_message=None)

        except Exception as e:
            error_message = f'Error: {e}'
            return render_template('index.html', error_message=error_message)

    return render_template('index.html', error_message=None)

@app.route('/download', methods=['POST'])
def download():
    try:
        if request.method == 'POST':
            # Retrieve the base64-encoded image string from the form data
            img_str = request.form['image']
            
            # Decode the base64 string to bytes
            img_byte_arr = base64.b64decode(img_str)

            return send_file(
                BytesIO(img_byte_arr),
                mimetype='image/png',
                as_attachment=True,
                download_name='downloaded_image.png'
            )
    except Exception as e:
        error_message = f'Error: {e}'
        return render_template('index.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
