# Xiang Li · CharlyX

Personal homepage: **https://charlyx-lee.github.io/**

A bilingual academic and campus portfolio with a dark starry background, animated moon avatar, and responsive layout. The default is English / Research; language and Research / Campus can be switched independently.

## 在 GitHub 中更新主页

1. 打开 `index.html`，点击编辑按钮，修改文字后提交到 `main`。
2. GitHub Pages 会自动发布，完成后刷新主页即可看到更新。
3. 英文内容位于 `class="lang-en"` 区域，中文内容位于 `class="lang-zh"` 区域；建议同时维护两种语言。

Research 依次展示论文成果、教育经历、科研经历、实习经历、学术任职、专业技能。Campus 依次展示教育经历、学生工作任职、荣誉称号、奖学金、竞赛经历。

| 修改内容 | 文件 |
| --- | --- |
| 页面文字、论文、经历与链接 | `index.html` |
| 字号、颜色、布局和动画样式 | `style.css` |
| 语言、视图、导航和动画行为 | `script.js` |
| 中文简历 PDF | `assets/Xiang-Li-CV.pdf` |
| 简历预览页 | `cv.html` |
| 月亮动态头像 | `assets/moon-wolf.webp` |
| 星空背景 | `assets/nightscape.webp` |

## 本地维护

网站是原生 HTML、CSS 和 JavaScript，无外部运行依赖。直接打开 `index.html` 可预览；也可在本目录运行 `python -m http.server 8000` 后访问 http://localhost:8000/。

`build_page.py` 和 `profile_content.py` 是可选的内容维护脚本。需要使用时，修改脚本并运行 `python build_page.py`，然后将脚本及更新后的 `index.html` 一起提交。生成脚本会读取现有 HTML 中的 SVG 图标，因此应保留 `index.html`。直接在 GitHub 编辑 HTML 后，如以后重新运行生成脚本，应先同步对应内容，避免覆盖修改。

## 发布

仓库 Settings → Pages 的发布来源设为 **Deploy from a branch**，分支选择 **main**，目录选择 **/ (root)**。GitHub Pages 在 `main` 每次更新后直接发布根目录中的网页文件。根目录的 `.nojekyll` 保证静态文件原样发布；无需迁移包、服务器、构建依赖或自定义工作流。GitHub 自带的发布进度仍可在仓库 Actions 页面查看。

界面组合支持直接分享：

- [English · Research](https://charlyx-lee.github.io/?view=research&lang=en)
- [中文 · 科研](https://charlyx-lee.github.io/?view=research&lang=zh-CN)
- [English · Campus](https://charlyx-lee.github.io/?view=campus&lang=en)
- [中文 · 校园经历](https://charlyx-lee.github.io/?view=campus&lang=zh-CN)
