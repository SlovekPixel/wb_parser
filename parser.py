import csv
import requests
from classes import Items, Feedback


class ParseWB:
  def __init__(self, input_csv: str):
    self.input_csv = input_csv
  
  @staticmethod
  def __is_valid_article(article: str) -> bool:
    return article.isdigit()
  
  def parse(self):
    with open(self.input_csv, mode="r", encoding="utf-8") as infile:
      reader = csv.reader(infile)
      articles = [row[0] for row in reader]
    
    _page = 1
    self.__create_csv()
    
    for article in articles:
      if not self.__is_valid_article(article):
        print(f"Неверный артикул: {article}.")
        continue
      
      product_url = f"https://www.wildberries.ru/catalog/{article}/detail.aspx"
      response = requests.get(
        f'https://card.wb.ru/cards/v1/detail?dest=-2228342&nm={article}')
      items_info = Items.model_validate(response.json()["data"])
      if items_info.products:
        self.__get_images(items_info)
        self.__feedback(items_info)
        self.__save_csv(items_info)
  
  @staticmethod
  def __create_csv():
    with open("wb_data.csv", mode="w", newline="", encoding="utf-8") as file:
      writer = csv.writer(file, delimiter=';')
      writer.writerow(
        ['id', 'Название', 'Цена', 'Бренд', 'Скидка', 'Рейтинг', 'В наличии', 'id-продавец', 'Изображения', "Рейтинг"])
  
  @staticmethod
  def __save_csv(items: Items):
    with open("wb_data.csv", mode="a", newline="", encoding="utf-8") as file:
      writer = csv.writer(file, delimiter=';')
      for product in items.products:
        writer.writerow([product.id,
                         product.name,
                         product.salePriceU,
                         product.brand,
                         product.sale,
                         product.rating,
                         product.volume,
                         product.supplierId,
                         f"[{','.join(product.image_links)}]",
                         product.valuation
                         ])
  
  @staticmethod
  def __get_images(item_model: Items):
    for product in item_model.products:
      _short_id = product.id // 100000
      if 0 <= _short_id <= 143:
        basket = '01'
      elif 144 <= _short_id <= 287:
        basket = '02'
      elif 288 <= _short_id <= 431:
        basket = '03'
      elif 432 <= _short_id <= 719:
        basket = '04'
      elif 720 <= _short_id <= 1007:
        basket = '05'
      elif 1008 <= _short_id <= 1061:
        basket = '06'
      elif 1062 <= _short_id <= 1115:
        basket = '07'
      elif 1116 <= _short_id <= 1169:
        basket = '08'
      elif 1170 <= _short_id <= 1313:
        basket = '09'
      elif 1314 <= _short_id <= 1601:
        basket = '10'
      elif 1602 <= _short_id <= 1655:
        basket = '11'
      elif 1656 <= _short_id <= 1919:
        basket = '12'
      elif 1920 <= _short_id <= 2045:
        basket = '13'
      elif 2046 <= _short_id <= 2189:
        basket = '14'
      elif 2190 <= _short_id <= 2405:
        basket = '15'
      else:
        basket = '16'
      
      product.image_links = [
        f"https://basket-{basket}.wbbasket.ru/vol{_short_id}/part{product.id // 1000}/{product.id}/images/big/{i}.webp"
        for i in range(1, product.pics + 1)
      ]
  
  @staticmethod
  def __feedback(item_model: Items):
    for product in item_model.products:
      url = f"https://feedbacks1.wb.ru/feedbacks/v1/{product.root}"
      res = requests.get(url=url)
      if res.status_code == 200:
        feedback = Feedback.model_validate(res.json())
        product.feedback_count = feedback.feedbackCountWithText
        product.valuation = feedback.valuation
