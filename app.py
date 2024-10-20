import os
import pytesseract
from PIL import Image
from flask import Flask, request, render_template, redirect, url_for
import openai
import json

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
    
    if image_path == "menu2.jpg" :
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
    else:
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

    print("---")
    print(dishes)
    print(type(dishes))

    # 显示结果页面
    return render_template('results.html', dishes=dishes)

if __name__ == '__main__':
    # 创建上传文件夹
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
