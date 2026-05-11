import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from datetime import timedelta
import io

# Initialize Flask with static folder pointing to the frontend directory
app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Serve the main index.html
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Serve other static files (dashboard.html, etc.)
@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

# Dummy simple model setup for the endpoints
# For a real app, you would load a trained model and handle actual feature engineering

def generate_dummy_forecast(days=30):
    """Generate dummy forecast data to mimic ML output."""
    dates = pd.date_range(start=pd.Timestamp.today(), periods=days).strftime('%Y-%m-%d').tolist()
    # Simple random walk for dummy data
    base_value = 10000
    values = []
    for _ in range(days):
        base_value += np.random.normal(500, 1500)
        values.append(max(0, round(base_value, 2)))
        
    return {"dates": dates, "predictions": values}

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({"status": "ForecastIQ API is running."}), 200

@app.route('/api/forecast', methods=['POST'])
def get_forecast():
    """Returns a forecast based on the specified timeframe."""
    data = request.json or {}
    days = data.get('days', 30)
    
    forecast_data = generate_dummy_forecast(days=days)
    
    return jsonify({
        "status": "success",
        "data": forecast_data,
        "metrics": {
            "accuracy": "92.4%",
            "rmse": 450.2,
            "mae": 320.1
        }
    }), 200

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handles CSV data uploads."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if file and file.filename.endswith('.csv'):
        try:
            # Read CSV to validate
            df = pd.read_csv(file)
            rows = len(df)
            columns = df.columns.tolist()
            
            return jsonify({
                "status": "success",
                "message": f"Successfully uploaded and parsed CSV with {rows} rows.",
                "columns": columns,
                "preview": df.head(5).to_dict(orient='records')
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
            
    return jsonify({"error": "Invalid file format. Please upload a CSV."}), 400

@app.route('/api/insights', methods=['GET'])
def get_insights():
    """Returns dynamic business insights."""
    insights = [
        {"id": 1, "type": "positive", "text": "Demand expected to increase by 18% next month in the West region.", "category": "Demand"},
        {"id": 2, "type": "warning", "text": "Inventory shortage risk detected for 'Wireless Earbuds' in Q3.", "category": "Inventory"},
        {"id": 3, "type": "neutral", "text": "Electronics category driving highest growth (up 22% YoY).", "category": "Sales"},
        {"id": 4, "type": "positive", "text": "Customer retention improved by 4.2% after recent promotional campaign.", "category": "Customers"}
    ]
    return jsonify({"status": "success", "data": insights}), 200

@app.route('/api/kpi', methods=['GET'])
def get_kpi():
    """Returns main KPI metrics."""
    kpi_data = {
        "total_revenue": {"value": "$2.4M", "trend": "+12.5%", "status": "up"},
        "forecasted_revenue": {"value": "$2.8M", "trend": "+16.2%", "status": "up"},
        "demand_index": {"value": "84/100", "trend": "+5.1%", "status": "up"},
        "inventory_health": {"value": "92%", "trend": "-2.0%", "status": "down"},
        "active_stores": {"value": "124", "trend": "+4", "status": "up"},
        "profit_margin": {"value": "32.4%", "trend": "+1.2%", "status": "up"}
    }
    return jsonify({"status": "success", "data": kpi_data}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

