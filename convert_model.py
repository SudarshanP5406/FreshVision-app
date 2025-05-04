from tensorflow.keras.models import load_model

# Load the existing Keras SavedModel
model = load_model('freshness_model.keras')

# Re-save it in HDF5 format
model.save('freshness_model.h5')
print("Conversion complete: freshness_model.h5 created")
