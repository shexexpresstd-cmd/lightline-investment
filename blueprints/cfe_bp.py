from flask import Blueprint, render_template

cfe_bp = Blueprint('cfe', __name__,
                   template_folder='../templates/cfe',
                   url_prefix='/cfe')

@cfe_bp.route('/')
def index():
    return render_template('cfe/index.html')

@cfe_bp.route('/about')
def about():
    return render_template('cfe/about.html')

@cfe_bp.route('/programs')
def programs():
    return render_template('cfe/programs.html')

@cfe_bp.route('/contact')
def contact():
    return render_template('cfe/contact.html')
