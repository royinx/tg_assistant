import os 
import time
import subprocess
import requests
import telebot

BOT_TOKEN = input("\nToken: ")
tb = telebot.TeleBot(BOT_TOKEN)	#create a new Telegram Bot object

# tb.infinity_polling(interval=0, timeout=20)

user = tb.get_me()
print(f"\n===== Login as bot: {user.username} =====\n")

updates = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates").json()['result']
# import json
# print(json.dumps(updates))

def get_chat_id(all_msg: list):
    chat_ids = {}
    for msg in all_msg:
        try:
            del msg["update_id"]
            msg = list(msg.values())[0]
            id = msg["chat"]["id"]
            channel_name = msg["chat"]["title"]
            chat_ids[channel_name] = id
        except:
            print("If your chatroom not shown, Please send out sth.\n")
    return chat_ids

# list chatroom
chat_ids = get_chat_id(updates)
for sel, (k, v) in enumerate(chat_ids.items()):
    print(f"{sel+1}.  {k}")

sel = int(input(f"\nChoose the Chatroom you want to post: ")) - 1
chat_id = list(chat_ids.values())[sel]

print()
support_func = {"doc": tb.send_document,
                "text": tb.send_message,
                "image": tb.send_photo,
                "video": tb.send_video,
                "video_note": tb.send_video_note}
for sel, (k,v) in enumerate(support_func.items()):
    print(f"{sel+1}.  {k}")
print()
action_type = input(f"Choose the msg type: {list(range(1,6))}: ")
try:
    action_type = int(action_type)
    if action_type not in range(1,len(support_func)+1):
        print(f'function not support yet, your input is "{action_type}"')
        exit()
    send_func = list(support_func.values())[action_type-1]
except:
    if action_type not in support_func.keys():
        print(f'function not support yet, your input is "{action_type}"')
        exit()
    send_func = support_func[action_type]

def check_file_size(file):
    if os.path.getsize(file)>>20 < 50:
        return [file]
    else:
        cmd = f"split --bytes=50MB {file} {file}_"
        with subprocess.Popen(cmd , shell = True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL):
            time.sleep(0.5) # wait for process return
        file_list = os.listdir()
        file_list = [file_ for file_ in file_list if file_.startswith(f"{file}_")]
        return file_list

# print(send_func)
if send_func == tb.send_message:
    msg = input(f"\nInput message: ")
else:
    file = input(f"\nFile location: ")
    files = check_file_size(file)

for file_ in files:
    msg = open(file_, 'rb')
    send_func(chat_id, msg)
    os.remove(file_)

if len(files)>1:
    tb.send_message(chat_id, f"\nPlease run the following command and join the files together.\ncat {file}_* > {file}")


"""
# getFile
# Downloading a file is straightforward
# Returns a File object
import requests
file_info = tb.get_file(file_id)

file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(API_TOKEN, file_info.file_path))
"""

# docker run --rm -it -v ${PWD}:/py -w /py python:3.8 bash
# pip3 install telebot
# python3 main.py