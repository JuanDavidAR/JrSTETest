from flask import Flask, request, jsonify
from config import Config
from models import db, Greeting

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the database
    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/hello', methods=['POST'])
    def hello():
        if request.is_json:
            json_data = request.get_json()
            if 'name' in json_data:
                name = json_data['name']

                try:
                    # Create a new entry in the database
                    new_greeting = Greeting(name=name)
                    db.session.add(new_greeting)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    return jsonify({'error': str(e)}), 500

                response = {
                    'message': f'Hello, {name}!'
                }
                return jsonify(response), 200
            else:
                return jsonify({'error': 'Missing name field in JSON'}), 400
        else:
            return jsonify({'error': 'Invalid JSON'}), 400

    @app.route('/list', methods=['POST'])
    def list_greetings():
        try:
            # Retrieve all records from the Greeting table
            greetings = Greeting.query.all()
            # Format the data as a list of dictionaries
            greetings_list = [
                {'name': g.name, 'timestamp': g.timestamp} for g in greetings]
            return jsonify(greetings_list), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=8080)
