#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, jsonify
from fuzzywuzzy import fuzz, process
import logging
from logging import Formatter, FileHandler
import os
import spell

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#
source = open('dict.txt', 'rt')
choices = []
for row in source:
    choices.append(str(row[:-1]))

@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')



@app.route('/api/v1/correction', methods=['GET'])
def correctSpell():
    results = []
    if 'query' in request.args:
        query = request.args['query']
    else:
        res = {
            "results": results
        }
        return jsonify(res)

    item = spell.correction(query)
    if item=='':
        results.append({
            "id": 0,
            "text":'',
        })
    else:
        results.append({
                    "id": 0,
                    "text":'Did you mean: ' + str(item) + '?',
                })
    res = {
        "results": results
    }
    return jsonify(res)



# Error handlers.

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
