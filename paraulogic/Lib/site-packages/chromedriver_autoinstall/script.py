import requests
from bs4 import BeautifulSoup
import zipfile
import io
from subprocess import PIPE, run
import sys
import os
import lxml
import re
import json
from urllib.request import urlopen


def out(command):
   result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
   return result.stdout


def get_platform():
   if sys.platform == "darwin":
      if "arm64" in out("uname -m"):
         return "mac-arm64"
      return "mac-x64"
   elif sys.platform.startswith("win"):
      return "win32"
   elif "linux" in sys.platform:
      return "linux64"


def get_version():
   platform = get_platform()
   if "mac" in platform:
      chrome_download_path = "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version"
   elif "win" in platform:
      chrome_download_path = 'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version'
   elif "linux" in platform:
      chrome_download_path = "google-chrome --version"
   version = re.Match.group(re.search(r"[\d.]+", out(chrome_download_path)))
   if int(version[:version.index(".")]) >= 115:
      return version
   return int(version[:version.index(".")])


def get_download_page():
   version = get_version()
   if isinstance(version, int):
      url, urls = "https://chromedriver.chromium.org/downloads", []
      r = requests.get(url, allow_redirects=True)
      soup = BeautifulSoup(r.text, 'html.parser')
      for link in soup.find_all('a'):
         urls.append(str(link.get('href')))
      for u in urls:
         if (f"https://chromedriver.storage.googleapis.com/index.html?path={version}" in u):
            return u
   elif isinstance(version, str):
      url = "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"
      response = urlopen(url)
      data = json.loads(response.read())
      target_dict = {l["version"][0:3]: l for l in data["versions"]}[version[0:3]]
      target_dict = {l["platform"]: l for l in target_dict["downloads"]["chromedriver"]}
      return target_dict[get_platform()]["url"]
      

def download_and_unzip():
   platform = get_platform()
   version = get_version()
   url = get_download_page()
   if isinstance(version, int):
      url = url.replace("index.html?path", "?delimiter=/&prefix")
      soup = BeautifulSoup(requests.get(url).text, features="xml").find_all("Key")
      keys = [f"https://chromedriver.storage.googleapis.com/{k.getText()}" for k in soup if platform in k.getText()]
      url = keys[0]
   url = requests.get(url, stream=True)
   z = zipfile.ZipFile(io.BytesIO(url.content))
   z.extractall()
   # MacOS only
   if "mac" in platform:
      path = f"./chromedriver-{platform}/chromedriver"
      out(f"chmod +x {path}")
      os.chmod(path, 0o755)
   path = f"{os.path.abspath(os.getcwd())}/chromedriver-{platform}"
   print(f"install path: {path}")
   

def install():
   download_and_unzip()