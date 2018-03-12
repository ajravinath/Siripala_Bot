import telepot
from telepot.loop import MessageLoop
from pprint import pprint
import time
import json
import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

bot = telepot.Bot('532527602:AAGVVkqBX-M-KwR6ZKD9LGqRpEMHzrVK3H0')
bot.getMe()

num = {'tech' : 0,
        'world' : 0,
        'sports' : 0,
        'business': 0,
        'buzzfeed' : 0,
        'entertainment':0
        }



def news(type_):
    def xstr(s):
        if s is None:
            return ''
        return str(s)

    dictType ={'tech' : 'techcrunch',
                'world' : 'bbc-news',
                'sports' : 'espn',
                'business': 'business-insider-uk',
                'buzzfeed' : 'buzzfeed',
               'entertainment':'entertainment-weekly'
                }
    urlTech = "https://newsapi.org/v1/articles?source="+dictType[type_]+"&apiKey=3662495ebb4d4f1ba3a1f264746f605f"

    art = urllib.request.urlopen(urlTech).read()
    obj = json.loads(art.decode('utf-8'))

    dict = {}
    j = 0
    for i in obj['articles']:
        dict[j] = {
                    'title' : i['title'],
                    'description' : i['description'],
                    'url' : i['url']
                    }
        j=j+1
    
    news_line =""
    global num 
    if(num[type_] < j):
        news_line = "*"+xstr(dict[num[type_]]['title'])+"* \n"+xstr(dict[num[type_]]['description'])+"\n"+xstr(dict[num[type_]]['url'])
        num[type_] =num[type_]+1
    else:
        news_line= "thats all folks"

    return news_line


def handle_command(command, chat_id,user):
    global bot
    commands ={"tech news" : news("tech"),
               "world news" : news("world"),
               "sports news" : news("sports"),
               "business news" : news("business"),
               "buzzfeed" : news("buzzfeed"),
               "entertainment news" : news("entertainment"),
               "hi" : "Hello @{}".format(user),
               "hello" : "Hi @{}".format(user),
               "who are you" : "I'm *Demon Rapiddeath* aka `rapidsdemon`,\n I was made by master *rapiddeath* at his homelab."
                }
    response = "ඔච්චර දේවල් තේරෙන්නේ නෑ ඔයි මට @{}. දන්න දෙයක් අහපං *".format(user) + (', '.join(commands.keys())) + \
               "* වගේ දේවල් "

    if("news" in str(command.lower()) or  "buzzfeed" in str(command.lower())):
            print(command.lower(),"inside this")
            bot.sendMessage(chat_id, "පොඩ්ඩක් ඉඳපන් කොල්ලෝ ...")
            
            
    gen = (comm_key for comm_key in commands.keys() if comm_key in command.lower())
    for comm_key in gen:
        print(command.lower())
        response = commands[comm_key]

    bot.sendMessage(chat_id, response)

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    # try:
    pprint(msg['text'])
    if ((msg['chat']).get('type')=='group'):
        if '@Siripala_Bot' in msg['text']:
            print(content_type, chat_type, chat_id)

            if content_type == 'text':
                handle_command(msg['text'], chat_id, ((msg['from']).get('first_name')))
                # bot.sendMessage(chat_id, "Hi")
    else:
        if content_type == 'text':
            handle_command(msg['text'], chat_id, ((msg['from']).get('first_name')))
                # bot.sendMessage(chat_id, "Hi")
    # except:
    #     print("in pass")
    #     pass

MessageLoop(bot,handle).run_as_thread()

