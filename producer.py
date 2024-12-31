import pika
import csv
from flask import Flask, request, jsonify

app = Flask(__name__)

def store_user(email, name):
    # check if the file users.csv exists
    # if it does not exist, create it and write the header
    try:
        with open('users.csv', mode='r') as file:
            pass
    except FileNotFoundError:
        with open('users.csv', mode='w') as file:
            writer = csv.DictWriter(file, fieldnames=['email', 'name'])
            writer.writeheader()
    # write the new user to the file
    with open('users.csv', mode='a') as file:
        writer = csv.DictWriter(file, fieldnames=['email', 'name'])
        writer.writerow({'email': email, 'name': name})

def is_email_registered(email):
    """Check if the email is already in the CSV file."""
    try:
        with open('users.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['email'] == email:
                    return True
    except FileNotFoundError:
        # If the file doesn't exist, no emails are registered
        return False
    return False

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    email = data.get('email')
    name = data.get('name')
    
    if not email or not name:
        return jsonify({"error": "Email and name are required!"}), 400

    # Check if the email is already registered
    if is_email_registered(email):
        return jsonify({"message": f"You're already registered, {name}!"}), 200

    # Store user in CSV
    store_user(email, name)

    # Add user registration details to RabbitMQ queue
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='registration_queue')

    message = {"email": email, "name": name, "type": "registration"}
    channel.basic_publish(exchange='', routing_key='registration_queue', body=str(message))
    connection.close()

    return jsonify({"message": f"User {name} registered successfully!"}), 200


@app.route('/broadcast', methods=['POST'])
def broadcast():
    data = request.json
    body = data.get('body')

    if not body:
        return jsonify({"error": "Email body is required!"}), 400

    # Create a broadcast message
    message = {"body": body}

    # Publish the broadcast message to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='broadcast_queue')

    channel.basic_publish(exchange='', routing_key='broadcast_queue', body=str(message))
    connection.close()

    return jsonify({"message": "Broadcast email queued successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
