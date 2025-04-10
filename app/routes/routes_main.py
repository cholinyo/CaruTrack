# filepath: c:\Users\vcaruncho\Downloads\CaruTrack\app\routes\routes_main.py
from flask import Blueprint, render_template

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')