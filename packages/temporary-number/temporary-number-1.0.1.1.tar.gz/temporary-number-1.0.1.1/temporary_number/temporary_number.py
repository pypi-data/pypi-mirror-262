from bs4 import BeautifulSoup
import tls_client
import random

def get_number(country="UK"):
  if country == "Random":
    country = random.choice(["UK", "US", "France", "Netherlands", "Finland"])
  if country not in ["UK", "US", "France", "Netherlands", "Finland"]:
    raise ValueError("Unsupported Country")
  session = tls_client.Session(client_identifier="chrome112", random_tls_extension_order=True)
  maxpages = {"UK": 59, "US": 3, "France": 73, "Netherlands": 60, "Finland": 47}
  maxpage = maxpages[country]
  minpage = 20
  if country in ["US"]:
    minpage = 1
  page = random.randint(minpage, maxpage)
  if page == 1:
    res = session.get(f"https://temporary-phone-number.com/{country}-Phone-Number")
  else:
    res = session.get(f"https://temporary-phone-number.com/{country}-Phone-Number/page{page}")
  soup = BeautifulSoup(res.content, "lxml")
  numbers = []
  plist = {"UK": "+44", "US": "+1", "France": "+33", "Netherlands": "+31", "Finland": "+358"}
  p = plist[country]
  for a in soup.find_all("a"):
    a = a.get("title", "none")
    if f"{country} Phone Number {p}" in a:
      a = a.replace(f"{country} Phone Number ", "").replace(" ", "")
      numbers.append(a)
  return random.choice(numbers)

class sms_message(object):
  content = ""
  frm = ""
  time = ""

  def __init__(self, content, frm, time):
      self.content = content
      self.frm = frm
      self.time = time

def get_messages(number: str):
  number = number.replace("+", "")
  try:
    i = int(number)
  except:
    raise ValueError("Wrong Number")
  countries = {"44": "UK", "1": "US", "33": "France", "31": "Netherlands", "358": "Finland"}
  country = None
  for key, value in countries.items():
    if number.startswith(key):
      country = value
  if country == None:
    raise ValueError("Unsupported Country")
  session = tls_client.Session(client_identifier="chrome112", random_tls_extension_order=True)
  res = session.get(f"https://temporary-phone-number.com/{country}-Phone-Number/{number}")
  if res.status_code == 404:
    raise ValueError("Number doesn't exist")
  soup = BeautifulSoup(res.content, "lxml")
  divclass = ""
  messages = []
  message = {"content": None, "frm": "", "time": ""}
  for div in soup.find_all("div"):
    divclass = div.get("class", "None")[0]
    if divclass == "direct-chat-info":
      message["frm"] = div.text.split("\n")[1].replace("From ", "")
      message["time"] = div.text.split("\n")[2]
    if divclass == "direct-chat-text":
      message["content"] = div.text
      messages.append(sms_message(content=message["content"], frm=message["frm"], time=message["time"]))
      message = {"content": None, "frm": "", "time": ""}
  return messages
