from core._shared.notification.notification import Notification
from core._shared.notification.notification_error import NotificationError, NotificationException


class TestNotification:
    def test_should_create_single_error(self):
        notification = Notification()
        error = NotificationError(
            message="error message",
            context="customer",
        )
        notification.add_error(error)
        assert notification.messages("customer") == "customer: error message"

    def test_should_create_multiple_errors(self):
        notification = Notification()
        error = NotificationError(
            message="error message",
            context="customer",
        )
        notification.add_error(error)

        error_2 = NotificationError(
            message="error message 2",
            context="customer",
        )
        notification.add_error(error_2)

        assert notification.messages("customer") == "customer: error message,customer: error message 2"

    def test_should_only_return_erros_by_context(self):
        notification = Notification()
        error = NotificationError(
            message="error message",
            context="customer",
        )
        error_2 = NotificationError(
            message="error message 2",
            context="order",
        )
        notification.add_error(error)
        notification.add_error(error_2)

        assert notification.messages("customer") == "customer: error message"
        assert notification.messages("order") == "order: error message 2"

    def test_when_no_context_provided_then_return_all_errors(self):
        notification = Notification()
        error = NotificationError(
            message="error message",
            context="customer",
        )
        error_2 = NotificationError(
            message="error message 2",
            context="order",
        )
        notification.add_error(error)
        notification.add_error(error_2)

        assert notification.messages("") == "customer: error message,order: error message 2"

    def test_check_if_has_error(self):
        notification = Notification()
        error = NotificationError(
            message="error message",
            context="customer",
        )

        assert notification.has_errors() is False

        notification.add_error(error)

        assert notification.has_errors() is True

    def test_raise_error_when_has_errors(self):
        notification = Notification()
        error = NotificationError(
            message="error message",
            context="customer",
        )
        notification.add_error(error)
        notification.add_error(error)

        try:
            raise NotificationException(notification.errors)
        except NotificationException as error:
            assert str(error) == "customer: error message,customer: error message"
