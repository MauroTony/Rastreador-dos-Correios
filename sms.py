from twilio.rest import Client

def envia_sms(telefone, msg):
    account_sid = "AC3a6539b5deee598f8677aa6614bc07f3"
    auth_token = "518abedfea31a7b9f2301b7581dd6bf6"
    client = Client(account_sid, auth_token)
    message = client.messages \
                    .create(
                         body=msg,
                         from_='+12014307149',
                         to=telefone
                     )