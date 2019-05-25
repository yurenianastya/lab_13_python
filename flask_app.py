from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,
                                                                    'dbsqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
database = SQLAlchemy(app)
# Init ma
marshmallow = Marshmallow(app)


# Event Class/Model
class ConcertHallEvent(database.Model):

    id = database.Column(database.Integer, primary_key=True)
    event_name = database.Column(database.String(100), unique=True)
    musicians_count = database.Column(database.Integer)
    event_duration = database.Column(database.Integer)
    ticket_price = database.Column(database.Integer)

    def __init__(self, event_name, musicians_count,
                 event_duration, ticket_price):
        self.event_name = event_name
        self.musicians_count = musicians_count
        self.event_duration = event_duration
        self.ticket_price = ticket_price


# Product Schema
class EventSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 'event_name', 'musicians_count', 'event_duration',
                  'ticket_price')


# Init schema
event_schema = EventSchema(strict=True)
events_schema = EventSchema(many=True, strict=True)


# handling default page
@app.route('/')
def greetings():
    return jsonify({'msg': 'Welcome to nsty app. Hey, add a slash event in '
                    'route (/event).'})

# Create a event
@app.route('/event', methods=['POST'])
def add_event():
    event_name = request.json['event_name']
    musicians_count = request.json['musicians_count']
    event_duration = request.json['event_duration']
    ticket_price = request.json['ticket_price']

    new_event = ConcertHallEvent(event_name, musicians_count, event_duration,
                                 ticket_price)

    database.session.add(new_event)
    database.session.commit()

    return event_schema.jsonify(new_event)


# Get all events
@app.route('/event', methods=['GET'])
def get_all_events():
    all_events = ConcertHallEvent.query.all()
    result = events_schema.dump(all_events)
    return jsonify(result.data)

# Get one event
@app.route('/event/<id>', methods=['GET'])
def get_event(id):
    event = ConcertHallEvent.query.get(id)
    return event_schema.jsonify(event)

# Uodate a event
@app.route('/event/<id>', methods=['PUT'])
def update_event(id):
    event = ConcertHallEvent.query.get(id)

    event_name = request.json["event_name"]
    musicians_count = request.json["musicians_count"]
    event_duration = request.json["event_duration"]
    ticket_price = request.json["ticket_price"]

    event.name = event_name
    event.musicians_count = musicians_count
    event.event_duration = event_duration
    event.ticket_price = ticket_price

    database.session.commit()

    return event_schema.jsonify(event)

# Delete event
@app.route('/event/<id>', methods=['DELETE'])
def delete_event(id):
    event = ConcertHallEvent.query.get(id)
    database.session.delete(event)
    database.session.commit()
    return event_schema.jsonify(event)


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
