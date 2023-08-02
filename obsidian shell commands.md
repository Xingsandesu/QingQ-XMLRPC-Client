Copy-Item -Path "你的草稿文件夹绝对路径\{{file_name}}" -Destination "你的Typecho Push API文件夹绝对路径";
Start-Sleep -Seconds 61;
Remove-Item  -Path  "你的Typecho Push API文件夹绝对路径\{{file_name}}"

# 在obsidian中安装shell commands插件，选择powershell运行，使用这个命令自动copy并删除，可以保存快捷键，写完文章后，使用快捷键，配合remotely save每分钟自动保存，实现自动上传自动清理
