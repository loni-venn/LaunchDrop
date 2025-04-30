#!/usr/bin/env python3
"""
LaunchDrop - Static landing page generator

This script generates static HTML landing pages from YAML configuration files.
It uses Jinja2 for templating and copies assets to the output directory.
"""

import os
import sys
import shutil
import argparse
import logging
import yaml
from jinja2 import Environment, FileSystemLoader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('launchdrop')

# Define script directory and related paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(SCRIPT_DIR, 'template.html.j2')
ASSETS_DIR = os.path.join(SCRIPT_DIR, 'assets')
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'rendered')


def load_yaml_config(yaml_path):
    """
    Load YAML configuration file
    
    Args:
        yaml_path (str): Path to the YAML file
        
    Returns:
        dict: Parsed YAML data
    """
    try:
        with open(yaml_path, 'r') as file:
            config = yaml.safe_load(file)
            logger.info(f"Loaded YAML config from {yaml_path}")
            return config
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML: {e}")
        sys.exit(1)
    except FileNotFoundError:
        logger.error(f"File not found: {yaml_path}")
        sys.exit(1)


def validate_config(config):
    """
    Validate the configuration to ensure required fields are present
    
    Args:
        config (dict): Parsed YAML configuration
        
    Returns:
        bool: True if valid, False otherwise
    """
    required_fields = [
        'product_slug', 'product_title', 'heading', 
        'subheading', 'price', 'stripe_link',
        'author_name', 'year', 'contact_email'
    ]
    
    for field in required_fields:
        if field not in config:
            logger.error(f"Missing required field in YAML config: {field}")
            return False
    
    return True


def render_template(config):
    """
    Render the Jinja2 template with the provided configuration
    
    Args:
        config (dict): Parsed YAML configuration
        
    Returns:
        str: Rendered HTML content
    """
    try:
        # Set up Jinja2 environment
        env = Environment(loader=FileSystemLoader(SCRIPT_DIR))
        template = env.get_template(os.path.basename(TEMPLATE_PATH))
        
        # Render the template with the configuration
        html_content = template.render(**config)
        logger.info("Template rendered successfully")
        return html_content
    except Exception as e:
        logger.error(f"Error rendering template: {e}")
        sys.exit(1)


def copy_assets(config, output_folder):
    """
    Copy assets referenced in the configuration to the output folder
    
    Args:
        config (dict): Parsed YAML configuration
        output_folder (str): Path to the output folder
    """
    if 'product_image' in config and config['product_image']:
        image_path = os.path.join(ASSETS_DIR, config['product_image'])
        if os.path.exists(image_path):
            dest_path = os.path.join(output_folder, config['product_image'])
            try:
                shutil.copy2(image_path, dest_path)
                logger.info(f"Copied image to {dest_path}")
            except Exception as e:
                logger.error(f"Error copying image: {e}")
        else:
            logger.warning(f"Image not found: {image_path}")


def save_html(html_content, output_path):
    """
    Save HTML content to the specified output path
    
    Args:
        html_content (str): Rendered HTML content
        output_path (str): Path to save the HTML file
    """
    try:
        with open(output_path, 'w') as file:
            file.write(html_content)
        logger.info(f"HTML saved to {output_path}")
    except Exception as e:
        logger.error(f"Error saving HTML: {e}")
        sys.exit(1)


def generate_landing_page(yaml_path):
    """
    Generate a landing page from a YAML configuration file
    
    Args:
        yaml_path (str): Path to the YAML file
    """
    # Load and validate configuration
    config = load_yaml_config(yaml_path)
    if not validate_config(config):
        logger.error("Invalid configuration")
        sys.exit(1)
    
    # Create output directory
    product_slug = config['product_slug']
    output_folder = os.path.join(OUTPUT_DIR, product_slug)
    os.makedirs(output_folder, exist_ok=True)
    
    # Render template and save HTML
    html_content = render_template(config)
    save_html(html_content, os.path.join(output_folder, 'index.html'))
    
    # Copy assets
    copy_assets(config, output_folder)
    
    logger.info(f"Landing page generated successfully for {product_slug}")
    return output_folder


def main():
    """Main entry point for the script"""
    parser = argparse.ArgumentParser(description='Generate static landing pages from YAML configs')
    parser.add_argument('yaml_path', help='Path to the YAML configuration file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Generate landing page
    output_folder = generate_landing_page(args.yaml_path)
    print(f"Landing page generated successfully at: {output_folder}")


if __name__ == "__main__":
    main()
