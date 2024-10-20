import ollama
response = ollama.chat(model='llama3.2', messages=[
  {
    'role': 'user',
    'content': 'Can you read a menu and extract dish names, ingredients, prices, and any special notes such as allergens? Return the results in JSON format as an array of objects like this: [{"name": "Dish Name", "ingredients": "Ingredients", "price": "Price", "notes": "Notes"}]. Menu Text: Aloo Gobi $12.99 Fresh cauliflower and potatoes sauteed with ginger, tomatoes, and spices. Contains dairy.'
  },
])
print(response['message']['content'])