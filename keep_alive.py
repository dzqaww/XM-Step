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
        content = "# 项目状态记录\n\n"
    
    # 添加新的状态记录
    new_entry = f"## {current_time}\n- 微信步数提交任务已执行\n- 仓库活跃状态已更新\n\n"
    
    # 保持文件大小合理，只保留最近50条记录
    entries = content.split('## ')
    if len(entries) > 50:
        entries = entries[:50]
        updated_content = '## '.join(entries)
    else:
        updated_content = content
    
    # 修复f-string中的反斜杠问题
    header = "# 项目状态记录\n\n"
    if '# 项目状态记录\n\n' in updated_content:
        content_after_header = updated_content.split('# 项目状态记录\n\n', 1)[-1]
        final_content = header + new_entry + content_after_header
    else:
        final_content = header + new_entry + updated_content
    
    with open(status_file, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    logging.info(f"✅ 已更新状态文件: {status_file}")
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
        os.system(f'git commit -m "{commit_message}"')
        
        # 推送到仓库
        os.system('git push')
        
        logging.info("✅ 更改已提交并推送到仓库")
        return True
    except Exception as e:
        logging.error(f"❌ 提交更改失败: {str(e)}")
        return False

def main():
    """主函数"""
    try:
        logging.info("🔄 开始执行仓库保活任务")
        
        # 更新状态文件
        if update_status_file():
            # 提交并推送更改
            if commit_and_push():
                logging.info("🎉 仓库保活任务完成")
                return True
        
        logging.error("❌ 仓库保活任务失败")
        return False
    except Exception as e:
        logging.error(f"❌ 仓库保活任务异常: {str(e)}")
        return False

if __name__ == "__main__":
    exit(0 if main() else 1)
