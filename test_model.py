from tensorflow.keras.models import load_model
model = load_model('freshness_model.keras')
print("Loaded model OK:", model)
