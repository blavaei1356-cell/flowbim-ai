from flask import Flask, jsonify, request

app = Flask(__name__)

@app.get("/")
def home():
    return jsonify({
        "status": "ok",
        "service": "FlowBIM AI test server"
    })

@app.post("/calculate")
def calculate():
    data = request.get_json(silent=True) or {}

    try:
        area = float(data.get("area", 0))
    except (TypeError, ValueError):
        return jsonify({"status": "error", "message": "area must be a number"}), 400

    factors = {
        "اداری": 200,
        "مسکونی": 150,
        "تجاری": 250,
        "درمانی": 300
    }

    usage = data.get("usage", "اداری")
    factor = factors.get(usage, 200)
    cooling_load_kw = round(area * factor / 1000, 2)

    return jsonify({
        "status": "success",
        "area_m2": area,
        "usage": usage,
        "cooling_load_kw": cooling_load_kw,
        "note": "Preliminary estimate only"
    })
