from ..api_users.tasks import notify_project_service
from .subscriber import start_listener
import time

if __name__ == "__main__":
    # Start the listener
    start_listener()

    # Give the listener a moment to start
    time.sleep(1)

    # Publish a test message
    notify_project_service.delay({"event": "new_user", "username": "testuser"})

    # Wait a bit to ensure the message is received
    time.sleep(5)
