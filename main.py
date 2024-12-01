import os
from dotenv import load_dotenv
from parser import ParseWB

load_dotenv()


def main():
  input_csv = os.getenv("INPUT_CSV")
  
  if not input_csv:
    print("Не указаны входной или выходной CSV файл в переменных окружения.")
    return
  
  parser = ParseWB(input_csv)
  parser.parse()


if __name__ == "__main__":
  main()
