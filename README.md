## Python WebScraping

> 此仓库是所有者 2025-2026 学年第二学期 课程「Python 程序设计」的课程设计。

本 `main` 分支开发进度已经落后于 `interact` 分支。请耐心等待仓库完成两分支的 merge。

如果你具有一定的 python 操作能力，请访问 interact 分支：https://github.com/Morristin/Python-WebScraping/tree/interact 。

### Installation

运行**下列命令之一**可以将仓库克隆到本地：
（在命令末尾添加 `--depth=1` 参数表示仅 clone 最后一次提交，从而加速 clone 仓库的过程。）

```shell
# 任选其一指令执行。第一行使用 HTTPS 协议，第二行使用 SSH 协议。
git clone https://github.com/Morristin/Python-WebScraping.git --depth=1
git clone git@github.com:Morristin/Python-WebScraping.git --depth=1
```

克隆完毕并进入仓库所在地址后，执行下列命令创建虚拟环境并使用 pip 安装本项目所有所需依赖：

```shell
python3 -m venv .venv
source .venv/bin/activate # Windows 用户请执行 .venv\Scripts\activate

pip install -e .
```

在安装完成所需依赖后，可以使用命令行与程序进行交互。具体交互方式可以在上述指令执行的位置运行如下命令获得：

```shell
python3 main.py --help
```

### Introduction

此项目使用 [selenium](https://www.selenium.dev/) 作为浏览器的驱动，提供绕过反爬虫进行网页爬取的可能。

- 该部分利用了 selenium 本身提供的自动下载并部署浏览器驱动的功能，同时允许使用本地的浏览器驱动，并且在类 Unix
  系统上提供自动查找本地浏览器驱动的服务。

此项目使用 [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) 对网页内容进行解析。

- 该部分针对每个不同的电商网站与不同网站的不同部分做出了逐个适配，使用不同的逻辑算法驱动 BeautifulSoup 过滤。
- 该部分会对所得到的数据进行大量的处理使之能够与数据库所需的类型相匹配。
  但同时，该部分与数据库部分做出了较为完全的解耦，保证了两部分各自的高度可维护性与可拓展性。

此项目使用 [SQLite](https://sqlite.org/) 作为数据库解决方案，对数据进行管理与存储。

- 该部分由 SQLite 代码手动驱动数据库操作，因此数据库中的数据格式均经过手工严格调整，对数据分析部分保留了充分的兼容性。

此项目集成 [Ollama](https://ollama.com/) 对非结构化数据进行解析。

- 该部分在测试使用了于 macOS 部署的 qwen3.5:0.8b。该部分有待进一步优化，你可以自行调整 `settings` 中的 prompt 文件。

### Road Map

- [x] 新增程序命令行交互功能以方便用户快速上手。
- [x] 完善对爬取到的商品价格进行处理的算法。
- [ ] 从数据库中读取数据并进行可视化分析和数学建模。

### LICENSE

This project is licensed under the [MIT License](LICENSE.md).