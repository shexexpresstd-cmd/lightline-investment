from flask import Blueprint, render_template

engineering_bp = Blueprint('engineering', __name__,
                           template_folder='../templates/engineering',
                           url_prefix='/engineering')

@engineering_bp.route('/')
def index():
    return render_template('engineering/index.html')

@engineering_bp.route('/about')
def about():
    return render_template('engineering/about.html')

@engineering_bp.route('/services')
def services():
    return render_template('engineering/services.html')

@engineering_bp.route('/projects')
def projects():
    return render_template('engineering/projects.html')

@engineering_bp.route('/contact')
def contact():
    return render_template('engineering/contact.html')
