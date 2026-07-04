
# File: main.py
# Author: Xzgyo (GitHub: xzgyo)
# Create Date: 2024-06-20
# Last Modified: 2024-06-20
# Description: Main script to extract specific column data from a MediaWiki text file and download files

import os
import re
import requests
from extra import TableExtractor

def download(url) -> str:
  response = requests.get(url)
  if response.status_code == 200:
    return response.text
  else:
    raise Exception(f"Failed to download the file. Status code: {response.status_code}")

if __name__ == "__main__":
  # git clone https://github.com/qbittorrent/search-plugins.wiki.git
  # cd search-plugins.wiki
  file_content = ""
  with open('/home/zhang/Desktop/qb-plugins/search-plugins.wiki/Unofficial-search-plugins.mediawiki', 'r', encoding='utf-8') as file:
    file_content = file.read()
  extractor = TableExtractor(file_content)
  table_index = 0
  extracted_data = extractor.do_extract(table_index, "Download link")
  print(f"Extracted data from table {table_index}: {extracted_data}")
  links = [re.findall(r'\[(.*?)\[', link, re.S)[0].strip() for link in extracted_data]
  print(f"Extracted links: {links}")
  for link in links:
    os.system(f"wget -c '{link}' -P ./downloads")