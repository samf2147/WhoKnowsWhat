import unittest
from config import SQLALCHEMY_DATABASE_URI
from app import db, routes, db_utilities
from app.models import User
import os.path
from hashlib import md5

class SQLTest(unittest.TestCase):
    
    def test_create_user(self):
        '''
        Test whether user is created
        '''
        db_utilities.create_user('temp_user','temp_password',commit=False)
        self.assertTrue(User.query.filter(User.username == 'temp_user'))

if __name__ == '__main__':
    unittest.main()