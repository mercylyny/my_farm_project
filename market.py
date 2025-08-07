from flask import Flask
from flask_cors import CORS
import os

# Import blueprints
from api_routes import api
from web_routes import web


def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for API access

    # Register blueprints
    app.register_blueprint(api)
    app.register_blueprint(web)

    return app


if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')

    app = create_app()

    print("🐓 Poultry Farm Management System Starting...")
    print("=" * 50)
    print("Web Interface: http://localhost:5000")
    print("=" * 50)
    print("API Documentation:")
    print("  📊 Dashboard & Analytics:")
    print("    GET  /api/dashboard")
    print("    GET  /api/financial-summary")
    print()
    print("  👥 Customer Management:")
    print("    GET  /api/customers")
    print("    POST /api/customers")
    print("    GET  /api/customers/{id}")
    print("    GET  /api/customers/{id}/purchases")
    print()
    print("  📦 Input Management:")
    print("    GET  /api/inputs")
    print("    POST /api/inputs")
    print()
    print("  📤 Output Management:")
    print("    GET  /api/outputs")
    print("    POST /api/outputs")
    print("    PUT  /api/outputs/{id}/delivery")
    print()
    print("  💬 Messaging:")
    print("    GET  /api/messages")
    print("    POST /api/messages")
    print("=" * 50)
    print("Required packages: pip install flask flask-cors")
    print("=" * 50)

    app.run(debug=True, host='0.0.0.0', port=5000)
