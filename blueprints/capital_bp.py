from flask import Blueprint, render_template

capital_bp = Blueprint('capital', __name__,
                       template_folder='../templates/capital',
                       url_prefix='/capital')

@capital_bp.route('/')
def index():
    return render_template('capital/index.html')

@capital_bp.route('/about')
def about():
    return render_template('capital/about.html')

@capital_bp.route('/services')
def services():
    return render_template('capital/services.html')

@capital_bp.route('/contact')
def contact():
    return render_template('capital/contact.html')
