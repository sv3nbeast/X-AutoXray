* Usage: 在Xray和rad同目录下运行 python3 X-AutoXray.py xxxx.txt
* 1. 写的蛮人性化的哦，os,linux,windows通用
* 2. 生成的xray报告会在当前目录的/result下面
* 3. Ctrl+c  打断脚本运行时还可以结算扫描进度，生成已扫描和未扫描的进度文件，让你第二天上班时继续当一名xray工程师

![](./run.png)


#### 2020·12·26 更新历史
  * 增加文件名检测，防止重复扫描时忘记删除之前的扫描报告
  * 修复windows的颜色模块不正常显示
  * 修复windows的兼容问题
