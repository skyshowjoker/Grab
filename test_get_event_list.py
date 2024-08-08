from appoinment import USTCGymAppointment


if __name__ == '__main__':
    phone_number = '17396245416'
    bot = USTCGymAppointment(phone_number)
    bot.test_get_event_list()