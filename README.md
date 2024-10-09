# 后端启动指南

## 安装环境
```bash
conda create --name datahub python==3.9.13
```

```bash
cd backend
pip install -r requirements.txt
```

# 库
- moment 时间库
- vue-router 路由
- tailwindcss 样式
- shadcn-vue ui库
- mock 脱离后端纯前端展示
- Axios 请求库

# 关于mock
mock默认开启如果需要关闭则到.env中把VITE_USE_MOCK设置为false