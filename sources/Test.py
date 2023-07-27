

### Below Code Sends email using python

import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import mysql.connector
from sshtunnel import SSHTunnelForwarder
import json
import pandas as pd

#Connection with prod db
tunnel = SSHTunnelForwarder(('172.29.65.120', 22), ssh_password="jumpbox", ssh_username="jumpbox",
      remote_bind_address=("172.29.115.79", 3306)) 
tunnel.start()

prod_connection = mysql.connector.connect(
        user= "Prd43eo32RUsr",
        password="8NcDnhrfp7",
        host="127.0.0.1",
        database="til_expresso_db",
        port=tunnel.local_bind_port
        )

print("Connection with prod mysql established")


## Dataframe from sql database
df = pd.read_sql("select r.expresso_id,date(r.order_create_date) as Order_Date, concat(COALESCE(u2.first_name,''), ' ' , COALESCE(u2.last_name,'')) as Sales_User, concat(COALESCE(u.first_name,''), ' ' , COALESCE(u.last_name,'')) as OPS_User, case r.status when 1 then 'Waiting for submission' when 2 then 'Pending' when 3 then 'Rejected' when 4 then 'Recalled' when 5 then 'Approved' when 100 then 'Sales User Review Required' when 109 then 'Value Add Approval Required' when 203 then 'CS Approval Required' when 210 then 'IRO Approved' when 211 then 'Campaign Created' when 215 then 'Finance Review Required For Campaign Close' when 321 then 'Invoice Generated' when 333 then 'Completed' else 'Others' end as Campaign_Status from til_ro r join til_ro_lineitem rl on r.til_ro_id = rl.til_ro_id join til_lineitem l on rl.til_lineitem_id = l.til_lineitem_id join til_user u on u.til_user_id = l.til_user_id_ops join til_user u2 on u2.til_user_id = r.til_user_id_sales where r.demand_channel = 0 and DATEDIFF(SYSDATE(), r.order_create_date) <= 7 AND r.company_code = 6200 AND r.til_user_id_sales IN (5243,28359,43415,45287,47047,52588,54494,57925,58311,58733,59724,60589,64672,65964,66308,66479,67194,67448,67498,68263,68265,68268,68270,68271,68273,68806,69482,69551,69607,69639,69679,69680,69799,70304,70305,70374,70413,70617,70866,70873,71282,71289,71574,71575,71576,71664) group by 1,2,3,4,5 order by 5",prod_connection)
df1 = pd.read_sql("select case r.status when 1 then 'Waiting for submission' when 2 then 'Pending' when 3 then 'Rejected' when 4 then 'Recalled' when 5 then 'Approved' when 100 then 'Sales User Review Required' when 109 then 'Value Add Approval Required' when 203 then 'CS Approval Required' when 210 then 'IRO Approved' when 211 then 'Campaign Created' when 215 then 'Finance Review Required For Campaign Close' when 321 then 'Invoice Generated' when 333 then 'Completed' else 'Others' end as Campaign_Status, count(distinct r.expresso_id) as RO_Count from til_ro r where r.demand_channel = 0 and DATEDIFF(SYSDATE(), r.order_create_date) <= 7 AND r.company_code = 6200 AND r.til_user_id_sales IN (5243,28359,43415,45287,47047,52588,54494,57925,58311,58733,59724,60589,64672,65964,66308,66479,67194,67448,67498,68263,68265,68268,68270,68271,68273,68806,69482,69551,69607,69639,69679,69680,69799,70304,70305,70374,70413,70617,70866,70873,71282,71289,71574,71575,71576,71664) group by 1 order by 2 desc",prod_connection)



# Convert DataFrame df1 to an HTML table
html_table = df1.to_html(index=False)

# Email content and details # Custom message with HTML line breaks
custom_message = "Hello,<br><br>Below is the Statuswise summary of RO's created in last 7 days. Campaign wise details are shared in the CSV attachment.<br><br>Regards,<br>Rahul Vimal<br><br>"


# Email content and details
mail_content = f"{custom_message}<html><body>{html_table}</body></html>"


sender_address = 'rahul.vimal@timesinternet.in'
sender_pass = 'xdoafioynpdbjapw' ## This is gmail app password for the above email id
receiver_address = 'rahul.vimal@timesinternet.in'

# Setup the MIME
message = MIMEMultipart()
message['From'] = sender_address
message['To'] = receiver_address
message['Subject'] = 'New Campaigns Created in last 7 days'

# Attach the email body
#message.attach(MIMEText(mail_content, 'plain'))
message.attach(MIMEText(mail_content, 'html'))


# Convert DataFrame to CSV and attach it as an attachment
csv_string = df.to_csv(index=False)  # Convert DataFrame to CSV string
csv_part = MIMEBase('application', 'octet-stream')
csv_part.set_payload(csv_string)
encoders.encode_base64(csv_part)
csv_part.add_header('Content-Disposition', 'attachment; filename="data_dump.csv"')
message.attach(csv_part)

# Create SMTP session for sending the mail
session = smtplib.SMTP('smtp.gmail.com', 587)  # use Gmail with port
session.starttls()  # enable security
session.login(sender_address, sender_pass)  # login with mail_id and password
text = message.as_string()
session.sendmail(sender_address, receiver_address, text)
session.quit()

print('Mail Sent')
