import pika
import csv
import json
import smtplib

def send_email(email, subject, body):
    """Send an email using smtplib."""
    try:
        # Load credentials from the JSON file
        with open('credentials.json', 'r') as file:
            credentials = json.load(file)

        # SMTP configuration
        sender_email = credentials.get('sender_email')
        sender_password = credentials.get('sender_password')

        if not sender_email or not sender_password:
            raise ValueError("Email credentials are not set in credentials.json.")

        # Connect to the Gmail SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Start TLS for security
        server.login(sender_email, sender_password)

        # Construct the email
        message = f"Subject: {subject}\n\n{body}"

        # Send the email
        server.sendmail(sender_email, email, message)
        print(f"Email sent successfully to {email}!")

        # Close the connection
        server.quit()
    except Exception as e:
        print(f"Failed to send email to {email}. Error: {e}")

def get_all_emails():
    """Retrieve all registered user emails from the CSV file."""
    emails = []
    try:
        with open('users.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                emails.append(row['email'])
    except FileNotFoundError:
        print("User CSV file not found!")
    return emails

def callback(ch, method, properties, body):
    """Process a broadcast message from RabbitMQ."""
    message = body.decode()
    # make sure to replace single quotes with double quotes
    message = json.loads(message.replace("'", "\""))

    broadcast_body = message.get('body')
    subject = "Broadcast"

    emails = get_all_emails()
    for email in emails:
        send_email(email, subject, broadcast_body)

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Establish a connection to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the queue (ensure it exists)
channel.queue_declare(queue='broadcast_queue')

# Set up a consumer on the queue
channel.basic_consume(queue='broadcast_queue', on_message_callback=callback)

print("Waiting for broadcast messages. To exit, press CTRL+C")
channel.start_consuming()
