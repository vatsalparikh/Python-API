from flask import Flask
from flask import request, jsonify
from scraper import holidays

app = Flask(__name__)

@app.route('/',methods=['GET'])
def home():
    return '''
                <h1>Welcome!</h1>
                <p>Click <a href = '/holidays'>here</a> to get a list of upcoming holidays</p>
            '''

@app.route('/holidays', methods=['GET'])
def upcoming_holidays():
    if 'holidayType' in request.args:
        return jsonify(holidays(request.args['holidayType']))
    else:
        return jsonify(holidays())

app.run(debug=True)