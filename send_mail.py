import smtplib
from email.mime.text import MIMEText

def send_email(customer, dealer, rating, comments):
    server='smtp.mailtrap.io'
    port = 2525
    user = '35011c8d7ed2b3'
    passs = 'f64f860adf07a5'
   # app.config['MAIL_USE_TLS'] = True
   # app.config['MAIL_USE_SSL'] = False
    message = f""" <h3>This is an email test: </h3>
                    <h1> {customer}\n</h1> 
                    <h1> {dealer}\n</h1> 
                    <h1> {rating}\n</h1> 
                    <h1> {comments}\n </h1> """
    sender_email = 'example_1@test.com'
    reciver_email = 'example_2@test.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Feedback_test'
    msg['From'] = sender_email
    msg['To'] = reciver_email

    with smtplib.SMTP(server,port) as server:
        server.login(user,passs)
        server.sendmail(sender_email,reciver_email,msg.as_string())

