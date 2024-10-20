import os
import pytesseract
from PIL import Image
from flask import Flask, request, render_template, redirect, url_for
import openai
import json
import random
import ollama

use_local_llm = False 

app = Flask(__name__)

# 设置OpenAI的API密钥
openai.api_key = '<ChatGPT-API-key-here>'

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

    if use_local_llm:
        print("log: using local llama")

        response = ollama.chat(model='llama3.2', messages=[
            {
                "role": "user", "content": f"Analyze this menu text and extract dish names, ingredients, prices, and any special notes such as allergens. Return the results in JSON format as an array of objects like this: [{{\"name\": \"Dish Name\", \"ingredients\": \"Ingredients\", \"price\": \"Price\", \"notes\": \"Notes\"}}]. Menu Text: {ocr_text}"
            },
            ])

    else:
        print("log: using OpenAI API")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {
                    "role": "user", "content": f"Analyze this menu text and extract dish names, ingredients, prices, and any special notes such as allergens. Return the results in JSON format as an array of objects like this: [{{\"name\": \"Dish Name\", \"ingredients\": \"Ingredients\", \"price\": \"Price\", \"notes\": \"Notes\"}}]. Menu Text: {ocr_text}"
                }
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
    
    recommended_dishes = random.sample(dishes, 5)

    # 显示结果页面
    return render_template('results.html', dishes=dishes, recommended_dishes=recommended_dishes)

if __name__ == '__main__':
    # 创建上传文件夹
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
