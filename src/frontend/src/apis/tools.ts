/**
 * 工具API接口
 */
import request from '../utils/request'

interface ApiResponse<T> {
  status_code: number
  status_message: string
  data: T
}

// ==================== 天气查询 ====================
export interface WeatherData {
  city: string
  temperature: string
  weather: string
  humidity: string
  wind: string
  update_time: string
}

export function getWeatherAPI(city: string) {
  return request<ApiResponse<WeatherData>>({
    url: '/api/v1/weather',
    method: 'GET',
    params: { city }
  })
}

// ==================== 邮件发送 ====================
export interface SendEmailRequest {
  sender: string
  receiver: string
  message: string
  password: string
}

export function sendEmailAPI(data: SendEmailRequest) {
  return request<ApiResponse<{ message: string }>>({
    url: '/api/v1/email/send',
    method: 'POST',
    data
  })
}

// ==================== 论文检索 ====================
export function searchArxivAPI(query: string) {
  return request<ApiResponse<{ query: string; papers: string }>>({
    url: '/api/v1/arxiv/search',
    method: 'GET',
    params: { query }
  })
}

// ==================== 物流查询 ====================
export function trackDeliveryAPI(trackingNumber: string) {
  return request<ApiResponse<{ tracking_number: string; info: string }>>({
    url: '/api/v1/delivery/track',
    method: 'GET',
    params: { tracking_number: trackingNumber }
  })
}

// ==================== 文件转换 ====================
export function convertToPdfAPI(fileUrl: string) {
  return request<ApiResponse<{ message: string }>>({
    url: '/api/v1/convert/to-pdf',
    method: 'POST',
    data: { file_url: fileUrl }
  })
}

export function convertToDocxAPI(fileUrl: string) {
  return request<ApiResponse<{ message: string }>>({
    url: '/api/v1/convert/to-docx',
    method: 'POST',
    data: { file_url: fileUrl }
  })
}

// ==================== 文生图 ====================
export function generateImageAPI(prompt: string) {
  return request<ApiResponse<{ message: string; prompt: string }>>({
    url: '/api/v1/image/generate',
    method: 'POST',
    data: { prompt }
  })
}

// ==================== 联网搜索 ====================
export interface TavilySearchParams {
  query: string
  topic?: 'general' | 'news' | 'finance'
  max_results?: number
  time_range?: 'day' | 'week' | 'month' | 'year'
}

export function searchWithTavilyAPI(params: TavilySearchParams) {
  return request<ApiResponse<{ query: string; results: string }>>({
    url: '/api/v1/search/tavily',
    method: 'GET',
    params
  })
}

export interface BochaSearchRequest {
  query: string
  count?: number
  freshness?: 'noLimit' | 'oneDay' | 'oneWeek' | 'oneMonth' | 'oneYear'
  summary?: boolean
  include?: string
  exclude?: string
}

export function searchWithBochaAPI(data: BochaSearchRequest) {
  return request<ApiResponse<{ query: string; results: string }>>({
    url: '/api/v1/search/bocha',
    method: 'POST',
    data
  })
}
