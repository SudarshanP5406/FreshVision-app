from flask import Flask, render_template, request, session, redirect, url_for
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os

app = Flask(__name__)
app.secret_key = 'replace_with_safe_key'
model = load_model('freshness_model.keras')
class_names = ['Fresh Apple', 'Fresh Banana', 'Fresh Orange', 'Rotten Apple', 'Rotten Banana', 'Rotten Orange']

@app.before_request
def init_history():
    if 'history' not in session:
        session['history'] = []

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = confidence = img_url = None
    if request.method == 'POST' and 'clear' not in request.form:
        f = request.files.get('image')
        if f:
            path = os.path.join('static','upload.jpg')
            f.save(path)
            img_url = url_for('static', filename='upload.jpg')
            img = load_img(path, target_size=(224,224))
            img = img_to_array(img)/255.0
            img = np.expand_dims(img,0)
            proba = model.predict(img)[0]
            idx = np.argmax(proba)
            prediction = class_names[idx]
            confidence = proba[idx]*100
            session['history'].insert(0, {'label':prediction, 'confidence':f"{confidence:.1f}%"})
            session['history'] = session['history'][:10]
    # Clear history
    if request.method == 'POST' and 'clear' in request.form:
        session['history'] = []
    return render_template('index.html', prediction=prediction, confidence=confidence, history=session['history'], img_url=img_url)

@app.route('/how-it-works')
def how_it_works():
    return render_template('how_it_works.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

