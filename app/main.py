import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template

def create_app():
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static',
    )

    from app.routes.services import services_bp
    from app.routes.gallery import gallery_bp
    from app.routes.quotes import quotes_bp
    from app.routes.appointments import appointments_bp

    app.register_blueprint(services_bp)
    app.register_blueprint(gallery_bp)
    app.register_blueprint(quotes_bp)
    app.register_blueprint(appointments_bp)

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
