#!/bin/bash
PRODUCT=$1

# Check if product argument is provided
if [ -z "$PRODUCT" ]; then
    echo "Error: Please provide a product slug as an argument."
    echo "Usage: ./deploy.sh <product-slug>"
    exit 1
fi

# Regenerate static site
python3 app/launchdrop.py products/$PRODUCT.yaml

# Check if generation was successful
if [ $? -ne 0 ]; then
    echo "Error: Failed to generate landing page for $PRODUCT"
    exit 1
fi

# Deploy to Nginx directory
sudo rm -rf /var/www/html/$PRODUCT
sudo mkdir -p /var/www/html/$PRODUCT
sudo cp -r rendered/$PRODUCT/* /var/www/html/$PRODUCT/
sudo chown -R www-data:www-data /var/www/html/$PRODUCT

echo "Deployed $PRODUCT to /var/www/html/$PRODUCT"
