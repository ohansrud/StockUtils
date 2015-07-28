from flask import render_template, make_response
from FlaskWebProject1 import app

# routing for basic pages (pass routing onto the Angular app)
@app.route('/')
@app.route('/scan/')
@app.route('/chart/')
@app.route('/chart/<ticker>')
def basic_pages(**kwargs):
    return render_template('index.html')

# routing for templates (pass routing onto the Angular app)
@app.route('/templates/<template_name>', methods=['GET'])
def get_template(template_name):
  return render_template('partials/{}'.format(template_name))