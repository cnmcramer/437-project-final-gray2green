"""
Gray to Green Landscaping — Flask App Entry Point
app/main.py
"""

from flask import Flask, send_from_directory
import os

def create_app():
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static',
    )

    # ── Register route blueprints ──────────────────────────────────────
    from app.routes.services import services_bp
    from app.routes.gallery import gallery_bp
    from app.routes.quotes import quotes_bp
    from app.routes.appointments import appointments_bp

    app.register_blueprint(services_bp)
    app.register_blueprint(gallery_bp)
    app.register_blueprint(quotes_bp)
    app.register_blueprint(appointments_bp)

    # ── Serve HTML pages ───────────────────────────────────────────────
    from flask import render_template

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/services')
    def services_page():
        return render_template('services.html')

    @app.route('/gallery')
    def gallery_page():
        return render_template('gallery.html')

    @app.route('/quote')
    def quote_page():
        return render_template('quote.html')

    @app.route('/contact')
    def contact_page():
        return render_template('contact.html')

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
