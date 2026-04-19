## Python WebScraping

> 此仓库是所有者 2025-2026 学年第二学期 课程「Python 程序设计」的课程设计。
>
> 此仓库暂时不能够通过简易的方式直接运行，请自行 clone 到本地并在安装 requirement.txt 所要求的依赖库之后手动运行。

### Introduction

此项目使用 [selenium](https://www.selenium.dev/) 作为浏览器的驱动，提供绕过反爬虫进行网页爬取的可能。

- 该部分利用了 selenium 本身提供的自动下载并部署浏览器驱动的功能，同时允许使用本地的浏览器驱动，并且在类 Unix 系统上提供自动查找本地浏览器驱动的服务。

此项目使用 [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) 对网页内容进行解析。

- 该部分针对每个不同的电商网站与不同网站的不同部分做出了逐个适配，使用不同的逻辑算法驱动 BeautifulSoup 过滤。
- 该部分会对所得到的数据进行大量的处理使之能够与数据库所需的类型相匹配。但同时，该部分与数据库部分做出了较为完全的解耦，保证了两部分各自的高度可维护性与可拓展性。

此项目使用 [SQLite](https://sqlite.org/) 作为数据库解决方案，对数据进行管理与存储。

- 该部分由 SQLite 代码手动驱动数据库操作，因此数据库中的数据格式均经过手工严格调整，对数据分析部分保留了充分的兼容性。

### Installation

**此项目仓库暂时设定为 Private**。在确保你拥有此项目的访问权限的情况下，运行**下列命令之一**将仓库克隆到本地：

```shell
git clone https://github.com/Morristin/Python-WebScraping.git
```

```shell
git clone git@github.com:Morristin/Python-WebScraping.git
```

克隆完毕并进入仓库所在地址后，执行下列命令创建虚拟环境：

```shell
python3 -m venv .venv
source .venv/bin/activate # Windows 用户请执行 .venv\Scripts\activate
```

下列命令将更新 pip 并安装本项目所有所需依赖。你可能需要将 `pip` 替换为 `pip3`。

```shell
pip install --upgrade pip
pip install -r requirements.txt
```

需要注意，此项目暂时不能通过简易方式直接运行，因此您需要手动检查安装是否成功。

### LICENSE

This project is licensed under the [MIT License](LICENSE.md).