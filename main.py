from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 初始化WebDriver
driver = webdriver.Chrome()

# 打开微信小程序活动报名页面
driver.get('https://ichangtou.zhidieyun.com/api/event/joinCancelEvent')  # 替换为实际的活动报名页面URL

try:
    # 等待页面加载并查找报名按钮
    wait = WebDriverWait(driver, 10)
    signup_button = wait.until(EC.element_to_be_clickable((By.ID, 'signup_button_id')))  # 替换为实际的按钮ID

    # 点击报名按钮
    signup_button.click()

    # 等待并填写报名表单
    name_field = wait.until(EC.presence_of_element_located((By.ID, 'name_field_id')))  # 替换为实际的字段ID
    name_field.send_keys('Your Name')

    email_field = driver.find_element(By.ID, 'email_field_id')  # 替换为实际的字段ID
    email_field.send_keys('your.email@example.com')

    # 继续填写其他必要的信息
    # ...

    # 提交表单
    submit_button = driver.find_element(By.ID, 'submit_button_id')  # 替换为实际的按钮ID
    submit_button.click()

    print('报名成功！')

except Exception as e:
    print(f'出现错误: {e}')

finally:
    # 关闭浏览器
    driver.quit()
