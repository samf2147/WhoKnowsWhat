from models import Payment, Event
import re
import pdb

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
    avg_payment = sum([payment for payer, payment in payment_dict.items()])\
                  /len(payment_dict)
    debt_dict = {}
    for payer, payment in payment_dict.items():
        debt_dict[payer] = avg_payment - payment
    return debt_dict

def payment_list(event):
    '''
    Construct a list of payments
    Each payment is a tuple: (payer,payee,amount)
    '''
    
    #owes is the list of people who underpayed
    #owed is the list of people who overpayed
    owes, owed = [], []
    debt_dict = debt_dictionary(event)
    payment_list = []
    for person, amount in debt_dict.items():
        #use lists b/c they're mutable
        if amount < 0:
            owed.append([person,amount])
        else:
            owes.append([person,amount])
    owes.sort()
    owed.sort(reverse=True)
        
    #for each person owed money, construct payments until they're fully payed
    #amount_owed is negative, owes values will be positive
    current_payer_index = 0
    for payee, amount_owed in owed:
        while amount_owed < 0 and current_payer_index < len(owes):
            #if the ower can fully pay the owee, subtract that amount and move on
            if owes[current_payer_index][1] >= -1*amount_owed:
                owes[current_payer_index][1] += amount_owed
                payment_list.append((owes[current_payer_index][0],payee,-1*amount_owed))
                break
            #otherwise, take as much as we can
            else:
                payment_list.append((owes[current_payer_index][0],payee,
                                     owes[current_payer_index][1]))
                amount_owed += owes[current_payer_index][1]
                current_payer_index += 1
    return payment_list
            
            
            
            
            
            
            
            
            