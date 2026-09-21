# 108 个种子案例的兼容与领域映射

规划日期：2026-09-21。来源为当前 `video-taxonomy.json`，保留原 ID、名称、Recipe 和文件。
“建议领域”是本次规划标注，不写回运行时目录；并未完成十二维完整标注。
领域定义见 [覆盖计划](COVERAGE_PLAN.md)，多个领域不代表创建重复场景。

每项均只有内容与既有路由测试基线；本文不新增成片、原生导出或宿主验收证据。
后续迁移以这 108 项作为旧版兼容 fixture，不要求每个领域分配相同数量。

## 个人生活 Vlog

| 种子 ID | 原有 example | Recipe | 建议领域 |
| --- | --- | --- | --- |
| VG01 | [日常一天][vg01] | R01 | D01 |
| VG02 | [工作日记][vg02] | R01 | D01 |
| VG03 | [学习记录][vg03] | R01 | D01 |
| VG04 | [创作幕后][vg04] | R01 | D01 |
| VG05 | [挑战成长][vg05] | R01 | D01 |
| VG06 | [搬家生活变化][vg06] | R01 | D01 |

## 旅行与户外

| 种子 ID | 原有 example | Recipe | 建议领域 |
| --- | --- | --- | --- |
| TR01 | [旅行日记][tr01] | R01 | D02 |
| TR02 | [城市漫游][tr02] | R12 | D02 |
| TR03 | [自驾记录][tr03] | R01 | D03/D17 |
| TR04 | [徒步露营][tr04] | R01 | D03 |
| TR05 | [目的地攻略][tr05] | R06 | D02 |
| TR06 | [风光短片][tr06] | R10 | D03/D40 |

## 婚礼与仪式

| 种子 ID | 原有 example | Recipe | 建议领域 |
| --- | --- | --- | --- |
| WD01 | [婚礼预告][wd01] | R02 | D04 |
| WD02 | [当日快剪][wd02] | R02 | D04 |
| WD03 | [爱情故事][wd03] | R02 | D04 |
| WD04 | [仪式全程][wd04] | R03 | D04 |
| WD05 | [誓言致辞精选][wd05] | R07 | D04 |
| WD06 | [求婚订婚记录][wd06] | R02 | D04 |

## 家庭与纪念

| 种子 ID | 原有 example | Recipe | 建议领域 |
| --- | --- | --- | --- |
| FM01 | [亲子成长][fm01] | R02 | D05 |
| FM02 | [生日纪念][fm02] | R02 | D05 |
| FM03 | [毕业回忆][fm03] | R02 | D06 |
| FM04 | [周年纪念][fm04] | R02 | D05 |
| FM05 | [家庭相册影片][fm05] | R02 | D05 |
| FM06 | [追思纪念][fm06] | R02 | D05 |

## 活动与会展

| 种子 ID | 原有 example | Recipe | 建议领域 |
| --- | --- | --- | --- |
| EV01 | [年会回顾][ev01] | R03 | D24 |
| EV02 | [发布会精华][ev02] | R11 | D24 |
| EV03 | [展会巡礼][ev03] | R12 | D24 |
| EV04 | [论坛会议][ev04] | R03 | D24 |
| EV05 | [庆典开幕][ev05] | R03 | D24 |
| EV06 | [公益活动记录][ev06] | R08 | D25 |

## 品牌与组织形象

| 种子 ID | 原有 example | Recipe | 建议领域 |
| --- | --- | --- | --- |
| BR01 | [品牌故事][br01] | R08 | D20 |
| BR02 | [企业形象][br02] | R08 | D20 |
| BR03 | [创始人故事][br03] | R07 | D20 |
| BR04 | [雇主品牌][br04] | R07 | D22 |
| BR05 | [公益倡议][br05] | R08 | D25 |
| BR06 | [品牌周年][br06] | R02 | D20 |

## 广告与电商转化

| 种子 ID | 原有 example | Recipe | 建议领域 |
| --- | --- | --- | --- |
| AD01 | [单品卖点][ad01] | R04 | D21 |
| AD02 | [问题解决广告][ad02] | R04 | D21 |
| AD03 | [使用者体验广告][ad03] | R04 | D21 |
| AD04 | [活动促销][ad04] | R04 | D21 |
| AD05 | [应用获客广告][ad05] | R04 | D16/D21 |
| AD06 | [门店团购推广][ad06] | R04 | D19/D21 |

## 产品与软件

| 种子 ID | 原有 example | Recipe | 建议领域 |
| --- | --- | --- | --- |
| PD01 | [产品开箱][pd01] | R05 | D15 |
| PD02 | [功能演示][pd02] | R05 | D15 |
| PD03 | [对比评测][pd03] | R08 | D15 |
| PD04 | [软件录屏介绍][pd04] | R05 | D16 |
| PD05 | [新功能发布][pd05] | R05 | D15/D16 |
| PD06 | [安装使用指南][pd06] | R06 | D15/D16 |

## 教育与知识

| 种子 ID | 原有 example | Recipe | 建议领域 |
| --- | --- | --- | --- |
| ED01 | [微课][ed01] | R06 | D26 |
| ED02 | [系列课程单节][ed02] | R06 | D26 |
| ED03 | [操作教程][ed03] | R06 | D26 |
| ED04 | [科普解释][ed04] | R08 | D27 |
| ED05 | [题目讲解][ed05] | R06 | D26 |
| ED06 | [实验演示][ed06] | R06 | D27 |

## 企业内部与服务

| 种子 ID | 原有 example | Recipe | 建议领域 |
| --- | --- | --- | --- |
| CO01 | [新员工培训][co01] | R06 | D22 |
| CO02 | [SOP 培训][co02] | R06 | D23 |
| CO03 | [安全培训][co03] | R06 | D23 |
| CO04 | [客户入门][co04] | R06 | D23 |
| CO05 | [常见问题解答][co05] | R06 | D23 |
| CO06 | [内部业务汇报][co06] | R08 | D22 |

## 访谈与播客

| 种子 ID | 原有 example | Recipe | 建议领域 |
| --- | --- | --- | --- |
| IV01 | [人物专访][iv01] | R07 | D33 |
| IV02 | [双人对谈][iv02] | R07 | D33 |
| IV03 | [圆桌讨论][iv03] | R07 | D33 |
| IV04 | [视频播客整期][iv04] | R07 | D33 |
| IV05 | [访谈金句片段][iv05] | R11 | D33 |
| IV06 | [街头采访][iv06] | R07 | D33 |

## 纪录与人物

| 种子 ID | 原有 example | Recipe | 建议领域 |
| --- | --- | --- | --- |
| DC01 | [人物小传][dc01] | R08 | D32 |
| DC02 | [职业纪实][dc02] | R08 | D32 |
| DC03 | [工艺传承][dc03] | R08 | D32/D36 |
| DC04 | [社区故事][dc04] | R08 | D25/D32 |
| DC05 | [自然观察][dc05] | R08 | D40 |
| DC06 | [历史档案叙事][dc06] | R08 | D32 |

## 新闻与公共解释

| 种子 ID | 原有 example | Recipe | 建议领域 |
| --- | --- | --- | --- |
| NW01 | [事件简报][nw01] | R08 | D31 |
| NW02 | [时间线梳理][nw02] | R08 | D31 |
| NW03 | [数据新闻][nw03] | R08 | D31 |
| NW04 | [公共议题解释][nw04] | R08 | D31 |
| NW05 | [现场报道整理][nw05] | R08 | D31 |
| NW06 | [辟谣核查][nw06] | R08 | D31 |

## 剧情与喜剧

| 种子 ID | 原有 example | Recipe | 建议领域 |
| --- | --- | --- | --- |
| ST01 | [剧情短片][st01] | R09 | D34 |
| ST02 | [微短剧单集][st02] | R09 | D34 |
| ST03 | [情景喜剧][st03] | R09 | D34 |
| ST04 | [反转小剧场][st04] | R09 | D34 |
| ST05 | [POV 情境片][st05] | R09 | D34 |
| ST06 | [预告片][st06] | R09 | D34 |

## 音乐与表演

| 种子 ID | 原有 example | Recipe | 建议领域 |
| --- | --- | --- | --- |
| MU01 | [音乐 MV][mu01] | R10 | D35 |
| MU02 | [歌词视频][mu02] | R10 | D35 |
| MU03 | [舞蹈作品][mu03] | R10 | D35 |
| MU04 | [乐器演奏][mu04] | R10 | D35 |
| MU05 | [演唱会精选][mu05] | R10 | D35 |
| MU06 | [舞台完整节目][mu06] | R03 | D35 |

## 体育与游戏

| 种子 ID | 原有 example | Recipe | 建议领域 |
| --- | --- | --- | --- |
| SG01 | [赛事集锦][sg01] | R11 | D13 |
| SG02 | [运动员故事][sg02] | R08 | D13 |
| SG03 | [动作教学][sg03] | R06 | D13 |
| SG04 | [电竞精彩片段][sg04] | R11 | D14 |
| SG05 | [游戏攻略][sg05] | R06 | D14 |
| SG06 | [游戏实况精编][sg06] | R11 | D14 |

## 空间与资产展示

| 种子 ID | 原有 example | Recipe | 建议领域 |
| --- | --- | --- | --- |
| SP01 | [房源导览][sp01] | R12 | D18 |
| SP02 | [酒店民宿][sp02] | R12 | D19 |
| SP03 | [建筑空间][sp03] | R12 | D18 |
| SP04 | [家居改造][sp04] | R12 | D10/D18 |
| SP05 | [展馆导览][sp05] | R12 | D36 |
| SP06 | [车辆展示][sp06] | R05 | D17 |

## 制作过程与体验

| 种子 ID | 原有 example | Recipe | 建议领域 |
| --- | --- | --- | --- |
| PR01 | [菜谱制作][pr01] | R06 | D07 |
| PR02 | [餐饮体验][pr02] | R01 | D07 |
| PR03 | [手工制作][pr03] | R06 | D11 |
| PR04 | [维修翻新][pr04] | R06 | D11 |
| PR05 | [妆造过程][pr05] | R06 | D09 |
| PR06 | [园艺种植][pr06] | R06 | D12 |

[vg01]: ../../skills/jianying-video-planning/examples/scenarios/vg01.md
[vg02]: ../../skills/jianying-video-planning/examples/scenarios/vg02.md
[vg03]: ../../skills/jianying-video-planning/examples/scenarios/vg03.md
[vg04]: ../../skills/jianying-video-planning/examples/scenarios/vg04.md
[vg05]: ../../skills/jianying-video-planning/examples/scenarios/vg05.md
[vg06]: ../../skills/jianying-video-planning/examples/scenarios/vg06.md
[tr01]: ../../skills/jianying-video-planning/examples/scenarios/tr01.md
[tr02]: ../../skills/jianying-video-planning/examples/scenarios/tr02.md
[tr03]: ../../skills/jianying-video-planning/examples/scenarios/tr03.md
[tr04]: ../../skills/jianying-video-planning/examples/scenarios/tr04.md
[tr05]: ../../skills/jianying-video-planning/examples/scenarios/tr05.md
[tr06]: ../../skills/jianying-video-planning/examples/scenarios/tr06.md
[wd01]: ../../skills/jianying-video-planning/examples/scenarios/wd01.md
[wd02]: ../../skills/jianying-video-planning/examples/scenarios/wd02.md
[wd03]: ../../skills/jianying-video-planning/examples/scenarios/wd03.md
[wd04]: ../../skills/jianying-video-planning/examples/scenarios/wd04.md
[wd05]: ../../skills/jianying-video-planning/examples/scenarios/wd05.md
[wd06]: ../../skills/jianying-video-planning/examples/scenarios/wd06.md
[fm01]: ../../skills/jianying-video-planning/examples/scenarios/fm01.md
[fm02]: ../../skills/jianying-video-planning/examples/scenarios/fm02.md
[fm03]: ../../skills/jianying-video-planning/examples/scenarios/fm03.md
[fm04]: ../../skills/jianying-video-planning/examples/scenarios/fm04.md
[fm05]: ../../skills/jianying-video-planning/examples/scenarios/fm05.md
[fm06]: ../../skills/jianying-video-planning/examples/scenarios/fm06.md
[ev01]: ../../skills/jianying-video-planning/examples/scenarios/ev01.md
[ev02]: ../../skills/jianying-video-planning/examples/scenarios/ev02.md
[ev03]: ../../skills/jianying-video-planning/examples/scenarios/ev03.md
[ev04]: ../../skills/jianying-video-planning/examples/scenarios/ev04.md
[ev05]: ../../skills/jianying-video-planning/examples/scenarios/ev05.md
[ev06]: ../../skills/jianying-video-planning/examples/scenarios/ev06.md
[br01]: ../../skills/jianying-video-planning/examples/scenarios/br01.md
[br02]: ../../skills/jianying-video-planning/examples/scenarios/br02.md
[br03]: ../../skills/jianying-video-planning/examples/scenarios/br03.md
[br04]: ../../skills/jianying-video-planning/examples/scenarios/br04.md
[br05]: ../../skills/jianying-video-planning/examples/scenarios/br05.md
[br06]: ../../skills/jianying-video-planning/examples/scenarios/br06.md
[ad01]: ../../skills/jianying-video-planning/examples/scenarios/ad01.md
[ad02]: ../../skills/jianying-video-planning/examples/scenarios/ad02.md
[ad03]: ../../skills/jianying-video-planning/examples/scenarios/ad03.md
[ad04]: ../../skills/jianying-video-planning/examples/scenarios/ad04.md
[ad05]: ../../skills/jianying-video-planning/examples/scenarios/ad05.md
[ad06]: ../../skills/jianying-video-planning/examples/scenarios/ad06.md
[pd01]: ../../skills/jianying-video-planning/examples/scenarios/pd01.md
[pd02]: ../../skills/jianying-video-planning/examples/scenarios/pd02.md
[pd03]: ../../skills/jianying-video-planning/examples/scenarios/pd03.md
[pd04]: ../../skills/jianying-video-planning/examples/scenarios/pd04.md
[pd05]: ../../skills/jianying-video-planning/examples/scenarios/pd05.md
[pd06]: ../../skills/jianying-video-planning/examples/scenarios/pd06.md
[ed01]: ../../skills/jianying-video-planning/examples/scenarios/ed01.md
[ed02]: ../../skills/jianying-video-planning/examples/scenarios/ed02.md
[ed03]: ../../skills/jianying-video-planning/examples/scenarios/ed03.md
[ed04]: ../../skills/jianying-video-planning/examples/scenarios/ed04.md
[ed05]: ../../skills/jianying-video-planning/examples/scenarios/ed05.md
[ed06]: ../../skills/jianying-video-planning/examples/scenarios/ed06.md
[co01]: ../../skills/jianying-video-planning/examples/scenarios/co01.md
[co02]: ../../skills/jianying-video-planning/examples/scenarios/co02.md
[co03]: ../../skills/jianying-video-planning/examples/scenarios/co03.md
[co04]: ../../skills/jianying-video-planning/examples/scenarios/co04.md
[co05]: ../../skills/jianying-video-planning/examples/scenarios/co05.md
[co06]: ../../skills/jianying-video-planning/examples/scenarios/co06.md
[iv01]: ../../skills/jianying-video-planning/examples/scenarios/iv01.md
[iv02]: ../../skills/jianying-video-planning/examples/scenarios/iv02.md
[iv03]: ../../skills/jianying-video-planning/examples/scenarios/iv03.md
[iv04]: ../../skills/jianying-video-planning/examples/scenarios/iv04.md
[iv05]: ../../skills/jianying-video-planning/examples/scenarios/iv05.md
[iv06]: ../../skills/jianying-video-planning/examples/scenarios/iv06.md
[dc01]: ../../skills/jianying-video-planning/examples/scenarios/dc01.md
[dc02]: ../../skills/jianying-video-planning/examples/scenarios/dc02.md
[dc03]: ../../skills/jianying-video-planning/examples/scenarios/dc03.md
[dc04]: ../../skills/jianying-video-planning/examples/scenarios/dc04.md
[dc05]: ../../skills/jianying-video-planning/examples/scenarios/dc05.md
[dc06]: ../../skills/jianying-video-planning/examples/scenarios/dc06.md
[nw01]: ../../skills/jianying-video-planning/examples/scenarios/nw01.md
[nw02]: ../../skills/jianying-video-planning/examples/scenarios/nw02.md
[nw03]: ../../skills/jianying-video-planning/examples/scenarios/nw03.md
[nw04]: ../../skills/jianying-video-planning/examples/scenarios/nw04.md
[nw05]: ../../skills/jianying-video-planning/examples/scenarios/nw05.md
[nw06]: ../../skills/jianying-video-planning/examples/scenarios/nw06.md
[st01]: ../../skills/jianying-video-planning/examples/scenarios/st01.md
[st02]: ../../skills/jianying-video-planning/examples/scenarios/st02.md
[st03]: ../../skills/jianying-video-planning/examples/scenarios/st03.md
[st04]: ../../skills/jianying-video-planning/examples/scenarios/st04.md
[st05]: ../../skills/jianying-video-planning/examples/scenarios/st05.md
[st06]: ../../skills/jianying-video-planning/examples/scenarios/st06.md
[mu01]: ../../skills/jianying-video-planning/examples/scenarios/mu01.md
[mu02]: ../../skills/jianying-video-planning/examples/scenarios/mu02.md
[mu03]: ../../skills/jianying-video-planning/examples/scenarios/mu03.md
[mu04]: ../../skills/jianying-video-planning/examples/scenarios/mu04.md
[mu05]: ../../skills/jianying-video-planning/examples/scenarios/mu05.md
[mu06]: ../../skills/jianying-video-planning/examples/scenarios/mu06.md
[sg01]: ../../skills/jianying-video-planning/examples/scenarios/sg01.md
[sg02]: ../../skills/jianying-video-planning/examples/scenarios/sg02.md
[sg03]: ../../skills/jianying-video-planning/examples/scenarios/sg03.md
[sg04]: ../../skills/jianying-video-planning/examples/scenarios/sg04.md
[sg05]: ../../skills/jianying-video-planning/examples/scenarios/sg05.md
[sg06]: ../../skills/jianying-video-planning/examples/scenarios/sg06.md
[sp01]: ../../skills/jianying-video-planning/examples/scenarios/sp01.md
[sp02]: ../../skills/jianying-video-planning/examples/scenarios/sp02.md
[sp03]: ../../skills/jianying-video-planning/examples/scenarios/sp03.md
[sp04]: ../../skills/jianying-video-planning/examples/scenarios/sp04.md
[sp05]: ../../skills/jianying-video-planning/examples/scenarios/sp05.md
[sp06]: ../../skills/jianying-video-planning/examples/scenarios/sp06.md
[pr01]: ../../skills/jianying-video-planning/examples/scenarios/pr01.md
[pr02]: ../../skills/jianying-video-planning/examples/scenarios/pr02.md
[pr03]: ../../skills/jianying-video-planning/examples/scenarios/pr03.md
[pr04]: ../../skills/jianying-video-planning/examples/scenarios/pr04.md
[pr05]: ../../skills/jianying-video-planning/examples/scenarios/pr05.md
[pr06]: ../../skills/jianying-video-planning/examples/scenarios/pr06.md
