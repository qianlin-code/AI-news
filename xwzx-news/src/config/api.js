/**
 * API配置文件
 * 包含API基础URL和AI问答功能所需的API参数
 */

// API基础URL配置
export const apiConfig = {
  // 后端API基础URL
  baseURL: 'http://127.0.0.1:8000',
}

export const aiChatConfig = {
  // OpenAI API地址
  apiEndpoint: 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',
  
  // API Key (由开发人员指定)
  apiKey: 'sk-ws-H.EMYXXDL.4ZMF.MEYCIQCJG9T8DP2VUdR3On1o1DM1aALgpX9nUeHCDLv0FtmdMwIhAONZi9FB0SYw0aPliB5X-9uZEPwnompjoCM9T--QTKwn',
  
  // 使用的模型
  model: 'qwen3-max-preview'
}
