import os
import json
import urllib.request
import socket
import ssl
import time

def check_ssl_config():
    """检查SSL配置"""
    ssl_conf_file = 'ssl.conf'
    http_redirect_file = 'http_redirect.conf'
    
    # 验证配置文件存在
    if not os.path.exists(ssl_conf_file) or not os.path.exists(http_redirect_file):
        print("错误: 缺少SSL配置文件")
        return False
    
    # 验证证书目录
    cert_dir = '.well-known/acme-challenge'
    if not os.path.exists(cert_dir):
        os.makedirs(cert_dir, exist_ok=True)
    
    return True

def test_acme_challenge():
    """测试ACME验证"""
    test_content = "test_" + str(int(time.time()))
    test_file = '.well-known/acme-challenge/test.txt'
    
    try:
        with open(test_file, 'w') as f:
            f.write(test_content)
        
        # 测试文件是否可访问
        if os.path.exists(test_file):
            os.remove(test_file)
            return True
    except Exception as e:
        print(f"ACME验证目录测试失败: {str(e)}")
        return False

def fix_ssl_configs():
    """修复SSL配置"""
    try:
        # 1. 检查现有配置
        if not check_ssl_config():
            return False
        
        # 2. 测试ACME验证
        if not test_acme_challenge():
            return False
        
        # 3. 更新SSL配置
        with open('ssl.conf', 'r', encoding='utf-8') as f:
            ssl_conf = f.read()
        
        if 'ssl_protocols' not in ssl_conf:
            print("正在添加SSL协议配置...")
            with open('ssl.conf', 'w', encoding='utf-8') as f:
                f.write(ssl_conf.replace('server {', '''server {
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;'''))
        
        # 4. 检查HTTP重定向
        with open('http_redirect.conf', 'r', encoding='utf-8') as f:
            redirect_conf = f.read()
        
        if '.well-known/acme-challenge' not in redirect_conf:
            print("正在添加ACME验证配置...")
            with open('http_redirect.conf', 'w', encoding='utf-8') as f:
                f.write(redirect_conf.replace('server {', '''server {
    location /.well-known/acme-challenge/ {
        alias /www/wwwroot/lvxing/.well-known/acme-challenge/;
        try_files $uri =404;
    }'''))
        
        print("SSL配置修复完成!")
        return True
        
    except Exception as e:
        print(f"修复SSL配置时出错: {str(e)}")
        return False

def main():
    """主函数"""
    print("开始修复SSL证书配置...")
    if fix_ssl_configs():
        print("""
修复完成！请按以下步骤操作：
1. 登录宝塔面板
2. 进入网站设置
3. 点击"SSL"选项
4. 点击"清除SSL"
5. 重新申请Let's Encrypt证书
6. 如果申请失败，请检查：
   - 域名是否正确解析到服务器
   - 80端口是否开放
   - 服务器时间是否准确
""")
    else:
        print("修复失败，请检查错误信息并重试")

if __name__ == '__main__':
    main()