一、如果想用flash工具刷最新小智升级固件，下载和使用附件的几个文件即可；

二、如果是软硬件开发人员需要自己编辑源代码，可以看以下链接资料。

三、想要在线刷为最新的小智升级固件，可进入赛搏智能专用网页烧录 （v2.0硬件版本喵伴烧录时要一直按着电源键）https://flash.cyberai.top/

四、原理图在附件三个PDF，赛博喵伴 V2.0硬件版本
v2.1硬件版本PDF原理图在下面第五条这个链接里

五、（重要）赛博喵伴的开源工程：https://github.com/cyberai8/cyberkit
该源码最新适配
2026年9月15日-最新购买的喵伴（V2.1硬件）
2026年5月28日-2026年9月15日购买的喵伴（V2.0硬件）
也同样适配2025年9月-2026年5月之间购买的喵伴（V1.2硬件）


源代码及小智AI系统相关参考资料：

1、小智开源项目介绍与源代码
https://ai.feishu.cn/wiki/F5krwD16viZoF0kKkvDcrZNYnhb
2、小智AI聊天系统常见问题Q&A
https://ai.feishu.cn/wiki/JiQowaSe1itt07kyVvZcHFcQnee
3、ESP-IDF编译源代码步骤（适合开发人员）
https://icnynnzcwou8.feishu.cn/wiki/JEYDwTTALi5s2zkGlFGcDiRknXf
4、最新源代码地址
https://ai.feishu.cn/wiki/W14Kw1s1uieoKjkP8N0c1VVvn8d
5、MCP能力开发说明
https://ai.feishu.cn/wiki/HiPEwZ37XiitnwktX13cEM5KnSb
6、更改唤醒词相关说明
https://ai.feishu.cn/wiki/H4dywK6ucigEtykKmm3cmZ7Dnog
7、主机乐鑫官方源代码仓库（带doa算法和番茄闹钟等）
https://gitee.com/esp-friends/esp-echo-ear-xiaozhi
8、底座乐鑫官方源代码仓库（带doa算法和磁吸控制等）
https://gitee.com/esp-friends/esp-echoear-base
需要注意的是赛搏科技底座为ESP32-C3主控，官方为ESP32-C61主控，编译的时候注意选择。
9、乐鑫官方硬件资源详解（赛搏科技喵伴兼容最新的V1.2设计）
https://docs.espressif.com/projects/esp-dev-kits/zh_CN/latest/esp32s3/echoear/user_guide_v1.2.html
10、乐鑫官方开源PCB工程文件原理图等资料
https://oshwhub.com/esp-college/echoear
11、Arduino小智，编译视频教程
【【开源】AI-你好小智-Arduino版程序使用教程-哔哩哔哩】 https://b23.tv/rvBQmsP
12、ESP-IDF 小智，编译视频教程（推荐）
【从零开始，配置小智代码编译环境（vscode和esp-idf）-哔哩哔哩】 https://b23.tv/eMyFjcf
要配合第五项：“五、（重要）赛博喵伴的开源工程”使用

开源的固件说明：
赛搏喵伴_主机_v2.0.5.4.bin
版本发布日期：20260106
1、陀螺仪开关，默认为开，语音指令：打开/关闭 摇晃感应开关；
2、头顶触摸感应，默认为关，语音指令：打开/关闭 头顶触摸感应；
3、网络音乐播放能力；
4、UI界面：左右滑动设置番茄时钟、猫咪倒计时功能；
5、升级DOA算法（需配合底座）；
6、自动OTA能力；
7、音乐律动模式，默认为关，语音指令：进入\关闭 音乐律动模式。
8、SD卡音乐播放能力；
9、实时对话模式，语音指令：打开实时对话模式。