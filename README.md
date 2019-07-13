
爬取的信息格式   可参考 project.csv

可根据具体信息需求对脚本进行调整，以适应任务 \
由于是临时的任务，所以选取了selenium的方法来进行爬虫（比较low），如果有大神有想法，可以重构 \


### 前提准备
# 这里的chromedriver要根据你自己的chrome版本来匹配

sudo cp chromedriver /usr/bin/

sudo chmod a+x /usr/bin/chromedriver \

pip3 install selenium

### 

### 使用说明
需要提前将搜索的关键字，选项手动选好搜索之后将url网址替换到.py文件中相应的url变量赋值，并且要将该搜索情况下的页数填入page_num,根据自己的cpu性能填写threadNum数量（这将影响你的爬虫完成速度)
总结来说 \ 
        1.设置url \
        2.设置page_num \
        3.设置threadNum \
使用之前只需设置好这三个参数就可以开始跑了 ubuntu/windows 中终端里 python3 ccgp_gov.py 即可
####


### 特殊的情况

1.中国政府采购网 有些 预算金额并没有完全按照 统一的格式来填写，有些是需要跳转到公告正文处来查看，而公告正文的形式并不统一，所以这一部分的信息需要手动填入 \
2.信息采集的页面大多数是以统一的表格形式呈现的，但有部分信息是直接以非统一标准格式的公告正文展示的，这部分比较少但存在，对于这一部分爬虫采集较为困难，非标准版面，标识用词也不统一，所以遇到这种情况，csv文件中都以"异常版面，需手动标注"进行填充，但相应的网址正常保留，这一部分也是需要大家手动填入的 \

如果有大神可以帮助改进当然更好
###



