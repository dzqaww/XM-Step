import smtplib
import os
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

def send_email(subject, content):
    """发送邮件通知"""
    # 从环境变量获取邮箱配置
    sender_email = os.getenv('EMAIL_SENDER')
    sender_password = os.getenv('EMAIL_PASSWORD')
    receiver_email = os.getenv('EMAIL_RECEIVER')
    
    if not all([sender_email, sender_password, receiver_email]):
        logging.error("邮箱配置不完整，无法发送邮件")
        return False

    try:
        # 创建邮件
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # 如果内容为空，使用默认内容
        if not content or content.strip() == "":
            content = "微信步数提交任务已完成，但未获取到详细结果。请查看GitHub Actions日志获取更多信息。"
        
        # 添加邮件内容
        msg.attach(MIMEText(content, 'plain'))

        # 连接SMTP服务器并发送
        server = smtplib.SMTP('smtp.qq.com', 587)
        server.starttls()  # 启用TLS加密
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        
        logging.info(f"✅ 邮件发送成功: {subject}")
        logging.info(f"邮件内容: {content}")
        return True

    except Exception as e:
        logging.error(f"❌ 邮件发送失败: {str(e)}")
        return False

def main():
    """推送主函数"""
    import sys
    
    # 从命令行参数获取摘要信息
    if len(sys.argv) > 1:
        summary = sys.argv[1]
    else:
        summary = "没有获取到任务执行结果"
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subject = f"微信步数提交报告 - {current_time}"
    
    if send_email(subject, summary):
        logging.info("🎉 邮件推送完成")
        return True
    else:
        logging.error("❌ 邮件推送失败")
        return False

if __name__ == "__main__":
    exit(0 if main() else 1)
