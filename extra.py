# File: extra.py
# Author: Xzgyo (GitHub: xzgyo)
# Create Date: 2024-06-20
# Last Modified: 2024-06-20
# Description: Extract specific column data from the first table in a MediaWiki text file.

import re
import sys

class TableExtractor:
  wiki_text = ''
  def __init__(self, wiki_text: str):
    self.wiki_text = wiki_text

  def get_specific_table_byIndex(self, index: int) -> str:
    # 匹配所有 {| 与 |} 之间的内容，包括该符号
    tables = re.findall(r'\{\|.*?\|\}', self.wiki_text, re.S)
    if not tables:
      # 长眼睛看清有没有表格
      sys.stderr.write("Error: No tables found in the provided MediaWiki text.\n")
      raise ValueError("Error: No tables found in the provided MediaWiki text.")
    elif index < 0 or index >= len(tables):
      # 长眼睛看清有多少表格
      sys.stderr.write(f"Error: Index {index} is out of range. This document only has {len(tables)} tables.\n")
      raise IndexError(f"Error: Index {index} is out of range. This document only has {len(tables)} tables.\n")
    return tables[index] if 0 <= index < len(tables) else ""
  
  def get_thead_index(self, thead_text: str, target_column: str):
    # 分隔表头行，提取列名
    headers = [h.strip() for h in re.split(r'[\s\n]*!+[\s]*', thead_text) if h.strip()]
    print(f"Headers: {headers}")
    # 没找到你提取你大坝
    target_index = headers.index(target_column) if target_column in headers else -1
    print(f"Index of '{target_column}': {target_index}")
    return target_index
  
  def extract_column_from_first_table(self, table_text: str, target_column: str) -> list[str]:
    tables = table_text.split('|-') # 分行
    first_table = tables[1 if tables[0].startswith('{|') else 0] # 表头
    target_index = self.get_thead_index(first_table, target_column) # 目标列索引
    if target_index == -1:
      # 没这玩意那你提取你大坝
      sys.stderr.write(f"Error: Column '{target_column}' not found in the first table.\n")
      return []
    print(f"Target index for column '{target_column}': {target_index}")
  
    table_data = []
    for i, row in enumerate(tables):
      if i <= tables.index(first_table):
        continue
      print(f"Processing row {i}")
      # 提取行数据
      cols = [c.strip() for c in re.split(r'[\s\n]*\|+[\s]*', row) if c.strip()]
      target_data = cols[target_index] if target_index < len(cols) else None
      print(f"Columns extracted: {target_data}")
      if target_data:
        table_data.append(target_data)
    return table_data
  
  def do_extract(self, table_index: int, target_column: str) -> list[str]:
    return self.extract_column_from_first_table(self.get_specific_table_byIndex(table_index), target_column)

if __name__ == "__main__":
  with open('/home/zhang/Desktop/qb-plugins/search-plugins.wiki/Unofficial-search-plugins.mediawiki', 'r', encoding='utf-8') as file:
    mediawiki_text = file.read()
    column_name = "Download link"
    extractor = TableExtractor(mediawiki_text)
    if len(sys.argv) < 3:
      print(f"Usage: {sys.argv[0]} <table_index> [column_name]")
      sys.exit(1)
    result = extractor.do_extract(int(sys.argv[1]), sys.argv[2])
    print(f"Extracted data for column '{column_name}': {result}")
    print(result)
