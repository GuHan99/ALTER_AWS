# ALTER_AWS
1.第一步去aws IAM里面添加配置一个user，获得这个user的AWS Access Key ID, AWS Secret Access Key<br>
2.把ec2实例建好，至少3个<br>
3.电脑上装python3.7，aws-cli/2.0.24，boto3(一个python的aws库)<br>
4.进入windows的cmd 敲aws configure，分别把 <br>AWS Access Key ID, AWS Secret Access Key，<br>Region（实例的地点），<br>Format（输出文件形式，就yaml，其实都随便））都填了<br>
5.用test.py测一下，能用的话说明之前的步骤都对了<br>
6.运行run.py，键盘输入，A就是轮换制，轮换制现在设定是每15s才能换一次ip。<br>但是实际aws的响应速度可能不止这个时间。<br>如果中间显示有错误，那程序就要先按B全关再重新运行run.py了。如果切换很慢（30s切换一次？），那可以一直运行。
B模式全开，全关，再重新运行run.py。<br>运行比A模式稳定。就是要一直手动切换。<br>
记住重新运行run.py要等上一次程序结束过一会（也是15s左右）。还是aws的响应问题。<br>
只要用的速度慢程序是没问题的。
