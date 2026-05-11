# ForecastIQ
**Predict the Future of Your Business**

ForecastIQ is a next-generation business forecasting and analytics platform for enterprises, startups, retail chains, and e-commerce businesses. Built with a stunning ultra-premium glassmorphic UI, it brings cinematic data visualization and enterprise-grade intelligence into a single dashboard.

## 🚀 Features

- **Advanced ML Forecasting**: Utilizes Random Forest and Scikit-learn to project 30/60/90-day revenue and demand trajectories based on historical patterns.
- **Smart Insight Engine**: Automatically translates complex data into actionable, human-readable insights (e.g., "Demand expected to increase by 18% next month").
- **Inventory Intelligence**: Tracks stock levels, predicts seasonal demand spikes, and automatically triggers low-stock or overstock alerts.
- **Premium Analytics UI**: Interactive animated charts, dynamic KPI cards with trend indicators, and real-time activity feeds.
- **Drag-and-Drop CSV Ingestion**: Train custom models on the fly by uploading historical sales datasets.

## 🛠️ Architecture

Because this environment does not have Node.js installed, ForecastIQ is built on a highly-performant, no-build architecture that delivers an identical cinematic experience:

- **Frontend**: HTML5, Vanilla JavaScript, Tailwind CSS (via CDN), GSAP for animations, Chart.js for data visualization, and Lucide Icons.
- **Backend**: Python, Flask REST API, Pandas for data processing, and Scikit-learn for machine learning.
- **Design System**: Custom CSS with advanced glassmorphism, animated mesh gradients, floating UI elements, and glowing hover states.

## 📦 Installation & Setup

1. **Prerequisites**: Ensure you have Python 3.x installed.
2. **Install Backend Dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. **Run the API Server**:
   ```bash
   python app.py
   ```
   The Flask server will start on `http://localhost:5000`.

4. **Launch the Frontend**:
   Simply open `frontend/index.html` in your web browser. No bundler or build step required! From there, you can navigate to the `dashboard.html`.

## 📸 Screenshots
*(Coming soon)*

## 🛣️ Roadmap
- Implement XGBoost support for more complex multi-variate datasets.
- Add user authentication (JWT) and persistent SQLite database integration.
- Export capabilities for Executive PDF Reports.

## 🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
