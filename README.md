# AutoOrderBus
自动预约万柳校车
个人学习用request访问学习网页以及gitflow的项目

### 使用方式
#### 1. 配置预约班车信息
在[config.ini](https://github.com/yyhyv0/AutoOrderBus/blob/master/config.ini)中配置需要预约的早班车和晚班车。
不需要预约时，请填写"none"。
#### 2. 配置身份信息
在github的**settings->security->secrets->Actions secrets->New repository secret**中[添加SECRET](https://docs.github.com/cn/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository)。

##### SECRET内容

| Name     |                Description                 |
| -------- | :----------------------------------------: |
| USER |                 学号(必须)                 |
| PASSWORD|                 密码(必须)                 |
| SENDKEY |[虾推啥](https://http://www.xtuis.cn/)SENDKEY,不需要推送时随便写个数字  |

#### 3.配置微信推送(可选)
使用[虾推啥](https://http://www.xtuis.cn/)推送预约信息，需要将[配置文件](https://github.com/yyhyv0/AutoOrderBus/blob/master/config.ini)的notification改为True，同时在SECRET中加入SENDKEY.

#### 4.配置workflow
**actions->select workflow->AutoOrderBus**

注：默认在每天15:05分预约校车，如需修改请按格式要求修改[main.yml](https://github.com/yyhyv0/AutoOrderBus/blob/master/.github/workflows/main.yml)文件中的**on.schedule.cron**项。