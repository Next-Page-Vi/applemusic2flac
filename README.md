# AppleMusic2FLAC

一个专门用于转换 zhaarey/apple-music-downloader 下载的 ALAC 音频文件转换为 FLAC 格式的工具，主要服务于 DIC(OPS，没有 RED 所以不确定) 的发种要求。

## 功能特点

- 制作符合要求的FLAC文件，保留符合 Vorbis Comments 的元数据；
- 目前版本去掉了内嵌封面，防止大体积内嵌封面附件违规；
- 自动识别 Apple Music 的虚高比特深度（24bit），转换时保留为正确的；
- 重命名结果大概率满足站点要求（复杂艺术家专辑请手动编辑）；
- 绝大多数情况满足 propolis 检查（我没遇到 KO 的）。

## 使用步骤

1. 需要安装 FFmpeg 并释放在环境变量中：

2. 克隆此仓库：
   git clone https://github.com/yourusername/applemusic2flac.git
   
## 饼

- [ ] 自定义命名方式以符合其他拍脑门定下命名规则的站点；
- [ ] 输出 Gazelle Json；
- [ ] 输出频谱图并自动上传到图床（你可以结合 propolis 实现）；
- [ ] 自动填写表单到 NexusPHP 架构的站点。