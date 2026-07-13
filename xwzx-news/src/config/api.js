/**
 * API配置文件
 * 包含API基础URL和AI问答功能所需的API参数
 * 所有敏感信息从 .env 环境变量读取
 */

// API基础URL配置
export const apiConfig = {
  // 后端API基础URL
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000',
}

export const aiChatConfig = {
  // OpenAI兼容 API地址
  apiEndpoint: import.meta.env.VITE_AI_API_ENDPOINT || 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',

  // API Key（从环境变量读取）
  apiKey: import.meta.env.VITE_AI_API_KEY || '',

  // 使用的模型
  model: import.meta.env.VITE_AI_MODEL || 'qwen3-max-preview',
}
