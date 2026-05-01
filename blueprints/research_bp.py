from flask import Blueprint, render_template

research_bp = Blueprint('research', __name__,
                        template_folder='../templates/research',
                        url_prefix='/research')

@research_bp.route('/')
def index():
    return render_template('research/index.html')

@research_bp.route('/about')
def about():
    return render_template('research/about.html')

@research_bp.route('/insights')
def insights():
    return render_template('research/insights.html')

@research_bp.route('/contact')
def contact():
    return render_template('research/contact.html')
