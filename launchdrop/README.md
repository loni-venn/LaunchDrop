# LaunchDrop 🚀

LaunchDrop is a static site generator that creates Stripe-enabled landing pages from simple YAML configuration files. Perfect for quickly launching products with minimal setup.

## 📦 Features

- Generate complete landing pages from YAML config files
- Stripe payment integration ready
- Fully static HTML output (no server-side code needed)
- Simple deployment to any web server
- Customizable templates with Jinja2
- Minimal dependencies (just Python, Jinja2, and PyYAML)

## 🔧 Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/launchdrop.git
   cd launchdrop
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## 🔨 Usage

### 1. Create a product config

Create a YAML file in the `products/` directory with your product details:

```yaml
product_slug: "yourproduct"
product_title: "Your Amazing Product"
heading: "Main Headline Goes Here"
subheading: "Compelling subheadline to engage visitors"
price: "$49"
stripe_link: "https://buy.stripe.com/your-product-link"
pitch_paragraph_1: "First paragraph of your pitch..."
pitch_paragraph_2: "Second paragraph with more details..."
features:
  - "Feature one description"
  - "Another great feature"
  - "One more reason to buy"
product_image: "yourimage.jpg"  # Place this in the assets/ folder
author_name: "Your Name"
year: "2023"
contact_email: "you@example.com"
