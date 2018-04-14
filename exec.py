try:
  import Image
except ImportError:
  from PIL import Image
import pytesseract
from subprocess import call
import sys
import subprocess
import time
from datetime import datetime
import requests
# import urllib
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

diag = {}

# helpers
def get_ts():
  """Return the current time stamp in seconds."""
  
  return int(round(time.time() * 1000))

def dd(dbg_str):
  """Print's out dbg_str to the console, along with helpful time stamps."""

  print('['+str(datetime.now())+'] ' + dbg_str)

def search_query(srch_query):
  """Search google for the specified phrase i.e. srch_query."""
  
  dd('qry: '+srch_query)
  headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

  # page = requests.get("https://www.google.co.in/search?dcr=0&source=hp&q=Grieving+Cloak", headers=headers)
  page = requests.get("https://www.google.co.in/search?dcr=0&source=hp&q="+quote_plus(srch_query), headers=headers)
  diag['ts_wwwsearch'] = get_ts()

  dd('parse_begin')
  soup = BeautifulSoup(page.content, 'lxml')
  diag['ts_parse'] = get_ts()
  # print(soup.prettify())
  
  dd('search_begin')
  srchs = soup.find_all('div', class_='rc')
  
  for srch_res in srchs:
    # print(*srch_res)
    srch_title_h3 = srch_res.find('h3', class_='r')
    srch_title = srch_title_h3.find('a')
    print(srch_title.get_text().upper())
    srch_desc = srch_res.find('span', class_='st')
    print(srch_desc.get_text())
    print('--------------------------------------------------')
  
  diag['ts_elemsrch'] = get_ts()  

dd('init')
diag['ts_start'] = get_ts()
ts_start = get_ts()


filecap = 'loco-'+str(ts_start)+'.png'
dd('capture ' + filecap)

# set pytesseract path
pytesseract.pytesseract.tesseract_cmd = '/usr/local/Cellar/tesseract/3.05.01/bin/tesseract'

# capture screenshot on an Android device, pull it to the cwd
ret_capture = subprocess.call('/Users/carlyle/dev/adt/sdk/platform-tools/adb shell screencap -p /sdcard/' + filecap, shell=True)
ret_pull = subprocess.call('/Users/carlyle/dev/adt/sdk/platform-tools/adb pull /sdcard/' + filecap, shell=True)
diag['ts_acquireimg'] = get_ts()

# simple image to string
try:
  question = Image.open(filecap)
  width, height = question.size
  question = question.crop(
      (
          0,
          height - (0.9 * height),
          width,
          height
      )
  )
  question.save(filecap)
  diag['ts_crop'] = get_ts()
except:
  dd('failed to open screencap')

try:
  dd('ocr_begin')
  ocred = pytesseract.image_to_string(Image.open(filecap))
  diag['ts_ocr'] = get_ts()
  dd('ocr_end: '+ocred)

  results = ocred.split('\n')
  dd(max(results, key=len))

  results = results[:-3]
  # print(*results)

  search_query(''.join(results))
except:
	dd('failed to ocr screencap')


# clean up sdcard
ret_copy = subprocess.call('/Users/carlyle/dev/adt/sdk/platform-tools/adb shell rm /sdcard/' + filecap, shell=True)

ts_end = get_ts()
dd('completed in %d secs' % ((ts_end-ts_start)))
diag['ts_end'] = get_ts()

# print diagnostics
