# Markdown批量转PDF工具

一个基于Python开发的批量Markdown转PDF工具，支持自定义页眉页脚，提供友好的图形界面。
![1.png](resources%2F1.png)
## 技术栈

- **Python 3.11**
- **PyQt5**: 用于构建现代化的图形用户界面
- **markdown2**: 提供Markdown到HTML的转换功能
- **pdfkit**: 提供HTML到PDF的转换功能
- **wkhtmltopdf**: PDF生成引擎

## 功能特性

- 批量转换：支持将整个文件夹的Markdown文件批量转换为PDF
- 自定义页眉页脚：可以为生成的PDF文件添加自定义的页眉和页脚
- 实时进度显示：转换过程中显示实时进度
- 自动页码：自动在PDF文件中添加页码
- 优雅的界面：简洁直观的用户界面，易于操作
- 智能路径检测：自动检测和配置wkhtmltopdf工具路径

## 环境要求

- Windows操作系统（已在Windows 10/11上测试）
- Python 3.6+
- wkhtmltopdf（程序会自动安装或使用系统已安装的版本）

## 安装使用

### 方式一：直接使用打包版本

1. 从发布页面下载最新的打包版本
2. 解压后直接运行`Markdown2PDF.exe`

### 方式二：从源码运行
