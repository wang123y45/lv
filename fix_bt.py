import os
import sys
import json
import socket
import time
import winreg
import subprocess

def is_admin():
    """检查是否有管理员权限"""
    try:
        return os.getuid() == 0
    except AttributeError:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

def modify_hosts():
    """修改hosts文件"""
    hosts_path = r'C:\Windows\System32\drivers\etc\hosts'
    
    # 备份hosts文件
    if os.path.exists(hosts_path):
        backup_path = hosts_path + '.bak'
        try:
            with open(hosts_path, 'r') as source, open(backup_path, 'w') as backup:
                backup.write(source.read())
            print("已备份hosts文件")
        except Exception as e:
            print(f"备份hosts文件失败: {str(e)}")
            return False
    
    try:
        # 读取现有hosts内容
        with open(hosts_path, 'r') as f:
            lines = f.readlines()
        
        # 移除所有bt.cn相关条目
        new_lines = [line for line in lines if 'bt.cn' not in line]
        
        # 添加新的解析记录
        new_lines.extend([
            '\n# BT Panel Nodes\n',
            '103.224.251.67 www.bt.cn\n',
            '103.224.251.67 api.bt.cn\n',
            '103.224.251.67 download.bt.cn\n'
        ])
        
        # 写入新的hosts文件
        with open(hosts_path, 'w') as f:
            f.writelines(new_lines)
        
        print("hosts文件更新成功")
        return True
    except Exception as e:
        print(f"修改hosts文件失败: {str(e)}")
        return False

def flush_dns():
    """刷新DNS缓存"""
    try:
        subprocess.run(['ipconfig', '/flushdns'], check=True, capture_output=True)
        print("DNS缓存已刷新")
        return True
    except subprocess.CalledProcessError as e:
        print(f"刷新DNS缓存失败: {str(e)}")
        return False

def update_bt_config():
    """更新宝塔面板配置"""
    bt_path = r'D:\BtSoft\panel'
    node_path = os.path.join(bt_path, 'data/node_url.pl')
    
    config = {
        'api-node': {
            'url': 'api.bt.cn',
            'ip': '103.224.251.67',
            'ping': 50,
            'name': '官方API节点'
        },
        'www-node': {
            'url': 'www.bt.cn',
            'ip': '103.224.251.67',
            'ping': 50,
            'name': '官方WWW节点'
        },
        'down-node': {
            'url': 'download.bt.cn',
            'ip': '103.224.251.67',
            'ping': 50,
            'name': '官方下载节点'
        }
    }
    
    try:
        os.makedirs(os.path.dirname(node_path), exist_ok=True)
        with open(node_path, 'w') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        print("宝塔面板配置已更新")
        return True
    except Exception as e:
        print(f"更新宝塔面板配置失败: {str(e)}")
        return False

def restart_panel():
    """重启宝塔面板服务"""
    try:
        subprocess.run(['net', 'stop', 'BtPanel'], check=True, capture_output=True)
        time.sleep(2)
        subprocess.run(['net', 'start', 'BtPanel'], check=True, capture_output=True)
        print("宝塔面板服务已重启")
        return True
    except subprocess.CalledProcessError as e:
        print(f"重启宝塔面板服务失败: {str(e)}")
        return False

def main():
    """主函数"""
    if not is_admin():
        print("请以管理员权限运行此脚本")
        return False
    
    print("开始修复宝塔面板...")
    
    # 1. 修改hosts文件
    if not modify_hosts():
        return False
    
    # 2. 刷新DNS缓存
    if not flush_dns():
        return False
    
    # 3. 更新宝塔面板配置
    if not update_bt_config():
        return False
    
    # 4. 重启面板服务
    if not restart_panel():
        return False
    
    print("""
修复完成！请按以下步骤操作：
1. 打开宝塔面板界面
2. 点击软件商店
3. 找到MySQL
4. 点击安装
5. 选择MySQL 5.7版本（推荐）
6. 设置root密码
7. 等待安装完成
    """)

if __name__ == '__main__':
    main()