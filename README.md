# Overview
  Tracking爬虫系统是基于Scrapy框架开发的，爬取闻成就各个公众号，在各大社交平台发布的视频追踪数据，如公众号粉丝数，视频播放量、转发量、收藏量、阅读量、评论量等。
# Architecture
  Tracking爬虫代码目录如下
   - tracking
      - spiders
        - platform1
          - platform1_taskName1_task.py
          - platform1_taskName2_task.py
        - platform2
          - platform2_taskName1_task.py
      - util
        - utils.py
      - items.py
      - settings.py
      - ...

  Tracking爬虫任务在spiders目录下：
     1. 为每个视频平台分别建立独立的文件夹，命名规则为该视频平台的域名或简写，必须使用小写字母命名，如微博平台命名为”weibo“;
     2. 每个文件夹下为该平台的爬虫任务，任务文件命名规则为“上级文件夹名称_任务名称_task”，如微博平台的tracking任务文件命名为“weibo_tracking_task”
     3. 每个爬虫任务的name属性必须与该任务的文件名相同，如如微博平台的tracking任务中”name“命名为该文件的名称“weibo_tracking_task”， 其他辅助Python文件不以“\_task”结尾即可。<br />

   以上命名规则与Jenkins任务密切相关，违反规则将导致爬虫任务不能自动部署。

# Deployment
  爬虫任务通过Jenkins-DSL任务自动部署，参见: http://117.78.50.217:8080/view/seed/job/Jobs_Seed/
  Jobs_Seed任务是自动部署Tracking爬虫任务的Jenkins-DSL任务，它的工作流程如下：
    1. 通过shell脚本读取tracking git source的对应branch
      a. 读取源代码“spders”目录下的所有folder(即视频平台目录)，将所有folder名称存储在"seed.views"文件中
      b. 读取每个folder(即视频平台目录)下的爬虫任务文件（以folder名称开头，以“\_task”结尾的文件），将所有任务名称存储在"seed.jobs"文件中
    2. 通过DSL脚本，自动创建爬虫任务
      a. 通过yaml文件设置爬虫任务参数，如schedule，git source，archive等
      b. 遍历seed.views文件，创建Jenkins的list view，并设置正则规则，将以view名称开头的任务显示在该view中
      c. 遍历seed.jobs文件，并读取步骤a中参数文件，通过groovy脚本创建Jenkins job
