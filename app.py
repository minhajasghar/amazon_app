from flask import Flask, render_template, request
import numpy as np
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os

app = Flask(__name__, static_folder="static", template_folder="templates")

# Load tokenizer, encoder, and model
try:
    tokenizer = pickle.load(open("model/tokenizer.pkl", "rb"))
    encoder = pickle.load(open("model/label_encoder.pkl", "rb"))
    model = load_model("model/sentiment_ensemble_model.h5")
except Exception as e:
    print("Model or tokenizer load error:", e)
    tokenizer, encoder, model = None, None, None

MAX_LEN = 200

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        review = request.form.get("review", "")
        if not review.strip() or not model:
            return render_template("index.html", review=review, label="Error", confidence=0)

        sequence = tokenizer.texts_to_sequences([review])
        padded_seq = pad_sequences(sequence, maxlen=MAX_LEN)

        pred = model.predict(padded_seq)
        predicted_class = np.argmax(pred)
        label = encoder.inverse_transform([predicted_class])[0]
        confidence = round(np.max(pred) * 100, 2)

        return render_template("index.html", review=review, label=label, confidence=confidence)

    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
