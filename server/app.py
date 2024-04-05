from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    all_message = Message.query.all()

    if all_message:
        if request.method == 'GET':
            message_list_dict = [message.to_dict() for message in all_message]
            return make_response(message_list_dict, 200)
        
        elif request.method == 'POST':
            new_messages = Message(body=request.json.get('body'), username=request.json.get('username'))
            db.session.add(new_messages)
            db.session.commit()

            body = new_messages.to_dict()
            return make_response(body, 201)
    

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    messages_id = db.session.get(Message, id)

    if messages_id:
        if request.method == 'PATCH':
            for attr in request.json:
                setattr(messages_id, attr, request.json[attr])
            db.session.commit()

            body = messages_id.to_dict()
            status = 200
            return make_response(body, status)
        
        elif request.method == 'DELETE':
            db.session.delete(messages_id)
            db.session.commit()
            

if __name__ == '__main__':
    app.run(port=5555)
