from models import Payment, Event
import re

def normalize_name(name):
    '''
    Normalize a name
    Put name in title case
    Remove extra spaces
    '''
    normalized = name.strip().lower()
    normalized = re.sub(r' +', ' ', normalized)
    return normalized

def payment_dictionary(event):
    '''
    Construct a dictionary mapping people to their payments
    Strings of people's names are the keys
    Their total payments are the values
    Names are normalized
    '''
    payment_dict = {}
    for payment in event.payments:
        payer = payment.payer
        amount = payment.amount
        if payer in payment_dict:
            payment_dict[payer] += amount
        else:
            payment_dict[payer] = amount
    return payment_dict

def debt_dictionary(event):
    '''Construct a dictionary mapping payers to how much they owe'''
    payment_dict = payment_dictionary(event)
    avg_payment = sum([payment for payer, payment in payment_dict])\
                  /len(payment_dict)
    debt_dict = {}
    for payer, payment in payment_dict:
        debt_dict[payer] = avg_payment - payment
    return debt_dict