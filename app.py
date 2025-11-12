from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

@app.route("/events", methods=["POST"])
def create_event():

    # Extract JSON data from the request body
    data = request.get_json()

    # Validate presence of required "title" field
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    # Generate a new unique ID based on the existing events
    new_id = max((event.id for event in events), default=0) + 1

    # Create new Event instance
    new_event = Event(new_id, data["title"])

    # Add to the in-memory list
    events.append(new_event)

    # Return the created event with 201 Created
    return jsonify(new_event.to_dict()), 201

@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
  
    # Extract JSON data
    data = request.get_json()

    # Validate input
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    # Search for event to update
    for event in events:
        if event.id == event_id:
            event.title = data["title"]  # Update the title
            return jsonify(event.to_dict()), 200

    # If event not found
    return jsonify({"error": "Event not found"}), 404

@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):

    # Search for event by index
    for index, event in enumerate(events):
        if event.id == event_id:
            events.pop(index)  # Remove from list
            return "", 204  # No content response

    # If no event matched the ID
    return jsonify({"error": "Event not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
