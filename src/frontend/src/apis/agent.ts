import { request } from "../utils/request"

// 智能体相关接口类型定义
export interface AgentCreateRequest {
  name: string
  description: string
  logo_url: string
  tool_ids: string[]
  llm_id: string
  mcp_ids: string[]
  system_prompt: string
  knowledge_ids: string[]
  enable_memory: boolean
}

export interface AgentUpdateRequest {
  agent_id: string
  name?: string
  description?: string
  logo_url?: string
  tool_ids?: string[]
  llm_id?: string
  mcp_ids?: string[]
  system_prompt?: string
  knowledge_ids?: string[]
  enable_memory?: boolean
}

export interface AgentResponse {
  agent_id: string
  name: string
  description: string
  logo_url: string
  tool_ids: string[]
  llm_id: string
  mcp_ids: string[]
  system_prompt: string
  knowledge_ids: string[]
  enable_memory: boolean
}

export interface ApiResponse<T> {
  status_code: number
  status_message: string
  data: T
}

// 创建智能体
export function createAgentAPI(data: AgentCreateRequest) {
  return request<ApiResponse<null>>({
    url: '/api/v1/agent',
    method: 'POST',
    data
  })
}

// 获取智能体列表
export function getAgentsAPI() {
  return request<ApiResponse<AgentResponse[]>>({
    url: '/api/v1/agent',
    method: 'GET'
  })
}

// 根据ID获取智能体详情（新接口，更高效）
export function getAgentByIdAPI(agentId: string) {
  return request<ApiResponse<AgentResponse>>({
    url: `/api/v1/agent/${agentId}`,
    method: 'GET'
  })
}

// 删除智能体
export function deleteAgentAPI(data: { agent_id: string }) {
  return request<ApiResponse<null>>({
    url: '/api/v1/agent',
    method: 'DELETE',
    data
  })
}

// 更新智能体
export function updateAgentAPI(data: AgentUpdateRequest) {
  return request<ApiResponse<null>>({
    url: '/api/v1/agent',
    method: 'PUT',
    data
  })
}

// 克隆智能体
export function cloneAgentAPI(agentId: string) {
  return request<ApiResponse<AgentResponse>>({
    url: `/api/v1/agent/${agentId}/clone`,
    method: 'POST'
  })
}

// 搜索智能体
export function searchAgentsAPI(data: { name: string }) {
  return request<ApiResponse<Array<{
    agent_id: string
    name: string
    description: string
    logo_url: string
  }>>>({
    url: '/api/v1/agent/search',
    method: 'POST',
    data
  })
}

// 获取默认参数（保留原有接口）
export function defaultParameterAPI() {
  return request({
    url: '/api/default/parameter',
    method: 'GET',
  })
}

// 获取默认代码（保留原有接口）
export function defaultCodeAPI() {
  return request({
    url: '/api/default/code',
    method: 'GET',
  })
}
