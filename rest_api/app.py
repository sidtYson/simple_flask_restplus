from flask import Flask, request
from flask_restplus import Api, Resource, fields
from functools import wraps

app = Flask(__name__)

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}
api = Api(app, authorizations=authorizations)

a_language = api.model('Language', {'language': fields.String('The language.')}) #, 'id': fields.Integer('ID')})

languages = []
python = {'language': 'Python', 'id': 1}
languages.append(python)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'X-API-KEY' in request.headers:
            token = request.headers['X-API-KEY']
        
        if not token:
            return {'message': 'Token is missing.'}, 401

        print('TOKEN: {}'.format(token))
        return f(*args, **kwargs)
    
    return decorated

@api.route('/language')
class Language(Resource):
    #@api.marshal_with(a_language, envelope='the_data')
    @api.doc(security='apikey')
    @token_required
    def get(self):
        return languages
    
    @api.expect(a_language)
    def post(self):
        language = api.payload
        language['id'] = len(languages) + 1
        languages.append(language)
        return {'result': 'Language added'}, 201
 
if __name__ == '__main__':
    app.run(port=5000, debug=True)