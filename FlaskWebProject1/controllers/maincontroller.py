from flask import render_template, make_response
from FlaskWebProject1 import app


# routing for basic pages (pass routing onto the Angular app)
@app.route('/')
@app.route('/about/')
@app.route('/chart/')
def basic_pages(**kwargs):
    return make_response(open('FlaskWebProject1/templates/index.html').read())

# routing for templates (pass routing onto the Angular app)
@app.route('/templates/<template_name>', methods=['GET'])
def get_template(template_name):
  return render_template('partials/{}'.format(template_name))

#@app.route('/<model_name>/')
#@app.route('/<model_name>/<item_id>')
#def rest_pages(model_name, item_id=None):
#    return make_response(open('FlaskWebProject1/templates/index.html').read())

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



#@app.route('/')
#@app.route('/ticker')
#@app.route('/ticker/')
#def index():
#  return render_template("nglayout.html")


#@app.route('/templates/<template_name>', methods=['GET'])
#def get_template(template_name):
#  return render_template('partials/{}'.format(template_name))



#@app.route('/', defaults={'path': ''})
#@app.route('/<path:path>')
#def home(path):
#    """Renders the about page."""
#    return render_template(
#        'nglayout.html'
#    )
    #return app.send_static_file('FlaskWebProject1/templates/nglayout.html')

