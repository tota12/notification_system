# Notification System

This project is a notification system built using Flask and RabbitMQ. It simulates user registeration and sending broadcast messages.

## Setup

1. **Create a virtual environment:**

   ```sh
   python -m venv env
   ```

2. **Activate the virtual environment:**

   ```sh
   .\env\Scripts\activate
   ```

3. **Install the dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Set up RabbitMQ:**

   ```sh
   docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
   ```

5. **Add you Credintials:**
   In the credentials.json replace 'your_email@gmail.com' and 'your_password' with valid credentials.
   You'll need to generate an app password from your email service provider.

## Usage

1. **Start the Flask application:**

   ```sh
   python producer.py
   ```

2. **Run the consumer:**

   ```sh
   python consumer.py
   ```

3. **Run the broadcast consumer:**

   ```sh
   python broadcast_consumer.py
   ```

4. **Register a user:**
   Send a POST request to `/register` with JSON payload containing user's email and name.

5. **Broadcast a message:**
   Send a POST request to `/broadcast` with JSON payload containing the email body.

## Files

- **`producer.py`**: Contains the Flask application with routes for user registration and broadcasting messages.
- **`consumer.py`**: Contains the consumer logic for processing messages from RabbitMQ registration queue.
- **`broadcast_consumer.py`**: Contains the logic for broadcasting messages to all registered users.
- **`credentials.json`**: Contains the credentials for connecting to RabbitMQ.

## License

This project is licensed under the MIT License.
