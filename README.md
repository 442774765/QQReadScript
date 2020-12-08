## 描述
一个使用 `Python` 语言写的薅羊毛脚本仓库，支持 `github action` 和 `linux/windows virtual private server` 

## 部署方式
**注意**：所有脚本任务都是未启用并且默认不发消息推送，请自行根据自身需求设置，配置文件采用 `yaml` 语法编写（注意空格），建议使用文本编辑器填写配置，以防格式错误！  
### linux/windows virtual private server
* `git clone https://github.com/TNanko/Scripts.git`
* 安装脚本所需要的包 `pip3 install -r requirements.txt`
* 复制文件夹 `config` 下的 `config.yml.example` 文件并将文件命名为 `config.yml` （`cp config.yml.example config.yml`）。使用 `vi` 或者文本编辑器编辑文件 `config.yml` 填写配置  
* 在配置文件中填写对应的推送方式的 `key` 或者 `code`  
* 找到想要运行的脚本，设置对应的配置信息  
* 运行脚本 `python3 ./scripts/xxx.py`

### github action
* 添加一个 `secrets` - `CONFIG` ， `Value` 内容请复制目录下 `./config/config.yml.example` 所有内容  
* 填写对应的推送方式的 `key` 或者 `code`  
* 找到想要运行的脚本，设置对应的配置信息
* 手动 `star` 一下仓库，看下 `Action` 是否正常运行
#### 定时同步仓库
* 添加一个 `secrets` - `PAT` ，[教程](https://www.jianshu.com/p/bb82b3ad1d11)

## 消息推送
目前支持 `ios bark app` ， `telegarm bot` ， `dingding bot` ， `serverJ` 四种方式推送消息。    
打开推送方式：将 `config.yml` 里面 `notify` 选项中，参数 `enable` 设置为 `true`    

## 支持的脚本任务
* 企鹅读书 脚本地址：https://raw.githubusercontent.com/TNanko/Scripts/master/scripts/qq_read.py
  <details>
  <summary>教程</summary>
  进入脚本地址 https://raw.githubusercontent.com/TNanko/Scripts/master/scripts/qq_read.py 获取参数，然后根据 https://raw.githubusercontent.com/TNanko/Scripts/master/config/config.yml.example 将参数填入对应的位置并且配置其他设置。
  </details>
* `bilibili` 签到 脚本地址：https://raw.githubusercontent.com/TNanko/Scripts/master/scripts/bilibili.py