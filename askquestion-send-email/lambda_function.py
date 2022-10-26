import json,boto3
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from boto3.dynamodb.conditions import Key, Attr

from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # TODO implement
    ddbClient = boto3.resource('dynamodb', region_name='us-west-2')
    table = ddbClient.Table('askquestion')
    
    
    #print(event)
    #email=event['queryStringParameters']['email']
    email="kavashgar@gmail.com"
    # registerDate in epoch format
    #registerDate=event['queryStringParameters']['registerDate']
    registerDate='1569923827468'
    # product cloudaz or skydrm
    #sourceType=event['queryStringParameters']['sourceType']
    sourceType='cloudaz'
    
    try:
        
        responseGet = table.scan(FilterExpression=Attr('registerDate').eq(registerDate) &  Attr('email').eq(email))
        items = responseGet['Items']

        for item in items:
            if item['email']==email:
                name=item['name']
                company=item['company']
                phone=item['phone']
                registerDate=item['registerDate']
                message=item['message']
                sourceType=item['sourceType']

                toEmail="kavashgar@gmail.com"

                if sourceType=="skydrm":
                    fromEmail =  "admin@skydrm.com"
                elif sourceType =="cloudaz":
                    fromEmail =  "admin@cloudaz.com"
                elif sourceType =="cloudaz":
                    fromEmail =  "admin@cloudaz.com"
            
                # Create message container - the correct MIME type is multipart/alternative.
                msg = MIMEMultipart('alternative')
                msg['Subject'] = sourceType + ": Ask Question Form Data"
                msg['From'] = fromEmail
                msg['To'] = toEmail
                
                # Create the body of the message (a plain-text and an HTML version).
               
                html = """
                    <html>
                        <head>
                      <style type="text/css">
                        .askForm {
                            font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
                            border-collapse: collapse;
                            width: 100%;
                        }

                        .askForm td, .askForm th {
                            border: 1px solid #ddd;
                            padding: 8px;
                        }

                        .askForm tr:nth-child(even){background-color: #f2f2f2;}

                        .askForm tr:hover {background-color: #ddd;}

                        .askForm th {
                            padding-top: 12px;
                            padding-bottom: 12px;
                            text-align: left;
                            background-color: #f16a25;
                            color: white;
                        }
                    </style>
                    </head>
                    <body>
                    
                    <table class='askForm'>
                    """
                properDateFormat=time.strftime('%Y-%m-%d', time.localtime(int(registerDate)))
                html=html + '<tr>'
                html=html + '<td>Date Received</td>'
                html=html + '<td>' + properDateFormat + '</td>'
                html=html + '</tr>'

                html=html + '<tr>'
                html=html + '<td>Product</td>'
                html=html + '<td>' + sourceType + '</td>'
                html=html + '</tr>'

                html=html + '<tr>'
                html=html + '<td>Name</td>'
                html=html + '<td>' + name + '</td>'
                html=html + '</tr>'

                html=html + '<tr>'
                html=html + '<td>Company</td>'
                html=html + '<td>' + company + '</td>'
                html=html + '</tr>'

                html=html + '<tr>'
                html=html + '<td>Phone</td>'
                html=html + '<td>' + phone + '</td>'
                html=html + '</tr>'

                html=html + '<tr>'
                html=html + '<td>Message</td>'
                html=html + '<td>' + message + '</td>'
                html=html + '</tr>'

                html=html + """
                    </body>
                  </html>
                """
                
                part = MIMEText(html, 'html')
                try:
                    msg.attach(part)
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login("admin@cloudaz.com", "sgjunjhxnqisfmwr")
                    server.sendmail(fromEmail, toEmail, msg.as_string())
                    server.quit()
                    print("email has been sent successfully")

                except smtplib.SMTPException as e:
                    print(str(e))
                    return { 
                            "statusCode": 500,
                            "body": json.dumps("error"),
                            "isBase64Encoded": "false",
                            "headers": {
                                    "Access-Control-Allow-Origin" : "*", 
                                    "Access-Control-Allow-Credentials" : "true"
                             }
                    
                    }

        return { 
                "statusCode": 200,
                "body": json.dumps("success"),
                "isBase64Encoded": "false",
                "headers": {
                        "Access-Control-Allow-Origin" : "*", 
                        "Access-Control-Allow-Credentials" : "true"
                 }
            
        }
        
    
    except ClientError as e:
        print(set(e))
        return { 
                "statusCode": 500,
                "body": json.dumps("error"),
                "isBase64Encoded": "false",
                "headers": {
                        "Access-Control-Allow-Origin" : "*", 
                        "Access-Control-Allow-Credentials" : "true"
                 }
            
        }

       
