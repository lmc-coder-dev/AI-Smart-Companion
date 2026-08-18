# AI 智能伴侣（AI Smart Companion）

一个基于 [Streamlit](https://streamlit.io/) 和 DeepSeek 大模型构建的 AI 虚拟伴侣聊天应用。你可以自定义伴侣的昵称与性格，它会以符合该设定的方式与你聊天，并支持多个会话的保存、加载与删除。

## ✨ 功能特性

- 💬 角色扮演聊天：自定义昵称与性格，AI 按设定人设回复
- 📝 多会话管理：新建、加载会话，聊天记录自动保存到本地
- 🎨 界面简洁：仿微信聊天风格，侧边栏管理会话
- 🔒 本地存储：会话数据保存在本地 JSON 文件，不上传云端

## 📸 界面截图

<img width="1920" height="910" alt="image" src="https://github.com/user-attachments/assets/113f068b-b102-485d-8ea8-eec9ada2c117" />

## 🛠️ 技术栈

- Python 3
- Streamlit 1.59
- OpenAI SDK 2.46（用于调用 DeepSeek 接口）

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/lmc-coder-dev/AI-Smart-Companion.git
cd AI-Smart-Companion
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 DeepSeek API Key（重要）

本项目调用 DeepSeek 大模型，运行前必须在本地设置环境变量 `DEEPSEEK_API_KEY`。

> 还没有 Key？先到 [DeepSeek 开放平台](https://platform.deepseek.com/) 注册并创建 API Key。

**Windows（PowerShell）：**

```powershell
$env:DEEPSEEK_API_KEY="sk-你的密钥"
```

**macOS / Linux（Bash）：**

```bash
export DEEPSEEK_API_KEY="sk-你的密钥"
```

> 也可以把该变量写入系统环境变量，永久生效。

### 4. 运行

```bash
streamlit run main.py
```

浏览器会自动打开，默认地址 `http://localhost:8501`。

## 📖 使用说明

- **新建会话**：点击侧边栏「📝 新建会话」，开始一段全新对话
- **加载会话**：在「会话历史」中点击某个会话名即可切换
- **删除会话**：点击会话右侧的「❌」按钮
- **设置伴侣**：在「伴侣信息」中修改昵称与性格，会影响 AI 的回复风格

## 📁 项目结构

```
AI-Smart-Companion/
├── main.py              # 主程序（Streamlit 应用）
├── requirements.txt     # 依赖清单
├── img/
│   ├── img.png          # 页面图标
│   └── screenshot.png   # 界面截图
├── sessions/            # 会话数据（本地生成，已加入 .gitignore）
└── README.md
```

## ⚠️ 注意事项

- `sessions/` 目录存放你的聊天记录，属于隐私数据，已在 `.gitignore` 中排除，不会被上传到 GitHub。
- 请勿把 `DEEPSEEK_API_KEY` 提交到仓库，仅通过环境变量配置。

## 📄 License

[MIT](LICENSE)
