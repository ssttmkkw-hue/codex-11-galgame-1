# 生成记录与扩图方法

生成工具：内置 `image_gen.imagegen`。本轮由空仓库开始建立原创题材，未使用第三方角色或素材站图片。生成日期：2026-11-22。

## 生产顺序

1. 独立生成夏澄与澪的角色设计参考图，确立成年身份、发型、服装、色板和标志配饰。
2. 分别以设计图作参考，生成一张透明全身中性表情立绘，作为生产主参考。
3. 每一种表情均重新引用对应 `neutral.png`，要求只改变眼、眉、嘴、脸红或泪水，保留镜头、身形、衣装、持物、手势及透明背景；不从上一张差分逐级转绘，避免累积偏移。
4. 海堤与咖啡馆先生成日景，再引用基础场景生成夕照／雨天变化。其余地点统一依照视觉设定绘制。
5. CG 引用对应角色立绘与对应场景；双人主视觉引用两位生产立绘。
6. 将原始输出复制进规范目录，保留原始 PNG，并检查尺寸、Alpha 和文件完整性。

## 提示词核心

角色绘制共同约束：`original Japanese visual novel, adult woman, premium clean anime line art, refined soft cel painting, consistent identity and outfit, one full-body character, complete shoes and hair, portrait 1024x1536, transparent RGBA background, no lettering, no floor, no cast shadow`。

表情差分共同约束：`edit the neutral production sprite, change only eyes, eyebrows, mouth and subtle blush or tears, preserve exact pose, proportions, all accessories, hands and canvas, no extra gestures or symbols, transparent background`。

六类表情的含义：

- neutral：眼睛睁开、闭嘴、自然倾听。
- smile：明亮眼神、张嘴微笑、放松眉形。
- shy：明显脸红、视线稍移、克制闭嘴微笑。
- surprised：睁大眼睛、抬眉、小幅 O 型嘴。
- serious：眉头收紧、坚定目光、紧闭嘴唇。
- sad：内侧抬眉、含泪眼神、一条细泪痕、小幅颤抖嘴形。

背景共同约束：`cozy coastal summer town, delicate architectural linework, hand-painted anime background, subtle watercolor texture, coherent standing eye-level perspective, turquoise sea, cream walls, weathered warm wood, lavender shadows, open center foreground, no people, no text, no UI, landscape 1536x1024, center 16:9 safe area`。

每个角色的不可变细节和八处场景的用途见 [美术设定](art-direction.md)。

## 使用边界

此版本交付单套日常服装、单个站姿、六种剧情表情。全套素材是统一主题的首轮美术包；最终剧本若新增泳装、节庆、跑动、拥抱、额外地图或更多结局事件，应新增相应原画。当前没有声称覆盖尚未编写的完整游戏内容。

生成图不包含可编辑 PSD 分层、面部精确遮罩或 Live2D 骨架。原生 PNG 的轻微轮廓和配饰漂移已在接入文档说明，不应假设达到手工逐像素校准。
