import smtplib
import os
import logging
from email.mime.text import MIMEText
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

def send_email(subject, content):
    sender_email = os.getenv('EMAIL_SENDER')
    sender_password = os.getenv('EMAIL_PASSWORD')
    receiver_email = os.getenv('EMAIL_RECEIVER')
    
    if not all([sender_email, sender_password, receiver_email]):
        logging.error("邮箱配置不完整")
        return False

    try:
        # 如果内容为空，使用默认内容
        if not content or content.strip() == "":
            content = "微信步数提交任务已完成，请查看GitHub Actions日志获取详细信息。"
        
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        server = smtplib.SMTP('smtp.qq.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        
        logging.info("邮件发送成功")
        return True

    except Exception as e:
        logging.error(f"邮件发送失败: {str(e)}")
        return False

def main():
    import sys
    
    if len(sys.argv) > 1:
        summary = sys.argv[1]
    else:
        summary = "没有获取到任务执行结果"
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subject = f"微信步数提交报告 - {current_time}"
    
    if send_email(subject, summary):
        return True
    else:
        return False

if __name__ == "__main__":
    exit(0 if main() else 1)