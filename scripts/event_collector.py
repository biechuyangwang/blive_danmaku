from bilibili_api import sync
from bilibili_api.live import LiveDanmaku
from requests import post
import json
import time
import os

from pychatgpt import Chat


def check_and_create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def send_dm(room: int, msg: str, csrf: str, sessdata: str):
    payload = post(
        url='https://api.live.bilibili.com/msg/send',
        params={
            'msg': msg,
            'rnd': int(time.time()),
            'color': 16777215,
            'fontsize': 25,
            'mode': 1,
            'roomid': room,
            'bubble': 0,
            'csrf': csrf,
            'csrf_token': csrf
        },
        cookies={
            'SESSDATA': sessdata,
            'bili_jct': csrf
        }
    )
    # print(payload.json())

if __name__ == '__main__':
    chat = Chat(email="biechuyangwang@gmail.com", password="li123456")

    room_id = 21696079
    csrf = '81d5e90be7bc4fec56feac9e42929dfa'
    sessdata = '0cd85d58%2C1685932358%2Ca3e89%2Ac2'
    reply_room_id = 21696079

    while room_id==0:
        try:
            room_id = int(input('请输入房间号码:'))
        except ValueError:
            print('格式错误!')
            continue
        except KeyboardInterrupt:
            exit(0)
        break
    stream = LiveDanmaku(room_display_id=room_id)
    room_path = os.path.join('../output', str(room_id))

    @stream.on('ALL')
    async def on_all_event(event):
        event_type = event["type"]
        # print(f'接收到事件: {event_type}')
        # file_path = os.path.join(room_path, event_type)
        # file_name = f"{event_type}_{time.strftime('%Y%m%d_%H%M%S', time.localtime())}.json5"
        if event_type == "DANMU_MSG":
            msg = event['data']['info'][1]
            print(f"[{event['room_real_id']}][{time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime())}]{event['data']['info'][2][1]}:{msg}")
            if "小六" in msg[:4]:
                msg = msg[2:]
                # print(msg)
                res = chat.ask(msg)
                send_dm(reply_room_id, res[:21], csrf, sessdata)
                print(f"[{event['room_real_id']}][{time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime())}]小六:{res}")
        # try:
        #     check_and_create_folder(file_path)
        #     with open(os.path.join(file_path, file_name).replace('\\', '/'), 'w', encoding='utf8') as f:
        #         print('已保存至', f.name)
        #         json.dump(event, f, indent=4, ensure_ascii=False)
        #         print(f"{event['data']['info'][2][1]}:{event['data']['info'][1]}")
        # except KeyboardInterrupt:
        #     pass

    try:
        sync(stream.connect())
    except KeyboardInterrupt:
        exit(0)
