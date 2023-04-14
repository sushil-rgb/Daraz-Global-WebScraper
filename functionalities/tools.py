import re
import os
import yaml
import random
import smtplib
import itertools
from email.message import EmailMessage


class TryExcept:
    async def text(self, element):        
        try:
            elements = (await (await element).inner_text()).strip()
        except AttributeError:
            elements = "N/A"        
        return elements

    async def attributes(self, element, attr):        
        try:
            elements = await (await element).get_attribute(attr) 
        except AttributeError:
            elements = "N/A"
        return elements


class AlertEmail:
    def __init__(self, emailUserSender, emailSenderPassword):        
        self.emailUserSender = emailUserSender        
        self.emailPassword = emailSenderPassword        

    
    def sendAlert(self, emailUserReceiver, msgSubject, msgContent):
        self.emailUserReceiver = emailUserReceiver
        self.msgSubject = msgSubject
        self.msgContent = msgContent        

        msg = EmailMessage()
        msg['Subject'] = self.msgSubject
        msg["From"] = self.emailUserSender
        msg['To'] = self.emailUserReceiver
        msg.set_content(self.msgContent)        

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(self.emailUserSender, self.emailPassword)
            smtp.send_message(msg)
            smtp.quit()
    

async def verifyDarazURL(url):
    daraz_pattern = re.search("""^https://www.daraz.(com.np|lk|pk|com.bd)/+""", url)
    if daraz_pattern == None:
        return True
    else:
        return False


async def check_domain(url):
    pattern = re.search(r"(.np|.bd|.lk|.pk)", url) 
    domain_lists = {
        'np': 'Nepal',
        'lk': 'Sri Lanka',
        'bd': 'Bangladesh',
        'pk': 'Pakistan',
    }
    country =pattern.group(1).replace(".", '')
    return domain_lists[country]
    
                

# For flattening the multi-dimensional lists:
def flat(d_lists):    
    return list(itertools.chain(*d_lists))


def yamlMe(selectors):
    with open(f"scrapersFunctionalities\\{selectors}.yaml") as file:
        sel = yaml.load(file, Loader = yaml.SafeLoader)
        return sel


def userAgents():
   with open(f"{os.getcwd()}\\functionalities\\user-agents.txt") as f:
    agents = f.read().split("\n")
    return random.choice(agents)
   
   