import subprocess
import re
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from time import sleep


class Analyser(object):
    LOSS_REGEX = r"([a-z][A-Z])*(?P<loss_percentage>[0-9]+)% loss"
    FILE_NAME = "Connection drops.txt"
    SOURCES = ["www.bbc.co.uk", "www.google.co.uk"]
    PING_CMD = "ping {} -n 1"
    WAIT_SECONDS = 2

    EMAIL_THRESHOLD = 30
    # TODO: Fill in email and password here. Works best with gmail.
    EMAIL_ADDRESS = ""
    EMAIL_PASSWORD = ""

    def __init__(self):
        self.loss_regex = re.compile(self.LOSS_REGEX)
        file = open(self.FILE_NAME, "w")
        file.close()
        self.downtime = 0

    def ping(self):
        cmd_outs = []
        for source in self.SOURCES:
            cmd = subprocess.Popen(self.PING_CMD.format(source),
                                   stdout=subprocess.PIPE)
            cmd_out, _ = cmd.communicate()
            cmd_outs.append(str(cmd_out))
        return cmd_outs

    def filter_output(self, outputs):
        loss_percentage = 100
        for output in outputs:
            match = re.search(self.loss_regex, output)
            if match:
                lost = int(match.group("loss_percentage"))
                if not lost:
                    return 0
        return loss_percentage

    def analyse_ping(self, percentage_loss):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        if percentage_loss:
            self.downtime += self.WAIT_SECONDS
            with open(self.FILE_NAME, "a") as file:
                file.write("{} - Connection down for {} seconds.\n".
                           format(now, self.downtime))
            return
        if self.downtime:
            file = open(self.FILE_NAME, "a")
            file.write("{} - Connection recovered.\n".format(now))
            if self.downtime > self.EMAIL_THRESHOLD:
                try:
                    self.send_notification_email()
                except Exception as e:
                    file.write("Failed to send email.\n{}".format(e))
            self.downtime = 0
            file.close()

    def send_notification_email(self):
        msg = MIMEMultipart()
        msg['From'] = self.EMAIL_ADDRESS
        msg['To'] = self.EMAIL_ADDRESS
        msg['Subject'] = "There has been a connection drop!"

        with open(self.FILE_NAME, "rb") as file:
            part = MIMEApplication(file.read(), _subtype="txt")
        part.add_header('Content-Disposition', 'attachment',
                        filename=self.FILE_NAME)
        msg.attach(part)

        smtp = smtplib.SMTP("smtp.gmail.com")
        smtp.starttls()
        smtp.login(self.EMAIL_ADDRESS, self.EMAIL_PASSWORD)
        smtp.sendmail(self.EMAIL_ADDRESS, [self.EMAIL_ADDRESS], msg.as_string())
        smtp.quit()

    def run(self):
        while True:
            outputs = self.ping()
            percentage_loss = self.filter_output(outputs)
            self.analyse_ping(percentage_loss)
            sleep(self.WAIT_SECONDS)


if __name__ == '__main__':
    analyser = Analyser()
    analyser.run()
