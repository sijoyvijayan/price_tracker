from passlib.hash import pbkdf2_sha512
import re


class Utils(object):

    @staticmethod
    def hash_password(password):
        """
        Hashes a password using pbkdf2_sha512
        :param password: The sha512 password from the Login/Register form
        :return: A sha512->pbkdf2_sha512 encrypted password
        """
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        Checks that password sent by user matches the password in the database.
        The database password is encrypted
        :param password: sha512 password
        :param hashed_password: pbkdf2_sha512 password
        :return: True id password match, False otherwise
        """
        return pbkdf2_sha512.verify(password, hashed_password)

    @staticmethod
    def email_is_valid(email):
        email_address_matcher = re.compile('[\w.-]+@([\w-]+\.)+[\w]+')
        print("Checking whether email ID is valid")
        return True if email_address_matcher.match(email) else False
