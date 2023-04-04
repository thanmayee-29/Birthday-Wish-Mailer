import pandas as pd
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import smtplib
from datetime import datetime
from urllib.request import urlopen
import pymysql

# Connect to the database
conn = pymysql.connect(host='localhost', user='root',
                       password='', db='mailer')
cur = conn.cursor()

# Query the data you need from the database and store it in a pandas DataFrame
cur.execute('SELECT name, email, birthday FROM birthdays')
rows = cur.fetchall()
df = pd.DataFrame(rows, columns=['name', 'email', 'birthday'])

today = datetime.now().date()
df['birthday'] = pd.to_datetime(df['birthday'])
today_bdays = df[df['birthday'].dt.date == today]
msg = MIMEMultipart()
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('janapareddythanmayee29@gmail.com', 'ygqyjjuntjqlbjkt')

for index, row in today_bdays.iterrows():
    name = row['name']
    email = row['email']

    text = f'{name} Thanu hopes that we can always be together on this life-adventure. You know that Thanu will always be your best of friends right!!? and so HAPPY BIRTHDAY {name}!! May all your wishes come true.'
    part1 = MIMEText(text, "plain")
    msg.attach(part1)

    url = "file:///C:/Users/yowaisquad/OneDrive/Documents/cake/wishes.html"
    html_content = urlopen(url).read().decode('utf-8')
    body = MIMEText(html_content, 'html')
    msg.attach(body)

    msg['Subject'] = 'Look who\'s shining on their glorious day!!'
    msg['From'] = 'janapareddythanmayee29@gmail.com'
    msg['To'] = email
    server.sendmail('janapareddythanmayee29@gmail.com', email, msg.as_string())

server.quit()
