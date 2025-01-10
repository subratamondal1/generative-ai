# Factory Pattern Components
# 1. Product: An interface or abstract class that defines the type of objects the factory method creates.
# 2. Concrete Products: Classes that implement the Product interface.
# 3. Creator (Factory): An abstract class or interface that declares the factory method.
# 4. Concrete Creators: Classes that implement the factory method to create Concrete Products.


from abc import ABC, abstractmethod


# 1. Product Abstract Class
class Notification(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        pass


# 2. Concrete Products
class EmailNotification(Notification):
    def send(self, message: str) -> None:
        print(f"Sending Email with message: {message}")


class SMSNotification(Notification):
    def send(self, message: str) -> None:
        print(f"Sending SMS with message: {message}")


class PushNotification(Notification):
    def send(self, message: str) -> None:
        print(f"Sending Push Notification with message: {message}")


# 3. Creator (Factory) Abstract Class
class NotificationFactory(ABC):
    @staticmethod
    def create_notification(notification_type: str) -> Notification:
        if notification_type == "EMAIL":
            return EmailNotification()
        elif notification_type == "SMS":
            return SMSNotification()
        elif notification_type == "PUSH":
            return PushNotification()
        else:
            raise ValueError(f"Invalid notification type: {notification_type}")


# 4. Concrete Products Creators

if __name__ == "__main__":
    factory = NotificationFactory()
    user_preferences: list[str] = ["EMAIL", "SMS", "PUSH"]

    for preference in user_preferences:
        notification: Notification = factory.create_notification(
            notification_type=preference
        )
        notification.send(message="Hi! I am Subrata.")
