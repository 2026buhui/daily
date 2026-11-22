# 📰 Daily Hotspot — GitHub 每日热点自动推送

> 一个由 GitHub Actions 驱动的自动化项目，**每天北京时间 08:00** 自动抓取 GitHub Trending 排行榜，生成精美日报并归档到 `reports/` 目录。

## ✨ 功能

- 🔥 每日自动抓取 GitHub Trending TOP 10 仓库
- 📊 自动统计编程语言分布
- 📝 生成 Markdown 格式的日报，永久归档
- ⚡ 零成本运行，基于 GitHub Actions 免费额度

## 🚀 如何使用

### 方法一：直接使用（推荐）

1. 在 GitHub 上基于此模板创建新仓库，或 Fork 本仓库
2. 进入仓库 **Settings → Actions → General**，开启 Workflow 读写权限
3. 等待每天 08:00 自动运行，或手动触发：**Actions → Daily Hotspot → Run workflow**

### 方法二：本地运行

```bash
git clone https://github.com/2016buhui/daily-hotspot.git
cd daily-hotspot
pip install requests beautifulsoup4
python main.py
```

运行后日报会生成在 `reports/YYYY-MM-DD.md`。

## 📁 项目结构

```
daily-hotspot/
├── .github/workflows/daily-hotspot.yml   # GitHub Actions 工作流
├── main.py                                # 核心脚本：抓取 + 生成日报
├── reports/                               # 日报归档目录（自动生成）
├── requirements.txt
└── README.md
```

## ⚙️ 自定义

- **修改运行时间**：编辑 `.github/workflows/daily-hotspot.yml` 中的 `cron` 表达式
- **抓取其他语言趋势**：在 `main.py` 中调用 `fetch_trending(lang="python")`
- **抓取周/月榜**：修改 `since` 参数为 `weekly` 或 `monthly`

## 📄 License

MIT
