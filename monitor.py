#!/usr/bin/python3
# .,__,.........,__,.....╭¬¬¬¬¬━━╮
# `•.,¸,.•*¯`•.,¸,.•*|:¬¬¬¬¬¬::::|:^--------^
# `•.,¸,.•*¯`•.,¸,.•*|:¬¬¬¬¬¬::::||｡◕‿‿◕｡|
# -........--""-.......--"╰O━━━━O╯╰--O-O--╯
# v 0.0.1

import requests
import json
import os
import telepot
import time
from telepot.loop import MessageLoop
import threading

TELEGRAM_TOKEN = ""

class WebSite:

   def __init__(self, url, tag_string):
      self.url = url
      self.tag_string = tag_string

   def download_website(self):
      headers = {
         'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0'
      }
      return requests.get(self.url, headers=headers).text

   def low_price_string(self, complete_html):
      try:
         start = complete_html.index(self.tag_string[0]) + len(self.tag_string[0])
         end = complete_html.index(self.tag_string[1], start)
         return complete_html[start:end]
      except ValueError:
         return ""

   def check_price(self):
      price = float(self.low_price_string(self.download_website()))
      if os.path.exists('price.json'):
         old_price = json.load(open('price.json', 'r'))
         if price < old_price['price']:
            self.save_price(price)
            return price
      else:
         self.save_price(price)
         return price

   def save_price(self, price):
      data = {
         'price': float(price)
      }
      with open('price.json', 'w') as write_file:
         json.dump(data, write_file)

def main():
   string = ["(€ ", ")"]

   def set_interval(func, sec, param_1, param_2):
      def func_wrapper():
         set_interval(func, sec, param_1, param_2)
         func(param_1, param_2)

      t = threading.Timer(sec, func_wrapper)
      t.start()
      return t

   def handle(msg):
      content_type, chat_type, chat_id = telepot.glance(msg)
      if content_type == 'text':
         set_interval(check, 20, msg['text'], chat_id)
         check(msg['text'], chat_id)

   def check(msg, chat_id):
      booking = WebSite(msg, string)
      new_price = booking.check_price()
      if new_price is not None:
         bot.sendMessage(chat_id, 'structure price ' + str(new_price))

   bot = telepot.Bot(TELEGRAM_TOKEN)
   MessageLoop(bot, handle).run_as_thread()

   while 1:
      time.sleep(10)

if __name__ == "__main__":
   main()
