from app import payment_math
import unittest
from app.models import Event, Payment

class DummyEvent:
    def __init__(self,name,id,payments):
        self.name=name
        self.id=id
        self.payments=payments

class DummyPayment:
    def __init__(self,payer,amount):
        self.payer=payer
        self.amount=amount
    

class MathTest(unittest.TestCase):
    def setUp(self):
        #creating dummy objects for functions
        self.payment_one = DummyPayment(payer='Jimmy',amount=10.00)
        self.payment_two = DummyPayment(payer='Jimmy',amount=20.00)
        self.payment_three = DummyPayment(payer='Sam',amount=40.00)
        self.payment_four = DummyPayment(payer='Harry',amount=50.00)
        self.event = DummyEvent(name='dummy_event',id=1,payments=
         [self.payment_one, self.payment_two, self.payment_three, self.payment_four])
        
    def test_debt_dict(self):
        self.debt_dict = payment_math.debt_dictionary(self.event)
        self.assertAlmostEqual(self.debt_dict['Jimmy'],10.0)
        self.assertAlmostEqual(self.debt_dict['Sam'],0.0)
        self.assertAlmostEqual(self.debt_dict['Harry'],-10.0)
    
    def test_payment_list(self):
        self.payment_list = payment_math.payment_list(self.event)
        self.assertEqual(self.payment_list[0][0],'Jimmy')
        self.assertEqual(self.payment_list[0][1],'Harry')
        self.assertAlmostEqual(self.payment_list[0][2],10.0)

if __name__ == '__main__':
    unittest.main()

