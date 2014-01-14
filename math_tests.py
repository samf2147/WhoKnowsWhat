from app import payment_math
import unittest
from app.models import Event, Payment

class MathTest(unittest.TestCase):
    def setUp(self):
        self.event = Event(name='dummy_event', creator=1)
        self.payment_one = Payment(amount=10.00, event_id=self.event.id, payer='Jimmy')
        self.payment_one = Payment(amount=20.00, event_id=self.event.id, payer='Jimmy')
        self.payment_one = Payment(amount=40.00, event_id=self.event.id, payer='Sam')
        self.payment_one = Payment(amount=50.00, event_id=self.event.id, payer='Harry')
        
    def test_debt_dict(self):
        self.debt_dict = payment_math.debt_dictionary(self.event)
        self.assertAlmostEqual(self.debt_dict['Jimmy'],10.0)
        self.assertAlmostEqual(self.debt_dict['Sam'],0.0)
        self.assertAlmostEqual(self.debt_dict['Harry'],-10.0)

if __name__ == '__main__':
    unittest.main()

