import os
import hmac
from flask import Flask, jsonify, request

app = Flask(__name__)

API_SECRET = os.environ.get("FLOWBIM_API_SECRET", "")

def is_authorized(request):
    provided_secret = request.headers.get("X-FlowBIM-Key", "")
    return bool(API_SECRET) and hmac.compare_digest(provided_secret, API_SECRET)

@app.get("/")
def home():
    return jsonify({
        "status": "ok",
        "service": "FlowBIM AI test server",
        "message": "Python API is running."
    })

@app.post("/calculate")
def calculate():
    if not is_authorized(request):
        return jsonify({
            "status": "error",
            "message": "Unauthorized"
        }), 401

    data = request.get_json(silent=True) or {}

    try:
        area = float(data.get("area", 0))
    except (TypeError, ValueError):
        return jsonify({
            "status": "error",
            "message": "area must be a number"
        }), 400

    if area <= 0:
        return jsonify({
            "status": "error",
            "message": "area must be greater than zero"
        }), 400

    factors = {
        "اداری": 200,
        "مسکونی": 150,
        "تجاری": 250,
        "درمانی": 300
    }

    usage = str(data.get("usage", "اداری")).strip()
    factor = factors.get(usage, 200)
    cooling_load_kw = round((area * factor) / 1000, 2)

    return jsonify({
        "status": "success",
        "area_m2": area,
        "usage": usage,
        "factor_w_m2": factor,
        "cooling_load_kw": cooling_load_kw,
        "note": "Preliminary estimate only; not a final engineering calculation."
    })
