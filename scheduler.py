import os
from ocr import recognize_text_to_record_list, image_to_position, recognize_text, preprocess
import warnings
import config
import random
import asyncio
from report.report_damage import report_damage


async def record_task():
    screenshot_path = 'screenshots/screen.png'
    connect()
    if config.DO_REFRESH_DATA:
        await refresh_data(['back_button', 'gild_battle', 'expand_button'])
    screenshot(screenshot_path)
    record_list = recognize_text_to_record_list(screenshot_path)
    for record in record_list:
        report_damage(record)


async def refresh_data(images: list):
    screenshot_path = 'screenshots/screen.png'
    for image in images:
        screenshot(screenshot_path)
        center = image_to_position(image)
        if center is not None:
            click(center[0], center[1])
            await asyncio.sleep(2)
        else:
            await game_error_handling()
            # 出错。可能是由于：1. 号被顶下去了 2. 日期变更


async def game_error_handling():
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
    if center is None:
        warnings.warn('无法解决游戏问题，请检查模拟器')
        return
    click(center[0], center[1])
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
    await refresh_data(images)
    # 现在应该回到了公会战界面，结束


def click(x, y):
    os.system('adb shell input tap %s %s' % (x, y))


def connect():
    try:
        os.system('adb connect 127.0.0.1:7555')
    except:
        warnings.warn("无法连接到模拟器，请检查模拟器是否正常运作。")


def screenshot(relative_path: str):
    path = os.path.abspath('.') + '/' + relative_path
    os.system('adb shell screencap /data/screen.png')
    os.system('adb pull /data/screen.png %s' % path)


# if __name__ == '__main__':
    # if not os.path.isfile('main.db'):
    #     init.init_database()