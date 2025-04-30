#!/bin/bash
# LaunchDrop - Deployment Script
# Deploys a rendered landing page to a Linode server

# Environment variables (modify these or set them in your shell)
REMOTE_HOST=${REMOTE_HOST:-"your-linode-ip"}
REMOTE_USER=${REMOTE_USER:-"root"}
KEY_PATH=${KEY_PATH:-"~/.ssh/id_rsa"}

# Usage information
function show_usage() {
    echo "LaunchDrop Deployment Script"
    echo ""
    echo "Usage: $0 <product_slug>"
    echo ""
    echo "Arguments:"
    echo "  product_slug    The slug of the product to deploy"
    echo ""
    echo "Environment Variables:"
    echo "  REMOTE_HOST     The hostname or IP of your Linode server"
    echo "  REMOTE_USER     The SSH username for your Linode server"
    echo "  KEY_PATH        Path to the SSH private key for authentication"
    echo ""
    echo "Example:"
    echo "  REMOTE_HOST=123.456.789.0 REMOTE_USER=admin KEY_PATH=~/.ssh/linode $0 3daybucket"
}

# Error handling
function handle_error() {
    echo "ERROR: $1"
    exit 1
}

# Check if product slug is provided
if [ -z "$1" ]; then
    show_usage
    handle_error "Product slug is required"
fi

PRODUCT_SLUG="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="${SCRIPT_DIR}/rendered/${PRODUCT_SLUG}"
REMOTE_DIR="/var/www/html/${PRODUCT_SLUG}"

# Validate source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    handle_error "Source directory does not exist: $SOURCE_DIR. Run launchdrop.py first."
fi

# Validate source directory has content
if [ ! -f "${SOURCE_DIR}/index.html" ]; then
    handle_error "index.html not found in source directory. Make sure launchdrop.py generated the files."
fi

echo "Deploying ${PRODUCT_SLUG} to ${REMOTE_HOST}..."

# Create remote directory (ignore error if it already exists)
ssh -i "$KEY_PATH" "${REMOTE_USER}@${REMOTE_HOST}" "mkdir -p ${REMOTE_DIR}" || \
    handle_error "Failed to create remote directory"

# Deploy files using rsync
rsync -avz --delete -e "ssh -i ${KEY_PATH}" "${SOURCE_DIR}/" "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}" || \
    handle_error "Rsync failed"

echo "Deployment successful!"
echo "Your landing page is now available at: http://${REMOTE_HOST}/${PRODUCT_SLUG}/"

exit 0
