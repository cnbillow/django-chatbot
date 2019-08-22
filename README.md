# django_chatbot
django_chatbot是chatbot-py的django封装版本，chatbot-py是中文聊天机器人， 支持上下文管理，动态的函数调用，
可以根据自己的语料训练出自己想要的聊天机器人，可以用于智能客服、在线问答、智能聊天等场景!

# 快速开始
**1. 安装**
```
git clone https://github.com/lin423497786/django_chatbot
cd django_chatbot
pip install -r requirements.txt
```

**2. 启动django服务**
```
python manage.py runserver 80
```

**3. 静态语料学习**
静态语料：不需要调用函数或接口的语料
```
import requests


post_data = {
    'question': '早上吃鸡蛋对身体好吗?',
    'answer': '早餐当中吃鸡蛋，的确是对身体有很大的益处',
}

headers = {
    'Content-Type': 'application/json',
    'Accept': '*/*',
}

# post
requests.post('http://127.0.0.1/api/chatbot/learn/', json=post_data, headers=headers)
```

**4. 动态语料学习**
动态语料：需要调用函数或接口的语料
这里以天气查询为例子，首先先定义一个函数，这里使用chatbot.ext.integrate_weather_gaode.get_weather函数
```
import requests


post_data = {
    'question': '天气查询',   # 问题
    'answer': 'chatbot.ext.integrate_weather_gaode.get_weather',  # 回答，这里要填函数的绝对路径
    'category': '天气',        # 分类，可以随便填，不填也行
    'type_': 1                # 固定值1，所有动态的问题该值都是1
}

headers = {
    'Content-Type': 'application/json',
    'Accept': '*/*',
}

# post
requests.post('http://127.0.0.1/api/chatbot/learn/', json=post_data, headers=headers)
```
**5. 提问**
学习完后就可以向机器人提出问题， 这里以步骤4学习的“天气查询”进行提问，因为“天气查询”调用的是chatbot.ext.integrate_weather_gaode.get_weather
函数，该函数有2个参数，程序会一一识别出来，并一个个询问，但所有参数都询问完后程序就会调用该函数，将该函数的返回值作为回复，如下所示。
```
import requests


session = requests.session()

# 第一轮询问
response = session.post('http://127.0.0.1/api/chatbot/question/', json={'question': '天气查询'})
print(response.text)

# 第二轮询问
response = session.post('http://127.0.0.1/api/chatbot/question/', json={'question': '南京'})
print(response.text)

# 第三轮询问
response = session.post('http://127.0.0.1/api/chatbot/question/', json={'question': '20190822'})
print(response.text)
```

# 效果图
这是集成到微信公众号后的效果图
![](你刚复制的图片路径)