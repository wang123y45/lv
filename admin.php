<?php
session_start();

// 如果已经登录，直接跳转到预约记录页面
if (isset($_SESSION['admin_logged_in']) && $_SESSION['admin_logged_in'] === true) {
    header('Location: submit.php?password=admin123');
    exit;
}

// 处理登录请求
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if ($_POST['password'] === 'admin123') {
        $_SESSION['admin_logged_in'] = true;
        header('Location: submit.php?password=admin123');
        exit;
    } else {
        $error = '密码错误';
    }
}
?>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>管理员登录</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0e6f7;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .login-box {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            width: 300px;
        }
        h1 {
            color: #8b572a;
            text-align: center;
            margin-bottom: 20px;
        }
        input[type="password"] {
            width: 100%;
            padding: 8px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 10px;
            background-color: #8b572a;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #6d4c41;
        }
        .error {
            color: red;
            text-align: center;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="login-box">
        <h1>管理员登录</h1>
        <?php if (isset($error)): ?>
            <div class="error"><?php echo $error; ?></div>
        <?php endif; ?>
        <form method="POST">
            <input type="password" name="password" placeholder="请输入管理员密码" required>
            <button type="submit">登录</button>
        </form>
    </div>
</body>
</html>