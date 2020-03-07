# 挑战答题

## 免责申明
`AutoXue`为本人`Python`学习交流的开源非营利项目，仅作为`Python`学习交流之用，使用需严格遵守开源许可协议。严禁用于商业用途，禁止使用`AutoXue`进行任何盈利活动。对一切非法使用所产生的后果，本人概不负责。

## 环境准备[下载](http://49.235.90.76:5000/downloads)
0. 如果之前添加过环境变量`ADB1.0.40`请确保删除之
1. 安装`JDK`，本文使用JDK1.8
    + 在环境变量中新建`JAVA_HOME`变量，值为JDK安装路径，如`C:\Program Files\Java\jdk1.8.0_05`
    + 新建`CLASSPATH`变量，值为`.;%JAVA_HOME%\lib;%JAVA_HOME%\lib\tools.jar;`
    + `Path`变量中添加：`%JAVA_HOME%\bin和%JAVA_HOME%\jre\bin`
2. 安装`SDK`，本文使用SDK r24.4.1
    + 在环境变量中新建`ANDROID_HOME`，值为SDK安装路径，如`C:\Program Files (x86)\Android\android-sdk`
    + 在Path变量中添加项：`%ANDROID_HOME%\platform-tools` 和 `%ANDROID_HOME%\tools`
    + 打开`SDK Manager.exe` 安装对应的工具和包

3. 安装`Appium-desktop`，为了使用`UiAutomator2`，请将`Appium`设为以管理员权限启动，并赋予JDK和SDK所有权限
4. 安装一个模拟器，就选夜神Nox吧，如用其他模拟器或真机出现问题请自救。
5. 安装`Python`，请至少使用3.7+版本，推荐3.8

## 使用方法(windows)
0. 克隆项目 `git clone https://github.com/kessil/AutoXue.git --depth 1`
1. 双击运行`setup.cmd`
2. 启动 `Appium` 和 `Nox`
3. 双击运行 `start.cmd`

## 写在最后
+ 在[这里](http://49.235.90.76:5000/downloads)可能有您需要的安装包，你可以官方网站下载使用最新版本，也可在[这里](http://49.235.90.76:5000/downloads)下载（未必最新版）
+ 强烈建议需要自定义配置文件的用户下载使用vscode编辑器,[why vscode?](https://hacpai.com/article/1569745141957)，请一定不要使用系统自带记事本修改配置文件。

