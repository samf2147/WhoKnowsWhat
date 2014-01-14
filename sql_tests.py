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
    
    def test_money_pattern(self):
        '''
        Test pattern for turning strings of money into amounts
        '''
        test_values = ['$120.00','Jimmy: 120.00','120.00','120']
        for test_value in test_values:
            self.assertAlmostEqual(db_utilities.payment_to_float(test_value),120.00)

if __name__ == '__main__':
    unittest.main()