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

1. 克隆仓库：
```bash
git clone [repository-url]
cd markdown2pdf
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行程序：
```bash
python main.py
```

## 打包说明

本项目使用PyInstaller进行打包，生成单文件可执行程序。打包命令：

```bash
pyinstaller --name="Markdown2PDF" --windowed --icon=icon/logo.png --add-data="wkhtmltox-0.12.6-1.msvc2015-win64.exe;." main.py
```

打包后的文件将在`dist`目录中生成。

## 使用说明

1. 启动程序
2. 选择包含Markdown文件的输入文件夹
3. 选择PDF文件的输出文件夹
4. 可选：输入自定义的页眉和页脚文本
5. 点击"开始转换"按钮开始处理
6. 等待转换完成，程序会自动打开输出文件夹

## 注意事项

- 确保有足够的磁盘空间用于存储生成的PDF文件
- 转换大文件时可能需要等待较长时间
- 如果遇到字体显示问题，请确保系统安装了相应的字体

## 开发计划

- [ ] 添加更多PDF样式自定义选项
- [ ] 支持更多Markdown扩展语法
- [ ] 添加批处理转换配置保存功能
- [ ] 支持更多操作系统平台

## 贡献指南

欢迎提交问题和功能建议！如果您想贡献代码：

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件