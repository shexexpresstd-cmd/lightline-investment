from flask import Blueprint, render_template

logistics_bp = Blueprint('logistics', __name__,
                         template_folder='../templates/logistics',
                         url_prefix='/logistics')

@logistics_bp.route('/')
def index():
    return render_template('logistics/index.html')

@logistics_bp.route('/about')
def about():
    return render_template('logistics/about.html')

@logistics_bp.route('/services')
def services():
    return render_template('logistics/services.html')

@logistics_bp.route('/contact')
def contact():
    return render_template('logistics/contact.html')
