from appoinment import USTCGymAppointment

from apscheduler.schedulers.background import BackgroundScheduler
import time

def my_task():

    phone_number = '17396245416'
    activity = '华体汇'
    bot = USTCGymAppointment(phone_number)
    bot.appointment(activity)




if __name__ == '__main__':

    # 创建后台调度器
    scheduler = BackgroundScheduler()

    # 添加任务：每周六早上8点执行
    scheduler.add_job(my_task, 'cron', day_of_week='sat', hour=22, minute=24)
    # scheduler.add_job(my_task, 'cron', day_of_week='sat', hour=8, minute=0)


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