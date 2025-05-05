from flask import Flask, render_template, request, session, url_for
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
import os

app = Flask(__name__)
app.secret_key = 'replace_with_safe_key'

# ✅ Load model once globally
model = load_model('freshness_model.h5')

# ✅ Define class names
class_names = [
    'Fresh Apple', 'Fresh Banana', 'Fresh Orange',
    'Rotten Apple', 'Rotten Banana', 'Rotten Orange'
]

# ✅ Initialize session history
@app.before_request
def init_history():
    if 'history' not in session:
        session['history'] = []

# ✅ Home route
@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = confidence = img_url = None

    if request.method == 'POST' and 'clear' not in request.form:
        f = request.files.get('image')
        if f:
            # ✅ Save uploaded file securely
            filename = secure_filename(f.filename)
            path = os.path.join('static', 'upload.jpg')
            f.save(path)
            img_url = url_for('static', filename='upload.jpg')

            # ✅ Efficient image preprocessing
            img = Image.open(path).resize((224, 224))
            img = np.array(img) / 255.0
            if img.shape[-1] == 4:  # handle transparency
                img = img[..., :3]
            img = img.reshape(1, 224, 224, 3)

            # ✅ Predict
            proba = model.predict(img)[0]
            idx = int(np.argmax(proba))
            prediction = class_names[idx]
            confidence = float(proba[idx]) * 100

            session['history'].insert(0, {
                'label': prediction,
                'confidence': f"{confidence:.1f}%"
            })
            session['history'] = session['history'][:10]

    elif request.method == 'POST' and 'clear' in request.form:
        session['history'] = []

    return render_template(
        'index.html',
        prediction=prediction,
        confidence=confidence,
        history=session['history'],
        img_url=img_url
    )

@app.route('/how-it-works')
def how_it_works():
    return render_template('how_it_works.html')

@app.route('/about')
def about():
    return render_template('about.html')

# ✅ Gunicorn compatibility
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
