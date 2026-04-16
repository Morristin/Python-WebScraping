## Python WebScraping

> 此仓库是所有者 2025-2026 学年第二学期 课程「Python 程序设计」的课程设计。
>
> 此仓库不能够通过简易的方式直接运行，请自行 clone 到本地并在安装 requirement.txt 所要求的依赖库之后手动运行。

### Introduction

此项目使用 [selenium](https://www.selenium.dev/) 作为浏览器的驱动，提供绕过反爬虫进行网页爬取的可能。

- 此项目允许使用本地的浏览器驱动，并且在类 Unix 系统上提供自动查找本地浏览器驱动的服务。
- 此项目利用了 selenium 本身提供的自动下载并部署浏览器驱动的功能。

此项目使用 [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) 对网页内容进行解析。

- **该部分内容有待进一步开发**。

### Installation

**此项目仓库暂时设定为 Private**。在确保你拥有此项目的访问权限的情况下，运行**下列命令之一**将仓库克隆到本地：

```shell
git clone https://github.com/Morristin/Python-WebScraping.git
```

```shell
git clone git@github.com:Morristin/Python-WebScraping.git
```

克隆完毕并进入仓库所在地址后，执行下列命令创建虚拟环境并安装相关依赖：

```shell
python3 -m venv .venv
source .venv/bin/activate # Windows 用户请执行 .venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt
```

需要注意，此项目暂时不能通过简易方式直接运行，因此您需要手动检查安装是否成功。

### LICENSE

This project is liensed under the [MIT License](LICENSE.md).