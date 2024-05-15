class EmailContentUtil:
    @staticmethod
    def register_email_content(user, url):
        subject = "Welcome to our platform!"
        body = f"Hi {user.first_name}, welcome to our platform! Please verify your email address by clicking the link below:\n{url}"
        return subject, body

    @staticmethod
    def reset_password_email_content(user, url):
        subject = "Password reset request"
        body = f"Hi {user.first_name}, you request a password reset, Click the link below to reset your password:\n {url}"
        return subject, body

    #         subject = "Password Reset Request"
    #         body = f"Hi {user.first_name}, you requested a password reset. Click the link below to reset your password: {url}"
