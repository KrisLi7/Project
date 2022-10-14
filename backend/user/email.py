""" Implementation for email.py """

import smtplib
import ssl
from email.message import EmailMessage
from email.mime.text import MIMEText


class Email:
    def __init__(self, receiver_email, username):
        self.sender_email = "noreply.nobugplz@gmail.com"
        self.receiver_email = receiver_email
        self.password = "vutrxiffkqntsbth"
        self.username = username

    def sendResetEmail(self, reset_code):
        """
        A function that send a reset code for reseting password
        in html format
        """
        message = EmailMessage()
        message["Subject"] = "Verification code to reset PlzNoBug password"
        message["From"] = "PlzNoBug"
        message["To"] = self.receiver_email
        html = """
        <html>
        <head>
        <style>
            a:hover, a:active {{
                background-color: #040714 !important;
                color: white !important;
                padding: 14px 25px !important;
            }}
        </style>
        </head>
        <body>
            <center style="background-color: #f7f7f7;
                font-size:3vw;
                color:#0063E5;
                padding: 3% 25% 3% 25%;">
                Verification code to reset PlzNoBug password
            </center>
            <br>
            <br>
            <p style="font-size:1vw;
                color:#040714;
                padding: 0% 25% 0% 25%;"> Hi, {}:
            </p>
            <br>
            <center style="font-size:1vw;
                color:#040714;
                padding: 0% 30% 0% 30%;">
                To reset your password, enter this verification code when prompted:
            <br>
            <a  style="background-color: #0063E5;
                color: white;
                font-size:1vw;
                padding: 14px 25px;
                text-align: center;
                text-decoration: none;
                display: inline-block;"
                href="http://localhost:3000/password/reset" target="_blank">
                {}
            </a>
            </center>
            <br>
            <br>
            <p style="font-size:1vw;
                color:#040714;
                padding: 0% 25% 0% 25%;"> Thanks, <br> PlzNoBug
            </p>
            <br>
            <center style="background-color: #f7f7f7;
                font-size:1vw;
                color:#949494;
                padding: 9px 25% 9px 25%;"> <i>PlzNoBug Movie Website</i>
                <br>
                Please don't reply to this email
                <br>
                <br>
                Copyright PlzNoBug
            </center>
        </body>
        </html>
        """.format(self.username,reset_code)
        email_context = MIMEText(html, "html")
        message.set_content(email_context)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
        server.login(self.sender_email, self.password)
        server.send_message(message)
        server.close()


    def sendVerifyEmail(self, u_id):
        """
        A function that send a verification url email for register account
        in html format
        """
        message = EmailMessage()
        message["Subject"] = "Verify your email address"
        message["From"] = self.sender_email
        message["To"] = self.receiver_email
        html = """
        <html>
        <head>
        <style>
            a:hover, a:active {{
                background-color: #040714 !important;
                color: white !important;
                padding: 14px 25px !important;
            }}
        </style>
        </head>
        <body>
            <center style="background-color: #f7f7f7;
                font-size:3vw;
                color:#0063E5;
                padding: 3% 25% 3% 25%;">
                Verify your email address
            </center>
            <br>
            <br>
            <p style="font-size:1vw;
                color:#040714;
                padding: 0% 25% 0% 25%;"> Hi, {}:
            </p>
            <br>
            <center style="font-size:1vw;
                color:#040714;
                padding: 0% 30% 0% 30%;">
                Thanks for your interest in creating an NoBugPlz account.
                To create your account, please verify your email address by clicking below.
            <br>
            <a  style="background-color: #0063E5;
                color: white;
                font-size:1vw;
                padding: 14px 25px;
                text-align: center;
                text-decoration: none;
                display: inline-block;"
                href="http://localhost:3000/verify/email/{}" target="_blank">
                Verify email
            </a>
            </center>
            <br>
            <br>
            <p style="font-size:1vw;
                color:#040714;
                padding: 0% 25% 0% 25%;"> Thanks, <br> PlzNoBug
            </p>
            <br>
            <center style="background-color: #f7f7f7;
                font-size:1vw;
                color:#949494;
                padding: 9px 25% 9px 25%;"> <i>PlzNoBug Movie Website</i>
                <br>
                Please don't reply to this email
                <br>
                <br>
                Copyright PlzNoBug
            </center>
        </body>
        </html>
        """.format(self.username, u_id)

        email_context = MIMEText(html, "html")
        message.set_content(email_context)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
        server.login(self.sender_email, self.password)
        server.send_message(message)
        server.close()


    def sendVerifyEmailForChangeEmail(self, u_id):
        """
        A function that send a verification url email for change email
        in html format
        """
        message = EmailMessage()
        message["Subject"] = "Verify your email address"
        message["From"] = self.sender_email
        message["To"] = self.receiver_email
        html = """
        <html>
        <head>
        <style>
            a:hover, a:active {{
                background-color: #040714 !important;
                color: white !important;
                padding: 14px 25px !important;
            }}
        </style>
        </head>
        <body>
            <center style="background-color: #f7f7f7;
                font-size:3vw;
                color:#0063E5;
                padding: 3% 25% 3% 25%;">
                Verify your email address
            </center>
            <br>
            <br>
            <p style="font-size:1vw;
                color:#040714;
                padding: 0% 25% 0% 25%;"> Hi, {}:
            </p>
            <br>
            <center style="font-size:1vw;
                color:#040714;
                padding: 0% 30% 0% 30%;">
                To successfully change your email address,
                please verify your email address by clicking below.
            <br>
            <a  style="background-color: #0063E5;
                color: white;
                font-size:1vw;
                padding: 14px 25px;
                text-align: center;
                text-decoration: none;
                display: inline-block;"
                href="http://localhost:3000/verify/email/{}" target="_blank">
                Verify email
            </a>
            </center>
            <br>
            <br>
            <p style="font-size:1vw;
                color:#040714;
                padding: 0% 25% 0% 25%;"> Thanks, <br> PlzNoBug
            </p>
            <br>
            <center style="background-color: #f7f7f7;
                font-size:1vw;
                color:#949494;
                padding: 9px 25% 9px 25%;"> <i>PlzNoBug Movie Website</i>
                <br>
                Please don't reply to this email
                <br>
                <br>
                Copyright PlzNoBug
            </center>
        </body>
        </html>
        """.format(self.username, u_id)

        email_context = MIMEText(html, "html")
        message.set_content(email_context)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
        server.login(self.sender_email, self.password)
        server.send_message(message)
        server.close()


    def sendRecommendEmail(self, movie_list):
        """
        A function that send a new movie recommend email
        in html format
        """
        message = EmailMessage()
        message["Subject"] = "New Movies Coming Out"
        message["From"] = self.sender_email
        message["To"] = self.receiver_email
        html = """
        <html>
        <head>
        <style>
            a:hover, a:active {{
                text-decoration: underline !important;
                text-decoration-color: #040714 !important;
                padding: 14px 25px !important;
            }}
        </style>
        </head>
        <body>
            <center style="background-color: #f7f7f7;
                font-size:3vw;
                color:#0063E5;
                padding: 3% 25% 3% 25%;">
                New Upcoming Movie!
            </center>
            <br>
            <br>
            <p style="font-size:1vw;
                color:#040714;
                padding: 0% 25% 0% 25%;"> Hi, {}:
            </p>
            <br>
            <center style="font-size:1vw;
                color:#040714;
                padding: 0% 30% 0% 30%;">
            Below is the list of new movies coming out on this week:
            <br>
        """.format(self.username)

        for movie in movie_list:
            html += """
                <a  style="padding: 14px 25px;
                    color: #0063E5;
                    font-size:1vw;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;"
                    href="http://localhost:3000/movie/{}" target="_blank">
                    {}: release on {}
                </a>
                <br>
            """.format(movie[0], movie[1], movie[2])
        html += """
            </center>
                <br>
                <br>
                <p style="font-size:1vw;
                    color:#040714;
                    padding: 0% 25% 0% 25%;"> Thanks, <br> PlzNoBug
                </p>
                <br>
                <center style="background-color: #f7f7f7;
                    font-size:1vw;
                    color:#949494;
                    padding: 9px 25% 9px 25%;"> <i>PlzNoBug Movie Website</i>
                    <br>
                    Please don't reply to this email
                    <br>
                    <br>
                    Copyright PlzNoBug
                </center>
            </body>
            </html>
        """

        email_context = MIMEText(html, "html")
        message.set_content(email_context)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
        server.login(self.sender_email, self.password)
        server.send_message(message)
        server.close()


    def sendReviewMessageEmail(self, u_id, username, m_id, title):
        """
        A function that send a new review message notification
        in html format
        """
        message = EmailMessage()
        message["Subject"] = "New review for the movie in your wishlist"
        message["From"] = self.sender_email
        message["To"] = self.receiver_email
        html = """
            <html>
            <head>
            <style>
                a:hover, a:active {{
                    text-decoration: underline !important;
                    text-decoration-color: #0063E5 !important;
                }}
            </style>
            </head>
            <body>
                <center style="background-color: #f7f7f7;
                    font-size:3vw;
                    color:#0063E5;
                    padding: 3% 25% 3% 25%;">
                    A User has Post a Review for the Movie in your Wishlist
                </center>
                <br>
                <br>
                <p style="font-size:1vw;
                    color:#040714;
                    padding: 0% 25% 0% 25%;"> Hi, {}:
                </p>
                <br>
                <center style="font-size:1vw;
                    color:#040714;
                    padding: 0% 30% 0% 30%;">
                <a  style="color: #040714;
                    font-size:1vw;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;"
                    href="http://localhost:3000/user/pofile/{}" target="_blank">
                    {}
                </a>
                <p  style="color: #040714;
                    font-size:1vw;
                    display: inline;">
                    post a review on the movie "
                </p>
                <a  style="color: #040714;
                    font-size:1vw;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;"
                    href="http://localhost:3000/movie/{}" target="_blank">
                    {}
                </a>
                <p  style="color: #040714;
                    font-size:1vw;
                    display: inline;">
                    " in your wish list.
                </p>
                <br>
                <p style="color: #040714;
                    font-size:1vw;">
                    press on the user name to get redirect to his profile or
                    press on the movie title to get redirect to the movie information page.
                </p>
                </center>
                <br>
                <br>
                <p style="font-size:1vw;
                    color:#040714;
                    padding: 0% 25% 0% 25%;"> Thanks, <br> PlzNoBug
                </p>
                <br>
                <center style="background-color: #f7f7f7;
                    font-size:1vw;
                    color:#949494;
                    padding: 9px 25% 9px 25%;"> <i>PlzNoBug Movie Website</i>
                    <br>
                    Please don't reply to this email
                    <br>
                    <br>
                    Copyright PlzNoBug
                </center>
            </body>
            </html>
        """.format(self.username, u_id, username, m_id, title)

        email_context = MIMEText(html, "html")
        message.set_content(email_context)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
        server.login(self.sender_email, self.password)
        server.send_message(message)
        server.close()
