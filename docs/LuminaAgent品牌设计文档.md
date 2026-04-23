# LuminaAgent 品牌设计文档

## 🎨 品牌标识

### 产品名称
- **中文名称**：LuminaAgent
- **英文名称**：LuminaAgent
- **品牌含义**：Lumina（拉丁语：光明、启发）+ Agent（智能体）

### Slogan
- **中文**：照亮你的知识世界
- **英文**：Illuminate Your Knowledge

---

## 🌈 配色方案

### 主色调
```
渐变蓝紫色：
- 起始色：#4A90E2（天空蓝）
- 中间色：#7B68EE（中紫蓝）
- 结束色：#9B59B6（紫罗兰）

渐变代码：
background: linear-gradient(135deg, #4A90E2 0%, #9B59B6 100%);
```

### 辅助色
```
浅色背景：
- 浅蓝：#e8f4fd
- 浅紫：#f3e8ff
- 渐变背景：linear-gradient(135deg, #e8f4fd 0%, #f3e8ff 100%)

文字颜色：
- 主文字：#333333
- 次要文字：#666666
- 辅助文字：#999999
- 链接色：#4A90E2
- 链接悬停：#9B59B6
```

### 按钮配色
```
主按钮：
- 背景：linear-gradient(135deg, #4A90E2 0%, #9B59B6 100%)
- 文字：#FFFFFF
- 阴影：0 4px 15px rgba(74, 144, 226, 0.3)
- 悬停阴影：0 8px 25px rgba(155, 89, 182, 0.4)

次要按钮：
- 背景：transparent
- 边框：2px solid #e8f4fd
- 文字：#4A90E2
- 悬停边框：#9B59B6
```

---

## 🎯 Logo 设计

### Logo 元素
- **主图标**：光芒四射的星星
- **设计理念**：象征知识的光芒，照亮前行的道路
- **颜色**：渐变蓝紫色（#4A90E2 → #9B59B6）
- **装饰元素**：小星星点缀，增加灵动感

### Logo 文件
```
文件路径：src/frontend/src/assets/lumina-logo.svg
尺寸：64x64 px（可缩放）
格式：SVG 矢量图
```

### Logo 使用规范
```
最小尺寸：32x32 px
安全空间：Logo 周围至少留出 8px 空白
背景要求：
  - 浅色背景：使用原色 Logo
  - 深色背景：使用白色 Logo
  - 渐变背景：使用白色 Logo + 阴影
```

---

## 📐 设计规范

### 圆角规范
```
大卡片：24px
中等卡片：16px
小卡片/按钮：12px
输入框：12px
标签/徽章：8px
```

### 阴影规范
```
轻阴影（卡片）：
box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);

中阴影（悬停）：
box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);

重阴影（弹窗）：
box-shadow: 0 20px 60px rgba(74, 144, 226, 0.15);

品牌阴影（按钮）：
box-shadow: 0 4px 15px rgba(74, 144, 226, 0.3);
```

### 间距规范
```
超小间距：4px
小间距：8px
中间距：16px
大间距：24px
超大间距：32px
```

---

## 🖋️ 字体规范

### 字体家族
```css
font-family: 'PingFang SC', 'Helvetica Neue', Arial, sans-serif;
```

### 字体大小
```
超大标题：48px（主页品牌名）
大标题：32px（登录页品牌名）
中标题：24px（页面标题）
小标题：18px（卡片标题）
正文：15-16px
辅助文字：13-14px
小字：12px
```

### 字重
```
超粗：800（品牌名称）
粗体：700（标题）
半粗：600（按钮、重点文字）
常规：400（正文）
```

---

## 🎨 页面设计

### 登录页面
```
背景：渐变蓝紫色 + 动态光斑
卡片：白色半透明（rgba(255, 255, 255, 0.95)）
Logo：80x80 px，渐变背景
品牌名：32px，渐变文字
Slogan：
  - 中文：16px，#5a5a5a
  - 英文：13px，#9B59B6，斜体
输入框：
  - 边框：2px solid #e8f4fd
  - 聚焦：#9B59B6 + 阴影
按钮：渐变蓝紫色，52px 高
```

### 注册页面
```
背景：渐变蓝紫色 + 动态光斑
卡片：白色半透明
Logo：56x56 px
其他样式：与登录页保持一致
```

### 主页面
```
背景：白色
Logo：60x60 px
品牌名：48px，渐变文字 + 光晕效果
搜索框：
  - 背景：#f8f9fa
  - 边框：#e9ecef
  - 聚焦：#9B59B6 + 阴影
发送按钮：渐变蓝紫色，圆形
案例卡片：
  - 背景：白色
  - 边框：#f1f5f9
  - 悬停：上移 + 阴影增强
  - 标签：渐变蓝紫色背景
```

---

## 🎭 动画效果

### 按钮动画
```css
transition: all 0.3s ease;

/* 悬停 */
&:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(155, 89, 182, 0.4);
}

/* 点击 */
&:active {
  transform: translateY(0);
}
```

### 卡片动画
```css
transition: all 0.3s ease;

/* 悬停 */
&:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
}
```

### 输入框动画
```css
transition: all 0.3s ease;

/* 聚焦 */
&:focus-within {
  border-color: #9B59B6;
  box-shadow: 0 0 0 4px rgba(155, 89, 182, 0.1);
}
```

---

## 📱 响应式设计

### 断点
```
移动端：< 768px
平板：768px - 1024px
桌面：> 1024px
```

### 移动端适配
```
品牌名：36px（缩小）
Logo：48x48 px（缩小）
卡片内边距：24px（缩小）
搜索框高度：140px（缩小）
按钮高度：36px（缩小）
```

---

## 🎯 品牌应用示例

### 网页标题
```html
<title>LuminaAgent - 照亮你的知识世界</title>
```

### Meta 描述
```html
<meta name="description" content="LuminaAgent - 照亮你的知识世界。基于大语言模型的智能对话系统，支持知识库管理、多工具调用、工作流编排。Illuminate Your Knowledge." />
```

### 社交媒体分享
```
标题：LuminaAgent - 照亮你的知识世界
描述：智能对话系统，让知识触手可及
图片：lumina-logo.svg（建议 1200x630 px）
```

---

## 🔧 技术实现

### CSS 变量（建议）
```css
:root {
  /* 主色 */
  --primary-start: #4A90E2;
  --primary-mid: #7B68EE;
  --primary-end: #9B59B6;
  --primary-gradient: linear-gradient(135deg, var(--primary-start) 0%, var(--primary-end) 100%);
  
  /* 背景色 */
  --bg-light-blue: #e8f4fd;
  --bg-light-purple: #f3e8ff;
  --bg-gradient: linear-gradient(135deg, var(--bg-light-blue) 0%, var(--bg-light-purple) 100%);
  
  /* 文字色 */
  --text-primary: #333333;
  --text-secondary: #666666;
  --text-tertiary: #999999;
  
  /* 圆角 */
  --radius-lg: 24px;
  --radius-md: 16px;
  --radius-sm: 12px;
  --radius-xs: 8px;
  
  /* 阴影 */
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.08);
  --shadow-md: 0 8px 20px rgba(0, 0, 0, 0.12);
  --shadow-lg: 0 20px 60px rgba(74, 144, 226, 0.15);
  --shadow-brand: 0 4px 15px rgba(74, 144, 226, 0.3);
}
```

---

## 📋 文件清单

### 已修改的文件
```
✅ src/frontend/index.html - 页面标题
✅ src/frontend/src/assets/lumina-logo.svg - 新 Logo
✅ src/frontend/src/pages/login/login.vue - 登录页
✅ src/frontend/src/pages/login/register.vue - 注册页
✅ src/frontend/src/pages/homepage/homepage.vue - 主页
```

### 需要修改的文件（可选）
```
⏳ src/frontend/public/favicon.ico - 网站图标
⏳ src/frontend/src/components/Header.vue - 顶部导航栏
⏳ src/frontend/src/components/Sidebar.vue - 侧边栏
⏳ README.md - 项目说明
```

---

## 🎉 品牌特点

### 视觉特点
- ✨ **优雅现代**：渐变蓝紫色，科技感与优雅并存
- 🌟 **光明主题**：星星 Logo，象征知识的光芒
- 💎 **精致细腻**：圆角、阴影、动画，细节到位
- 🎨 **和谐统一**：配色协调，视觉一致性强

### 情感传达
- 💡 **启发**：照亮知识，启发思考
- 🚀 **专业**：科技感强，值得信赖
- 🤝 **友好**：柔和配色，亲和力强
- ✨ **创新**：现代设计，与时俱进

---

## 📞 品牌联系

```
产品名称：LuminaAgent
官方网站：（待定）
GitHub：（待定）
邮箱：（待定）
```

---

**LuminaAgent - 照亮你的知识世界 | Illuminate Your Knowledge**
