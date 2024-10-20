import ollama
import json
import random
import os
import pytesseract
from PIL import Image

image_path = ('menu1.jpg')

img = Image.open(image_path)
ocr_text = pytesseract.image_to_string(img)

print(ocr_text)

response = ollama.chat(model='llama3.2', messages=[
  {
    'role': 'user',
    'content': f'Can you read a menu and extract dish names, ingredients, prices, and any special notes such as allergens? Return the results in JSON format as an array of objects like this: [{{"name": "Dish Name", "ingredients": "Ingredients", "price": "Price", "notes": "Notes"}}]. Menu Text: {ocr_text} Please note that the test menu is in Spanish and it is generated from OCR which contains missing letters or words. Please make sure to handle these cases.'
  },
])

print(response['message']['content'])