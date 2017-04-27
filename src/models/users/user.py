import uuid
import src.models.users.errors as UserErrors
import src.models.users.constants as UserConstants

from src.common.database import Database
from src.common.utils import Utils
from src.models.alerts.alert import Alert



class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User {}>".format(self.email)

    @staticmethod
    def is_login_valid(email, password):
        """
        This method verifies that email/password combo (as sent by the site forms) is valid or not.
        Check that the email exists and the password associated to that email is correct
        :param email: The user's email
        :param password: A sha512 hashed password
        :return: True if valid, False otherwise
        """
        print("email: {}".format(email))
        user_data = Database.find_one('users', {"email": email})
        if user_data is None:
            # User email doesn't exist
            raise UserErrors.UserNotExistsError("User doesn't exist")
        if not Utils.check_hashed_password(password, user_data['password']):
            # Password entered is incorrect
            raise UserErrors.IncorrectPassword("Your password is incorrect")

        return True

    @staticmethod
    def register_user(email, password):
        """
        This method registers user using email and password.
        Password is sent from form and is a sha512 password.
        It checks if the email is valid and is not already registered
        :param email: User's email
        :param password: Password entered by user
        :return: True if registration is successful, Else False
        """
        user_data = Database.find_one('users', {"email": email})
        if user_data is not None:
            raise UserErrors.UserAlreadyRegisteredError("The email-id you used to register already exists")
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError("The email-id format is invalid")

        User(email, Utils.hash_password(password)).save_to_db()
        return True

    def save_to_db(self):
        Database.insert('users', self.json())

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }

    @classmethod
    def find_by_email(cls, email):
        return cls(**Database.find_one(UserConstants.COLLECTION, {"email": email}))

    def get_alerts(self):
        return Alert.find_by_user_email(self.email)
