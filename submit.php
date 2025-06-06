<?php
// 设置管理员访问密码
define('ADMIN_PASSWORD', 'admin123');

// 首先检查是否是管理员访问
if (isset($_GET['password']) && $_GET['password'] === ADMIN_PASSWORD) {
    // 管理员访问时使用HTML响应头
    header('Content-Type: text/html; charset=utf-8');
    
    $dataFile = 'bookings.json';
    if (!file_exists($dataFile)) {
        // 如果文件不存在，创建一个空的JSON数组
        file_put_contents($dataFile, '[]');
    }

    $existingData = json_decode(file_get_contents($dataFile), true);
    if ($existingData === null) {
        $existingData = [];
    }

    echo '<!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>预约记录管理</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 100%; margin-top: 20px; }
            th, td { border: 1px solid #ddd; padding: 12px 8px; text-align: left; }
            th { background-color: #8b572a; color: white; }
            tr:nth-child(even) { background-color: #f2f2f2; }
            tr:hover { background-color: #f5f5f5; }
            .no-records { text-align: center; padding: 20px; color: #666; }
        </style>
    </head>
    <body>
        <h1>预约记录</h1>';
    
    if (empty($existingData)) {
        echo '<div class="no-records">暂无预约记录</div>';
    } else {
        echo '<table>
            <tr>
                <th>提交时间</th>
                <th>姓名</th>
                <th>电话</th>
                <th>出行日期</th>
                <th>人数</th>
                <th>特殊要求</th>
            </tr>';
        
        foreach (array_reverse($existingData) as $booking) {
            echo '<tr>';
            echo '<td>' . htmlspecialchars($booking['submit_time'] ?? '') . '</td>';
            echo '<td>' . htmlspecialchars($booking['name'] ?? '') . '</td>';
            echo '<td>' . htmlspecialchars($booking['phone'] ?? '') . '</td>';
            echo '<td>' . htmlspecialchars($booking['travel_date'] ?? '') . '</td>';
            echo '<td>' . htmlspecialchars($booking['people_count'] ?? '') . '</td>';
            echo '<td>' . htmlspecialchars($booking['special_requirements'] ?? '') . '</td>';
            echo '</tr>';
        }
        echo '</table>';
    }
    echo '</body></html>';
    exit;
}

// 如果不是管理员访问，那就是表单提交
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // 设置JSON响应头
    header('Content-Type: application/json; charset=utf-8');
    
    try {
        // 验证必填字段
        $required_fields = ['name', 'phone', 'travel_date', 'people_count'];
        foreach ($required_fields as $field) {
            if (empty($_POST[$field])) {
                throw new Exception("请填写{$field}字段");
            }
        }

        // 接收表单数据
        $formData = [
            'name' => trim($_POST['name']),
            'phone' => trim($_POST['phone']),
            'travel_date' => trim($_POST['travel_date']),
            'people_count' => (int)$_POST['people_count'],
            'special_requirements' => trim($_POST['special_requirements'] ?? ''),
            'submit_time' => date('Y-m-d H:i:s')
        ];

        // 准备数据文件
        $dataFile = 'bookings.json';
        if (!file_exists($dataFile)) {
            file_put_contents($dataFile, '[]');
        }

        // 读取现有数据
        $json = file_get_contents($dataFile);
        $existingData = json_decode($json, true);
        if ($existingData === null) {
            $existingData = [];
        }

        // 添加新数据
        $existingData[] = $formData;

        // 保存数据
        $result = file_put_contents($dataFile, json_encode($existingData, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
        if ($result === false) {
            throw new Exception('保存数据失败，请稍后重试');
        }

        echo json_encode([
            'success' => true,
            'message' => '预约信息已成功提交'
        ]);

    } catch (Exception $e) {
        http_response_code(400);
        echo json_encode([
            'success' => false,
            'message' => $e->getMessage()
        ]);
    }
    exit;
}

// 如果既不是POST请求也不是管理员访问
header('Content-Type: application/json; charset=utf-8');
echo json_encode([
    'success' => false,
    'message' => '无效的请求方式'
]);