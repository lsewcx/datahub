import axios from "axios";

const service = axios.create({
    // 请求的基础路径
    baseURL: "",
    // 请求超时时间
    timeout: 2000,
    // 请求头信息
});

// 请求拦截器
service.interceptors.request.use(config => {
    return config;
}, error => {
    // 对请求错误做些什么
    console.error('Request error:', error);
});

// 响应拦截器
service.interceptors.response.use(response => {
    return response.data;
}, error => {
    return Promise.reject(error);
});

export default service;