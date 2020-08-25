import os
from ocr import recognize_text_to_record_list, image_to_position, recognize_text, preprocess
import warnings
import random
import asyncio
from report.report_damage import report_damage
from do_fetch import stop_fetch


async def record_task(header: dict):
    screenshot_path = 'screenshots/screen.png'
    connect()
    await refresh_data(['back_button', 'gild_battle', 'expand_button'], header=header)
    screenshot(screenshot_path)
    record_list = recognize_text_to_record_list(screenshot_path)
    for record in reversed(record_list):
        report_damage(record, auth_header=header)


async def refresh_data(images: list, header: dict):
    screenshot_path = 'screenshots/screen.png'
    for image in images:
        screenshot(screenshot_path)
        center = image_to_position(image)
        if center is not None:
            click(center[0], center[1])
            await asyncio.sleep(2)
        else:
            await game_error_handling(header=header)
            return
            # 出错。可能是由于：1. 号被顶下去了 2. 日期变更


async def game_error_handling(header: dict):
    screenshot_path = 'screenshots/screen.png'
    preprocess(screenshot_path, (0.25, 0.25, 0.75, 0.75))
    error_text = recognize_text('output.png').replace(' ', '')
    print(error_text)
    button_image = 'back_to_title'
    if '日期已变更' in error_text:
        button_image = 'date_change_ok_button'
    elif '连接中断' in error_text or '回到标题界面' in error_text:
        button_image = 'back_to_title'
    center = image_to_position(button_image)
    if center is not None:
        click(center[0], center[1])
        if button_image == 'back_to_title':
            stop_fetch(header=header)  # 如果被顶下来了，则停止抓取，等待重新开始
            return
    await asyncio.sleep(5)
    # 现在应该回到了标题画面
    button_image = 'adventure_button'
    center = None
    while center is None:
        click(random.randint(0, 100), random.randint(0, 100))
        await asyncio.sleep(5)
        screenshot(screenshot_path)
        center = image_to_position(button_image)
    # 现在应该在主界面
    click(center[0], center[1])
    # 现在应该在冒险界面
    images = ['gild_battle', 'expand_button']
    await refresh_data(images, header)
    # 现在应该回到了公会战界面，结束


def click(x, y):
    os.system('adb shell input tap %s %s' % (x, y))


def swipe(x1, y1, x2, y2):
    os.system('adb shell input swipe %s %s %s %s' % (x1, y1, x2, y2))


def connect():
    try:
        os.system('adb connect 127.0.0.1:62001')
    except:
        warnings.warn("无法连接到模拟器，请检查模拟器是否正常运作。")


def screenshot(relative_path: str):
    path = os.path.abspath('.') + '/' + relative_path
    os.system('adb -s 127.0.0.1:62001 shell screencap /data/screen.png')
    os.system('adb -s 127.0.0.1:62001 pull /data/screen.png "%s"' % path)


# if __name__ == '__main__':
    # if not os.path.isfile('main.db'):
    #     init.init_database()
