from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.all()
        messages_list = []
        for message in messages:
            message_dict = {
                "id": message.id,
                "body": message.body,
                "username": message.username,
                "created_at": message.created_at,
                "updated_at": message.updated_at,
            }
            messages_list.append(message_dict)

        response = make_response(
            jsonify(messages_list),
            200
        )
        return response

    elif request.method == 'POST':
        new_message = Message(
            body=request.form.get("body"),
            username=request.form.get("username"),
            
        )

        db.session.add(new_message)
        db.session.commit()

        message_dict = new_message.to_dict()

        response = make_response(
            jsonify(message_dict),
            201
        )

        return response




@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.get_or_404(id)

    if request.method == 'GET':
        message_dict = {
            "id":message.id,
            "body": message.body,
            "username": message.username,
            "created_at": message.created_at,
            "updated_at": message.updated_at,
        }
        response = make_response(
            jsonify(message_dict),
            200
        )
        return response

    elif request.method == 'PATCH':
        data = request.get_json()
        if 'body' in data:
            message.body = data['body']
            message.updated_at = datetime.utcnow()
            db.session.commit()

            updated_message_dict = {
                "body": message.body,
                "username": message.username,
                "created_at": message.created_at,
                "updated_at": message.updated_at,
            }
            response = make_response(
                jsonify(updated_message_dict),
                200
            )
            return response

    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        response = make_response(
            jsonify({"delete_successful": True, "message": "Message deleted."}),
            200
        )
        return response

if __name__ == '__main__':
    app.run(port=5555)
