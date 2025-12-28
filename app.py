from flask import Flask, render_template, request
import pickle
import numpy as np   # ✅ IMPORTANT

app = Flask(__name__)

# Load model and encoders
model = pickle.load(open("real_estate_model.pkl", "rb"))
area_le = pickle.load(open("area_encoder.pkl", "rb"))
type_le = pickle.load(open("type_encoder.pkl", "rb"))

def format_price(price):
    return "{:,.0f}".format(price)

@app.route("/", methods=["GET", "POST"])
def home():
    price = None
    error = None
    warning = None

    areas = sorted(area_le.classes_.tolist())
    property_types = sorted(type_le.classes_.tolist())

    if request.method == "POST":
        try:
            year = int(request.form["year"])
            area = request.form["area"]
            property_type = request.form["property_type"]
            size = float(request.form["size"])

            if year > 2025:
                warning = "Prediction for future year is an estimate based on historical trends"

            area_encoded = area_le.transform([area])[0]
            type_encoded = type_le.transform([property_type])[0]

            # 🔹 MODEL PREDICTS LOG PRICE
            log_price = model.predict(
                [[year, area_encoded, type_encoded, size]]
            )[0]

            # 🔹 CONVERT BACK TO ACTUAL PRICE
            actual_price = np.expm1(log_price)

            price = format_price(actual_price)

        except Exception as e:
            error = "Please select valid inputs"

    return render_template(
        "index.html",
        price=price,
        error=error,
        warning=warning,
        areas=areas,
        property_types=property_types
    )

if __name__ == "__main__":
    app.run(debug=True)
