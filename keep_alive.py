import os
import logging
from datetime import datetime

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

def update_status_file():
    """更新状态文件以保持仓库活跃"""
    status_file = "status.md"
    
    # 获取当前时间
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 读取现有内容或创建新文件
    if os.path.exists(status_file):
        with open(status_file, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = ""
    
    # 添加新的状态记录
    new_entry = f"## {current_time}\n- 微信步数提交任务已执行\n- 仓库活跃状态已更新\n\n"
    
    # 保持文件大小合理，只保留最近50条记录
    entries = content.split('## ')
    if len(entries) > 50:
        entries = entries[:50]
        updated_content = '## '.join(entries)
    else:
        updated_content = content
    
    # 完全重写构建内容的方式，避免复杂f-string
    header = "# 项目状态记录\n\n"
    
    # 如果内容已经包含头部，就分割处理
    if header.strip() in updated_content:
        parts = updated_content.split(header.strip(), 1)
        if len(parts) > 1:
            final_content = header + new_entry + parts[1]
        else:
            final_content = header + new_entry + updated_content
    else:
        final_content = header + new_entry + updated_content
    
    with open(status_file, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    logging.info(f"已更新状态文件: {status_file}")
    return True

def commit_and_push():
    """提交更改并推送到仓库"""
    try:
        # 配置Git用户信息
        os.system('git config --global user.name "GitHub Actions"')
        os.system('git config --global user.email "actions@github.com"')
        
        # 添加更改
        os.system('git add .')
        
        # 提交更改
        commit_message = f"更新状态文件 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        result = os.system(f'git commit -m "{commit_message}"')
        
        if result != 0:
            logging.info("没有更改需要提交")
            return True
            
        # 推送到仓库
        push_result = os.system('git push')
        if push_result == 0:
            logging.info("更改已提交并推送到仓库")
            return True
        else:
            logging.error("推送失败")
            return False
            
    except Exception as e:
        logging.error(f"提交更改失败: {str(e)}")
        return False

def main():
    """主函数"""
    try:
        logging.info("开始执行仓库保活任务")
        
        # 更新状态文件
        if update_status_file():
            # 提交并推送更改
            if commit_and_push():
                logging.info("仓库保活任务完成")
                return True
        
        logging.error("仓库保活任务失败")
        return False
    except Exception as e:
        logging.error(f"仓库保活任务异常: {str(e)}")
        return False

if __name__ == "__main__":
    exit(0 if main() else 1)