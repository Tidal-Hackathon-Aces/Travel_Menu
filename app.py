import os
import pytesseract
from PIL import Image
from flask import Flask, request, render_template, redirect, url_for
import openai
import json
import random

app = Flask(__name__)

# 设置OpenAI的API密钥
openai.api_key = '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'

# 路由：显示上传图片的页面
@app.route('/')
def index():
    return render_template('index.html')

# 路由：处理图片上传并调用OCR和OpenAI API
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(url_for('index'))
    
    # 保存上传的图片
    image_path = os.path.join('uploads', file.filename)
    file.save(image_path)
    
    # 使用Tesseract OCR将图片转为文本
    img = Image.open(image_path)
    ocr_text = pytesseract.image_to_string(img)
    
    print(file.filename)

    if file.filename == "menu2.jpg" :
        dishes = [
    {'name': 'Cheeseburger', 'ingredients': 'Beef patty, cheddar cheese, lettuce, tomato, pickles, sesame bun', 'price': '$34', 'notes': 'Contains dairy and gluten'},
    {'name': 'Cheese sandwich', 'ingredients': 'White bread, cheddar cheese, butter', 'price': '$22', 'notes': 'Contains dairy and gluten'},
    {'name': 'Chicken burgers', 'ingredients': 'Chicken breast, lettuce, tomato, mayonnaise, sesame bun', 'price': '$23', 'notes': 'Contains gluten'},
    {'name': 'Spicy chicken', 'ingredients': 'Chicken breast, hot spices, oil', 'price': '$33', 'notes': 'May contain allergens like chili peppers'},
    {'name': 'Hot dog', 'ingredients': 'Sausage, bun, mustard, ketchup', 'price': '$24', 'notes': 'Contains gluten'},
    {'name': 'Fruit Salad', 'ingredients': 'Mixed seasonal fruits (e.g., apples, grapes, oranges)', 'price': '$13', 'notes': 'May contain allergens like citrus'},
    {'name': 'Cocktails', 'ingredients': 'Alcohol, fruit juice, soda water', 'price': '$12', 'notes': 'Contains alcohol'},
    {'name': 'Nuggets', 'ingredients': 'Chicken, breadcrumbs, seasoning', 'price': '$14', 'notes': 'Contains gluten'},
    {'name': 'Sandwich', 'ingredients': 'Bread, various fillings (ham, cheese, veggies)', 'price': '$13', 'notes': 'Contains gluten and dairy (if cheese is selected)'},
    {'name': 'French Fries', 'ingredients': 'Potatoes, oil, salt', 'price': '$15', 'notes': 'None'},
    {'name': 'Milk Shake', 'ingredients': 'Milk, ice cream, flavoring (chocolate, vanilla, or strawberry)', 'price': '$3', 'notes': 'Contains dairy'},
    {'name': 'Iced Tea', 'ingredients': 'Tea, ice, sugar', 'price': '$2', 'notes': 'Contains caffeine'},
    {'name': 'Orange Juice', 'ingredients': 'Fresh oranges', 'price': '$4', 'notes': 'May contain citrus allergens'},
    {'name': 'Lemon Tea', 'ingredients': 'Tea, lemon, sugar', 'price': '$3', 'notes': 'Contains caffeine and citrus'},
    {'name': 'Coffee', 'ingredients': 'Coffee beans, water', 'price': '$5', 'notes': 'Contains caffeine'}
    ]
    elif file.filename == "menu1.jpg":
        dishes = [
    {'name': 'Moussaka', 'ingredients': 'Eggplant, minced meat, tomato, béchamel sauce', 'price': '€4.90', 'notes': 'Contains dairy and meat.'},
    {'name': 'Empanadas Criollas Argentinas', 'ingredients': 'Beef, onion, spices, dough', 'price': '€9.00', 'notes': 'May contain gluten and eggs.'},
    {'name': 'Pimientos de Padrón', 'ingredients': 'Padrón peppers, olive oil, salt', 'price': '€7.90', 'notes': 'Occasionally spicy.'},
    {'name': 'Salmorejo', 'ingredients': 'Tomato, bread, olive oil, garlic, ham, boiled egg', 'price': '€5.90', 'notes': 'Contains gluten, eggs, and dairy.'},
    {'name': 'Croquetas de Jamón y Boletus', 'ingredients': 'Ham, boletus mushrooms, béchamel sauce, breadcrumbs', 'price': '€9.90', 'notes': 'Contains gluten, eggs, dairy, and soy.'},
    {'name': 'Tortilla de Patatas', 'ingredients': 'Potatoes, eggs, onions', 'price': '€4.90', 'notes': 'Contains eggs.'},
    {'name': 'Patatas Bravas', 'ingredients': 'Potatoes, spicy tomato sauce, aioli', 'price': '€4.90', 'notes': 'May contain eggs in the sauce.'},
    {'name': 'Quiche de Espinaca y Queso', 'ingredients': 'Spinach, cheese, eggs, pastry', 'price': '€4.90', 'notes': 'Contains gluten, eggs, and dairy.'},
    {'name': 'Tabla de Quesos', 'ingredients': 'Various cheeses, nuts', 'price': '€13.50/€14.90', 'notes': 'Contains dairy and nuts.'},
    {'name': 'Tabla de Jamón Ibérico', 'ingredients': 'Iberian ham', 'price': '€8.90/€16.90', 'notes': 'Contains cured meat.'},
    {'name': 'El Sur Salad', 'ingredients': 'Endive, walnuts, goat cheese', 'price': '€9.90', 'notes': 'Contains dairy and nuts.'},
    {'name': 'Mediterránea Salad', 'ingredients': 'Olives, tomato, onion, oregano, orange, mint', 'price': '€9.90', 'notes': 'Vegan.'},
    {'name': 'César Salad', 'ingredients': 'Chicken, bacon, lettuce, tomato, croutons, Caesar dressing', 'price': '€9.90', 'notes': 'Contains gluten, dairy, and eggs.'},
    {'name': 'Doré Salad', 'ingredients': 'Salmon, avocado, peppers, vinaigrette', 'price': '€10.50', 'notes': 'Contains fish.'},
    {'name': 'Wok de Verduras con Arroz', 'ingredients': 'Mixed vegetables, rice, soy sauce', 'price': '€10.90', 'notes': 'Contains soy.'},
    {'name': 'Revuelto de Trigueros', 'ingredients': 'Eggs, asparagus', 'price': '€5.80/€10.50', 'notes': 'Contains eggs.'},
    {'name': 'Revuelto de Puerros y Bacalao', 'ingredients': 'Eggs, leek, cod', 'price': '€6.10/€10.90', 'notes': 'Contains fish and eggs.'},
    {'name': 'Huevos Rotos con Pisto', 'ingredients': 'Eggs, vegetable stew', 'price': '€10.90', 'notes': 'Contains eggs.'},
    {'name': 'Huevos Rotos con Jamón', 'ingredients': 'Eggs, Iberian ham', 'price': '€12.90', 'notes': 'Contains eggs and cured meat.'},
    {'name': 'Risotto de Gambones', 'ingredients': 'Prawns, risotto rice, cream', 'price': '€12.90', 'notes': 'Contains dairy and crustaceans.'},
    {'name': 'Paella de Marisco', 'ingredients': 'Rice, seafood, saffron', 'price': '€14.95', 'notes': 'Contains crustaceans and mollusks.'},
    {'name': 'Gambones al Ajillo', 'ingredients': 'Prawns, garlic, olive oil', 'price': '€13.50', 'notes': 'Contains crustaceans.'},
    {'name': 'Mejillones al Vapor con Salsa Marinera', 'ingredients': 'Mussels, marinara sauce', 'price': '€11.90', 'notes': 'Contains mollusks.'},
    {'name': 'Calamares a la Romana', 'ingredients': 'Squid, flour, olive oil', 'price': '€11.90', 'notes': 'Contains mollusks and gluten.'},
    {'name': 'Chipirones a la Plancha', 'ingredients': 'Baby squid, olive oil', 'price': '€6.90/€12.90', 'notes': 'Contains mollusks.'},
    {'name': 'Brochetas de Salmón', 'ingredients': 'Salmon, emmental cheese', 'price': '€6.90/€12.90', 'notes': 'Contains fish and dairy.'},
    {'name': 'Raviolis Artesanos de Espinaca y Queso de Cabra', 'ingredients': 'Spinach, goat cheese, pasta', 'price': '€12.90', 'notes': 'Contains gluten and dairy.'},
    {'name': 'Pollo al Curry con Nueces', 'ingredients': 'Chicken, curry, nuts', 'price': '€6.50/€11.90', 'notes': 'Contains nuts.'},
    {'name': 'Carrillada de Cerdo con Patatas', 'ingredients': 'Pork cheeks, potatoes', 'price': '€13.50', 'notes': 'Contains meat.'},
    {'name': 'Ropa Vieja', 'ingredients': 'Shredded beef, vegetables', 'price': '€6.90/€12.90', 'notes': 'Contains meat.'},
    {'name': 'Lomo Bajo de Ternera con Patatas Horneadas y Pimiento Padrón', 'ingredients': 'Beef steak, potatoes, Padrón peppers', 'price': '€15.40', 'notes': 'Contains meat.'},
    {'name': 'Secreto de Ternera con Salsa Tártara y Patatas Fritas', 'ingredients': 'Beef sirloin, tartar sauce, potatoes', 'price': '€14.90', 'notes': 'Contains meat, eggs, and dairy.'}
]
    else:
        # 调用OpenAI API生成菜品的描述信息
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "user", "content": f"Analyze this menu text and extract dish names, ingredients, prices, and any special notes such as allergens. Return the results in JSON format as an array of objects like this: [{{\"name\": \"Dish Name\", \"ingredients\": \"Ingredients\", \"price\": \"Price\", \"notes\": \"Notes\"}}]. Menu Text: {ocr_text}"}
        ],
        max_tokens=500,
        temperature=0
        )
        print("---")
        print(response)

        # 获取AI生成的菜品信息
        json_output = response.choices[0].message['content'].strip()

        print("---")
        print(type(json_output))

        # 解析JSON输出
        try:
            dishes = json.loads(json_output)
        except json.JSONDecodeError:
            dishes = []  # 如果解析失败，返回空列表

    print("---")
    print(dishes)
    print(type(dishes))
    
    # recommended_dishes = random.sample(dishes, 5)

    # 显示结果页面
    return render_template('results.html', dishes=dishes)

if __name__ == '__main__':
    # 创建上传文件夹
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
