import requests
import logging
import random
import os
import json
from datetime import datetime

# 设置日志
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s: %(message)s'
)

def get_step_range_by_time():
    """根据当前时间返回对应的步数范围"""
    current_hour = datetime.now().hour
    
    if 8 <= current_hour < 12:  # 早上9点
        return (5000, 8000)
    elif 12 <= current_hour < 16:  # 下午2点
        return (15000, 18000)
    elif 16 <= current_hour < 21:  # 晚上7点
        return (21000, 23000)
    else:  # 其他时间使用默认范围
        return (5000, 8000)

def load_accounts_from_env():
    """从环境变量加载账号信息"""
    accounts_json = os.getenv('WECHAT_ACCOUNTS')
    if not accounts_json:
        logging.error("未找到账号配置，请设置 WECHAT_ACCOUNTS 环境变量")
        return []
    
    try:
        accounts = json.loads(accounts_json)
        logging.info(f"成功加载 {len(accounts)} 个账号")
        return accounts
    except json.JSONDecodeError as e:
        logging.error(f"账号配置格式错误: {e}")
        return []

def submit_wechat_steps(username, password):
    """提交微信步数"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Origin': 'https://m.cqzz.top/',
        'Referer': 'https://m.cqzz.top/',
        "Content-Type": "application/x-www-form-urlencoded",
    }

    url = "https://wzz.wangzouzou.com/motion/api/motion/Xiaomi"
    
    # 根据时间生成对应范围的步数
    min_steps, max_steps = get_step_range_by_time()
    steps = random.randint(min_steps, max_steps)

    data = {
        "phone": username,
        "pwd": password,
        "num": steps
    }

    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 200:
                return True, f"提交成功! 步数: {steps}", steps
            else:
                return False, f"提交失败: {result.get('data', '未知错误')}", steps
        else:
            return False, f"服务器错误: {response.status_code}", steps

    except requests.exceptions.RequestException as e:
        return False, f"请求异常: {str(e)}", steps

def process_all_accounts():
    """处理所有账号的步数提交"""
    accounts = load_accounts_from_env()
    if not accounts:
        return [], "❌ 没有可用的账号配置"
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    min_steps, max_steps = get_step_range_by_time()
    
    logging.info(f"开始处理 {len(accounts)} 个账号 - 时间: {current_time}")
    logging.info(f"当前时段步数范围: {min_steps}-{max_steps}")
    
    results = []
    success_count = 0

    for i, account in enumerate(accounts, 1):
        username = account.get("username")
        password = account.get("password")
        
        if not username or not password:
            logging.warning(f"账号 {i} 配置不完整，跳过")
            continue
            
        # 隐藏用户名敏感信息
        masked_username = username[:3] + "****" + username[-2:] if len(username) > 5 else "***"
        logging.info(f"处理账号 {i}/{len(accounts)}: {masked_username}")
        
        success, message, steps = submit_wechat_steps(username, password)
        result = {
            "account": masked_username,
            "success": success,
            "message": message,
            "steps": steps
        }
        results.append(result)
        
        if success:
            success_count += 1
            logging.info(f"✓ 账号 {i} 成功: {steps}步")
        else:
            logging.error(f"✗ 账号 {i} 失败: {message}")
        
        # 请求间隔，避免频繁访问
        if i < len(accounts):
            time.sleep(2)

    # 生成汇总报告
    time_period = {
        (5000, 8000): "早上",
        (15000, 18000): "下午", 
        (21000, 23000): "晚上"
    }.get((min_steps, max_steps), "当前")
    
    summary = (
        f"🏃 微信步数提交报告 - {time_period}时段\n"
        f"📅 时间: {current_time}\n"
        f"👥 总账号: {len(accounts)}个\n"
        f"✅ 成功: {success_count}个\n"
        f"❌ 失败: {len(accounts) - success_count}个\n"
        f"🎯 步数范围: {min_steps}-{max_steps}\n"
    )
    
    for i, result in enumerate(results, 1):
        status = "✅" if result["success"] else "❌"
        summary += f"\n{status} 账号{i}: {result['account']} - {result['steps']}步"
    
    logging.info(f"任务完成: {summary}")
    return results, summary

def main():
    """主函数"""
    try:
        logging.info("🚀 开始执行微信步数提交任务")
        results, summary = process_all_accounts()
        logging.info("🎉 所有任务执行完成")
        return True, summary
    except Exception as e:
        logging.error(f"❌ 任务执行失败: {str(e)}")
        return False, f"任务执行失败: {str(e)}"

if __name__ == "__main__":
    success, summary = main()
    exit(0 if success else 1)
