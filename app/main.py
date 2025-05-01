from flask import Flask, render_template, redirect, url_for, request, send_from_directory
import os
import yaml
import json
from werkzeug.utils import secure_filename
import subprocess
import logging

"""
LaunchDrop - Main application entry point

This Flask application serves as the web interface for the LaunchDrop system.
It allows users to manage product configurations, generate landing pages,
and preview the generated content.
"""

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('launchdrop-web')

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRODUCTS_DIR = os.path.join(BASE_DIR, 'products')
RENDERED_DIR = os.path.join(BASE_DIR, 'rendered')
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

# Ensure directories exist
os.makedirs(PRODUCTS_DIR, exist_ok=True)
os.makedirs(RENDERED_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)

def get_product_list():
    """Get a list of available product configurations"""
    products = []
    if os.path.exists(PRODUCTS_DIR):
        for filename in os.listdir(PRODUCTS_DIR):
            if filename.endswith('.yaml'):
                file_path = os.path.join(PRODUCTS_DIR, filename)
                with open(file_path, 'r') as file:
                    try:
                        config = yaml.safe_load(file)
                        product_slug = config.get('product_slug', 'unknown')
                        product_title = config.get('product_title', 'Untitled')
                        is_rendered = os.path.exists(os.path.join(RENDERED_DIR, product_slug))
                        products.append({
                            'slug': product_slug,
                            'title': product_title,
                            'config_file': filename,
                            'is_rendered': is_rendered
                        })
                    except yaml.YAMLError:
                        logger.error(f"Error parsing YAML file: {filename}")
    return products

def generate_landing_page(yaml_path):
    """Run the launchdrop.py script to generate a landing page"""
    try:
        cmd = ['python', os.path.join(os.path.dirname(__file__), 'launchdrop.py'), yaml_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        logger.info(f"Generation output: {result.stdout}")
        if result.returncode != 0:
            logger.error(f"Generation error: {result.stderr}")
            return False, result.stderr
        return True, result.stdout
    except Exception as e:
        logger.error(f"Error running generation script: {e}")
        return False, str(e)

@app.route('/')
def index():
    """Main dashboard page"""
    products = get_product_list()
    return render_template('index.html', products=products)

@app.route('/view/<product_slug>')
def view_product(product_slug):
    """View rendered landing page"""
    product_path = os.path.join(RENDERED_DIR, product_slug)
    if not os.path.exists(product_path):
        return render_template('error.html', message=f"Product '{product_slug}' has not been rendered yet.")
    return send_from_directory(product_path, 'index.html')

@app.route('/generate/<product_slug>')
def generate_product(product_slug):
    """Generate a landing page from a product configuration"""
    products = get_product_list()
    product = next((p for p in products if p['slug'] == product_slug), None)
    
    if not product:
        return render_template('error.html', message=f"Product '{product_slug}' not found.")
    
    yaml_path = os.path.join(PRODUCTS_DIR, product['config_file'])
    success, message = generate_landing_page(yaml_path)
    
    if success:
        return redirect(url_for('view_product', product_slug=product_slug))
    else:
        return render_template('error.html', message=f"Error generating product: {message}")

@app.route('/products')
def list_products():
    """List all product configurations"""
    products = get_product_list()
    return render_template('products.html', products=products)

@app.route('/assets/<filename>')
def serve_asset(filename):
    """Serve assets from the assets directory"""
    return send_from_directory(ASSETS_DIR, filename)

@app.route('/rendered/<product_slug>/<filename>')
def serve_rendered_file(product_slug, filename):
    """Serve files from the rendered product directories"""
    product_path = os.path.join(RENDERED_DIR, product_slug)
    return send_from_directory(product_path, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
