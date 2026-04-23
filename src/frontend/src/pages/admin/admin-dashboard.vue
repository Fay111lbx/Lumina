<template>
  <div class="admin-dashboard">
    <div class="header">
      <h1>管理员后台</h1>
      <p class="subtitle">系统运营数据总览</p>
    </div>

    <!-- 数据概览卡片 -->
    <div class="stats-cards">
      <div class="stat-card">
        <div class="stat-icon users">👥</div>
        <div class="stat-content">
          <div class="stat-label">总用户数</div>
          <div class="stat-value">{{ dashboard.users?.total || 0 }}</div>
          <div class="stat-sub">今日新增: {{ dashboard.users?.today_new || 0 }}</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon active">✨</div>
        <div class="stat-content">
          <div class="stat-label">活跃用户</div>
          <div class="stat-value">{{ dashboard.users?.active_7d || 0 }}</div>
          <div class="stat-sub">7天活跃用户</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon dialogs">💬</div>
        <div class="stat-content">
          <div class="stat-label">总对话数</div>
          <div class="stat-value">{{ dashboard.dialogs?.total || 0 }}</div>
          <div class="stat-sub">今日: {{ dashboard.dialogs?.today || 0 }}</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon tokens">🔢</div>
        <div class="stat-content">
          <div class="stat-label">Token使用量</div>
          <div class="stat-value">{{ formatNumber(dashboard.tokens?.total_input + dashboard.tokens?.total_output) }}</div>
          <div class="stat-sub">今日: {{ formatNumber(dashboard.tokens?.today_input + dashboard.tokens?.today_output) }}</div>
        </div>
      </div>
    </div>

    <!-- 用户列表 -->
    <div class="user-list-section">
      <div class="section-header">
        <h2>用户列表</h2>
        <el-input
          v-model="searchKeyword"
          placeholder="搜索用户名"
          style="width: 200px"
          @input="searchUsers"
        />
      </div>

      <el-table :data="users" style="width: 100%">
        <el-table-column prop="user_id" label="用户ID" width="80" />
        <el-table-column prop="user_name" label="用户名" width="150" />
        <el-table-column prop="create_time" label="注册时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.create_time) }}
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.delete ? 'danger' : 'success'">
              {{ row.delete ? '已禁用' : '正常' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button size="small" @click="viewUserStats(row.user_id)">查看统计</el-button>
            <el-button
              size="small"
              :type="row.delete ? 'success' : 'danger'"
              @click="toggleUserStatus(row)"
            >
              {{ row.delete ? '启用' : '禁用' }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="totalUsers"
        layout="total, prev, pager, next"
        @current-change="loadUsers"
      />
    </div>

    <!-- 用户详情对话框 -->
    <el-dialog v-model="userStatsVisible" title="用户详细统计" width="600px">
      <div v-if="currentUserStats" class="user-stats">
        <div class="user-info">
          <h3>{{ currentUserStats.user?.user_name }}</h3>
          <p>用户ID: {{ currentUserStats.user?.user_id }}</p>
          <p>注册时间: {{ formatDate(currentUserStats.user?.create_time) }}</p>
        </div>

        <div class="stats-grid">
          <div class="stat-item">
            <div class="label">对话数</div>
            <div class="value">{{ currentUserStats.stats?.dialogs || 0 }}</div>
          </div>
          <div class="stat-item">
            <div class="label">消息数</div>
            <div class="value">{{ currentUserStats.stats?.messages || 0 }}</div>
          </div>
          <div class="stat-item">
            <div class="label">输入Token</div>
            <div class="value">{{ formatNumber(currentUserStats.stats?.tokens?.input_tokens) }}</div>
          </div>
          <div class="stat-item">
            <div class="label">输出Token</div>
            <div class="value">{{ formatNumber(currentUserStats.stats?.tokens?.output_tokens) }}</div>
          </div>
        </div>

        <div class="model-usage">
          <h4>模型使用情况</h4>
          <el-table :data="currentUserStats.stats?.models || []" size="small">
            <el-table-column prop="model" label="模型" />
            <el-table-column prop="count" label="调用次数" />
            <el-table-column prop="input_tokens" label="输入Token" />
            <el-table-column prop="output_tokens" label="输出Token" />
          </el-table>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { request } from '@/utils/request'

const dashboard = ref<any>({})
const users = ref<any[]>([])
const totalUsers = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const searchKeyword = ref('')
const userStatsVisible = ref(false)
const currentUserStats = ref<any>(null)

// 加载仪表板数据
const loadDashboard = async () => {
  try {
    const res = await request({
      url: '/api/v1/admin/dashboard',
      method: 'GET'
    })
    console.log('Dashboard API响应:', res)
    if (res.status_code === 200) {
      dashboard.value = res.data
      console.log('Dashboard数据:', dashboard.value)
    }
  } catch (error: any) {
    console.error('Dashboard加载错误:', error)
    if (error.response?.status === 403) {
      ElMessage.error('需要管理员权限')
    } else {
      ElMessage.error('加载数据失败')
    }
  }
}

// 加载用户列表
const loadUsers = async () => {
  try {
    const res = await request({
      url: '/api/v1/admin/users',
      method: 'GET',
      params: {
        page: currentPage.value,
        page_size: pageSize.value,
        keyword: searchKeyword.value || undefined
      }
    })
    console.log('Users API响应:', res)
    if (res.status_code === 200) {
      users.value = res.data.users
      totalUsers.value = res.data.total
      console.log('用户列表:', users.value, '总数:', totalUsers.value)
    }
  } catch (error) {
    console.error('用户列表加载错误:', error)
    ElMessage.error('加载用户列表失败')
  }
}

// 搜索用户
const searchUsers = () => {
  currentPage.value = 1
  loadUsers()
}

// 查看用户统计
const viewUserStats = async (userId: string) => {
  try {
    const res = await request({
      url: `/api/v1/admin/users/${userId}/stats`,
      method: 'GET',
      params: { days: 30 }
    })
    if (res.status_code === 200) {
      currentUserStats.value = res.data
      userStatsVisible.value = true
    }
  } catch (error) {
    ElMessage.error('加载用户统计失败')
  }
}

// 切换用户状态
const toggleUserStatus = async (user: any) => {
  try {
    const action = user.delete ? 'enable' : 'disable'
    await request({
      url: `/api/v1/admin/users/${user.user_id}/${action}`,
      method: 'POST'
    })
    ElMessage.success(`${action === 'enable' ? '启用' : '禁用'}成功`)
    loadUsers()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

// 格式化数字
const formatNumber = (num: number) => {
  if (!num) return '0'
  if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M'
  if (num >= 1000) return (num / 1000).toFixed(1) + 'K'
  return num.toString()
}

// 格式化日期
const formatDate = (dateStr: string) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('zh-CN')
}

onMounted(() => {
  loadDashboard()
  loadUsers()
})
</script>

<style scoped lang="scss">
.admin-dashboard {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;

  .header {
    margin-bottom: 30px;

    h1 {
      font-size: 28px;
      font-weight: 600;
      color: #303133;
      margin: 0 0 8px 0;
    }

    .subtitle {
      color: #909399;
      font-size: 14px;
      margin: 0;
    }
  }

  .stats-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin-bottom: 30px;

    .stat-card {
      background: white;
      border-radius: 8px;
      padding: 20px;
      display: flex;
      align-items: center;
      box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
      transition: transform 0.2s;

      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
      }

      .stat-icon {
        font-size: 40px;
        margin-right: 15px;
        width: 60px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 12px;

        &.users { background: #e3f2fd; }
        &.active { background: #f3e5f5; }
        &.dialogs { background: #e8f5e9; }
        &.tokens { background: #fff3e0; }
      }

      .stat-content {
        flex: 1;

        .stat-label {
          font-size: 14px;
          color: #909399;
          margin-bottom: 8px;
        }

        .stat-value {
          font-size: 28px;
          font-weight: 600;
          color: #303133;
          margin-bottom: 4px;
        }

        .stat-sub {
          font-size: 12px;
          color: #909399;
        }
      }
    }
  }

  .user-list-section {
    background: white;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);

    .section-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;

      h2 {
        font-size: 20px;
        font-weight: 600;
        color: #303133;
        margin: 0;
      }
    }

    .el-pagination {
      margin-top: 20px;
      justify-content: center;
    }
  }

  .user-stats {
    .user-info {
      padding: 20px;
      background: #f5f7fa;
      border-radius: 8px;
      margin-bottom: 20px;

      h3 {
        margin: 0 0 10px 0;
        font-size: 18px;
      }

      p {
        margin: 5px 0;
        color: #606266;
        font-size: 14px;
      }
    }

    .stats-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 15px;
      margin-bottom: 20px;

      .stat-item {
        padding: 15px;
        background: #f5f7fa;
        border-radius: 8px;
        text-align: center;

        .label {
          font-size: 14px;
          color: #909399;
          margin-bottom: 8px;
        }

        .value {
          font-size: 24px;
          font-weight: 600;
          color: #303133;
        }
      }
    }

    .model-usage {
      h4 {
        margin: 0 0 15px 0;
        font-size: 16px;
      }
    }
  }
}
</style>
