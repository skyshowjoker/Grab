import time

from appoinment import USTCGymAppointment
from apscheduler.schedulers.background import BackgroundScheduler
import threading
import time

def my_task():

    phone_number = '17396245416'
    activity = '华体汇'
    bot = USTCGymAppointment(phone_number)
    bot.appointment(activity)





def worker():
    print("子线程启动")
    time.sleep(3)  # 模拟工作一段时间
    print("子线程结束")


def monitor_thread():
    # 初次启动子线程
    stop_event = threading.Event()
    t = threading.Thread(target=my_task)
    t.start()
    start_time = time.time()
    while True:
        # 如果子线程已经结束，启动新的子线程
        if not t.is_alive():
            print("检测到子线程停止，启动新子线程...")
            t = threading.Thread(target=my_task)
            t.start()

        # 等待一段时间后再检查
        time.sleep(5)
        elapsed_time = time.time() - start_time
        if elapsed_time > 3 * 36:
            print("线程超过3小时，自动停止")
            stop_event.set()
            break

def scheduler():
    # 创建后台调度器
    scheduler = BackgroundScheduler()

    # 添加任务：每周六早上8点执行
    scheduler.add_job(monitor_thread, 'cron', day_of_week='sat', hour=12, minute=13)
    scheduler.add_job(monitor_thread, 'cron', day_of_week='sat', hour=8, minute=0)

    # 开始调度
    scheduler.start()

    print("调度器已启动，每周六早上8点执行任务。")

    try:
        # 保持主线程运行
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # 关闭调度器
        scheduler.shutdown()
        print("调度器已关闭。")

if __name__ == '__main__':
    scheduler()

