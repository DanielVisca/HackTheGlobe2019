from twilio.rest import Client

account_sid = 'AC384a4f8fb39ec4a48f45cd8e40e4de2d'
auth_token = 'c924cc19a0fbb9c9f26fbe3564ab0ebd'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Nice headphones",
                     from_='+16042298878',
                     to='+16472951885'
                 )
print(message.sid)