"""Build the static bilingual CV from the supplied CV and user-confirmed updates."""
from pathlib import Path
from html import escape as e
import re
from profile_content import (
    graduate_roles, undergraduate_roles,
    graduate_honors, undergraduate_honors,
    graduate_scholarships, undergraduate_scholarships,
)

ROOT = Path(__file__).parent
def b(en, zh):
    return f'<span class="lang-en" lang="en">{e(en)}</span><span class="lang-zh" lang="zh-CN">{e(zh)}</span>'
def icon(name):
    return f'<svg aria-hidden="true"><use href="#i-{name}"/></svg>'
def attrs(en, zh):
    return f'aria-label="{e(en)}" title="{e(en)}" data-label-en="{e(en)}" data-label-zh="{e(zh)}"'
def section_head(symbol, en, zh):
    return f'<div class="section-heading"><h2>{icon(symbol)}{b(en,zh)}</h2></div>'

universities = {
    'Dalian University of Technology': ('https://en.dlut.edu.cn/', 'https://www.dlut.edu.cn/'),
    'Peking University': ('https://english.pku.edu.cn/', 'https://www.pku.edu.cn/'),
    'Nanyang Technological University': ('https://www.ntu.edu.sg/', 'https://www.ntu.edu.sg/'),
    'Nanjing University': ('https://www.nju.edu.cn/en/', 'https://www.nju.edu.cn/'),
    'School of Computer Science and Technology': ('https://cs.dlut.edu.cn/ENGLISH/Home.htm', 'https://cs.dlut.edu.cn/'),
    'School of International Information and Software': ('https://drise.dlut.edu.cn/ywwENGLISH.htm', 'https://drise.dlut.edu.cn/'),
}

def university(en, zh):
    if en not in universities:
        return b(en, zh)
    urls = universities[en]
    return ''.join(f'<a class="university-link lang-{lang}" lang="{code}" href="{url}" target="_blank" rel="noopener noreferrer">{e(label)}</a>'
                   for lang, code, label, url in [('en', 'en', en, urls[0]), ('zh', 'zh-CN', zh, urls[1])])

def email_widget():
    return f'''<div class="email-widget">
      <a class="email-icon" href="mailto:1263763634@qq.com" {attrs('Send email','发送邮件')}>{icon('mail')}</a>
      <div class="email-popover"><button class="copy-email" type="button" data-email="1263763634@qq.com">{b('Copy email address','复制邮箱地址')}</button></div>
      <span class="email-status" role="status" aria-live="polite"></span>
    </div>'''

def view_switch():
    return f'''<div class="profile-view-switch" role="group" {attrs('Choose profile view','选择主页版本')}>
      <button class="view-button" type="button" data-view-select="research" aria-pressed="true">{icon('flask')}{b('Research','科研')}</button>
      <button class="view-button" type="button" data-view-select="campus" aria-pressed="false">{icon('people')}{b('Campus','校园经历')}</button>
    </div>'''

def section_navigation():
    sections = {
        'research': [('research','paper','Publications','论文成果'), ('education','education','Education','教育经历'), ('research-experience','flask','Research Experience','科研经历'), ('experience','briefcase','Industry Experience','实习经历'), ('academic-services','people','Academic Services','学术任职'), ('skills','skills','Skills','专业技能')],
        'campus': [('education','education','Education','教育经历'), ('leadership','people','Student Leadership','学生工作任职'), ('honors','trophy','Honors','荣誉称号'), ('scholarships','education','Scholarships','奖学金'), ('competitions','medal','Competitions','竞赛经历')],
    }
    links = ''.join(f'<a href="#{target}" data-audience="{view}">{icon(symbol)}{b(en,zh)}</a>' for view, entries in sections.items() for target, symbol, en, zh in entries)
    return f'<nav class="section-nav" {attrs("On this page","本页导航")}>{links}</nav>'

old = (ROOT/'dist/index.html').read_text(encoding='utf-8')
symbols = re.search(r'<svg class="icon-library".*?</svg>', old, re.S).group(0)
if 'id="i-mail"' not in symbols:
    symbols=symbols.replace('</svg>', '''
    <symbol id="i-mail" viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 6 9 7 9-7"/></symbol>
    <symbol id="i-download" viewBox="0 0 24 24"><path d="M12 3v12m-4-4 4 4 4-4M4 16v5h16v-5"/></symbol>
    <symbol id="i-bilibili" viewBox="0 0 24 24"><rect x="3" y="7" width="18" height="13" rx="3"/><path d="m7 2 4 5m6-5-4 5M8 11v3m8-3v3m-7 3 3 1 3-1"/></symbol>
    <symbol id="i-orcid" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M7 9v8M11 7h3a5 5 0 0 1 0 10h-3Z"/><circle cx="7" cy="6" r=".7" fill="currentColor" stroke="none"/></symbol>
    <symbol id="i-redbook" viewBox="0 0 24 24"><path d="M4 5h6c2 0 2 1 2 2 0-1 0-2 2-2h6v14h-6c-2 0-2 1-2 1s0-1-2-1H4Z"/><path d="M12 7v13M7 9h2m6 0h2M7 12h2m6 0h2"/></symbol>
  </svg>''')

section_symbols = {
    'paper': '<path d="M5 3h10l4 4v14H5Z M14 3v5h5 M8 12h8 M8 16h6"/>',
    'flask': '<path d="M9 3h6 M10 3v7L4 20h16l-6-10V3 M7 15h10"/>',
    'briefcase': '<rect x="3" y="7" width="18" height="14" rx="2"/><path d="M8 7V3h8v4 M3 12l9 3 9-3 M12 12v5"/>',
    'education': '<path d="m2 9 10-5 10 5-10 5Z M6 11v7c4 3 8 3 12 0v-7 M22 9v8"/>',
    'trophy': '<path d="M8 3h8v7a4 4 0 0 1-8 0Z M8 5H4v3a4 4 0 0 0 4 4 M16 5h4v3a4 4 0 0 1-4 4 M12 14v5 M8 21h8 M10 19h4"/>',
    'skills': '<path d="m8 7-5 5 5 5 M16 7l5 5-5 5 M14 4l-4 16"/>',
    'document': '<path d="M5 3h10l4 4v14H5Z M14 3v5h5 M8 12h8 M8 16h5"/>',
    'people': '<circle cx="9" cy="7" r="3"/><path d="M3 21v-3a6 6 0 0 1 12 0v3 M17 4a3 3 0 0 1 0 6 M19 21v-3a6 6 0 0 0-2-4"/>',
    'medal': '<circle cx="12" cy="8" r="5"/><path d="m8 12-2 9 6-3 6 3-2-9 M12 5v6 M9 8h6"/>',
    'project': '<path d="M3 7h7l2 3h9v11H3Z M3 7V3h7l2 3h9v4 M8 15h8 M12 12v6"/>',
}
for name, paths in section_symbols.items():
    if f'id="i-{name}"' not in symbols:
        symbols = symbols.replace('</svg>', f'<symbol id="i-{name}" viewBox="0 0 24 24">{paths}</symbol></svg>')

socials = [
 ('scholar','scholar','Google Scholar','谷歌学术','https://scholar.google.com/citations?user=BQuYZZwAAAAJ&hl=zh-CN'),
 ('github','github','GitHub','GitHub','https://github.com/CharlyX-Lee'),
 ('csdn','code','CSDN Blog','CSDN 博客','https://blog.csdn.net/m0_62970200?spm=1000.2115.3001.5343'),
 ('bilibili','bilibili','Bilibili','哔哩哔哩','https://space.bilibili.com/388319692?spm_id_from=333.33.0.0'),
 ('orcid','orcid','ORCID','ORCID 学者档案','https://orcid.org/0009-0007-4327-5468'),
 ('redbook','redbook','Xiaohongshu','小红书','https://www.xiaohongshu.com/user/profile/669b9d4b000000002402377f'),
 ('wechat','wechat','WeChat article','微信公众号文章','https://mp.weixin.qq.com/s/ijjlf18BKiNBhJyPUNr1tQ?poc_token=HP-v7WqjwsVAKKce3HrXdx1YI7uChwb2BokbRP0f')
]
social_html='\n'.join(f'<a class="social-link {cl}" href="{e(url)}" target="_blank" rel="noopener noreferrer" {attrs(en+" (opens in a new tab)",zh+"（新标签页打开）")}>{icon(ic)}</a>' for cl,ic,en,zh,url in socials)

research = [
 dict(id='goalfly', venue='ICRA 2027', status=('Under review','审稿中'),
      title='GoalFly: Adaptive Reasoning and View-Aware Goal Planning for Zero-shot Aerial Vision-Language Navigation',
      authors='<strong>Xiang Li</strong>, Zhang Zhiwei, Xin Gao, Yisha Liu, Yan Zhuang', links=[]),
 dict(id='stereo', venue='IJRR', status=('Under review','审稿中'),
      title='StereoAdapter-2: Globally Structure-Consistent Underwater Stereo Depth Estimation',
      authors='Zeyu Ren, <strong>Xiang Li</strong>, Yiran Wang, Zeyu Zhang, Hao Tang',
      links=[('Paper','论文','https://arxiv.org/abs/2602.16915')]),
 dict(id='vio', venue='ICARCV 2026', status=('Accepted','已接收'),
      title='Benchmarking Visual-Inertial Odometry in Subterranean Environments Under Sensor Degradation, Miscalibration, and Dynamic Occlusion',
      authors='Yueying Zhu, <strong>Xiang Li</strong>, Thien-Minh Nguyen, Xuehe Wang, Shenghai Yuan',
      links=[('Paper','论文','https://arxiv.org/abs/2609.18628')]),
 dict(id='gsuvce', venue='ICRA 2026', status=('Accepted','已接收'),
      title='GS-UVCE: Gaussian Splatting-Driven Unsupervised Visual Consistency Enhancement for Underwater 3D Scene Reconstruction',
      authors='<strong>Xiang Li</strong>, Chi Li, Yiming Xu, Yan Zhuang',
      links=[('Paper','论文','https://ieeexplore.ieee.org/document/11696993')]),
 dict(id='smiles', venue='SSPP 2026', status=('Project paper','项目论文'),
      title='Bayesian Latent Safety-Trait Inference for LLMs and Agentic Systems',
      authors='Anastasiia Lapshina, Danil Karpov, <strong>Xiang Li</strong>, Fuyao Qiu, Fang Liu',
      links=[('OpenReview','OpenReview','https://openreview.net/forum?id=K4FGdQSzDP')]),
 dict(id='oracle', venue='ICSECE 2024', status=('Published','已发表'),
      title='Text Detection and Character Recognition of Oracle Original Topographies Based on PP-YOLOE+',
      authors='<strong>Xiang Li</strong>, Mingqi Zhang, Xiaoman Du',
      links=[('Paper','论文','https://ieeexplore.ieee.org/abstract/document/10729332/')]),
]
def research_item(r):
    status={'Under review':'under-review','Accepted':'accepted','Published':'published','Project paper':'project-paper'}[r['status'][0]]
    author=f'<p class="research-authors">{r["authors"]}</p>' if r['authors'] else ''
    links=''.join(f'<a href="{e(url)}" target="_blank" rel="noopener noreferrer">{b(en,zh)} {icon("arrow")}</a>' for en,zh,url in r['links'])
    return f'''<article class="research-item">
      <div class="research-visual"><img src="assets/research-{r['id']}.svg" alt="" width="320" height="200" loading="lazy"></div>
      <div class="research-body"><div class="research-title-row"><h3 lang="en">{e(r['title'])}</h3><span class="venue {status}">{r['venue']} · {b(*r['status'])}</span></div>
      {author}{f'<div class="research-links">{links}</div>' if links else ''}</div>
    </article>'''

def timeline_item(date, role, org):
    zh_dates = {'Jul 2026':'2026.07','Jan – Mar 2026':'2026.01 – 2026.03','Oct 2025 – May 2026':'2025.10 – 2026.05','Jun – Sep 2026':'2026.06 – 2026.09','Apr – Jun 2026':'2026.04 – 2026.06','Mar 2025 – Apr 2026':'2025.03 – 2026.04'}
    return f'''<article class="timeline-item"><div class="timeline-date">{b(date,zh_dates[date])}</div><div class="timeline-content"><h3 class="role-title">{b(*role)}</h3><p class="organization">{university(*org)}</p></div></article>'''

research_experience = [
 ('Jul 2026', ('SMILES-2026 Summer School · Participant','SMILES-2026 暑期学校 · 学员'), ('Nanjing University','南京大学')),
 ('Jan – Mar 2026', ('Research Assistant · Robot Perception','科研助理 · 机器人感知'), ('Nanyang Technological University','南洋理工大学')),
 ('Oct 2025 – May 2026', ('Research Assistant · Underwater 3D Vision','科研助理 · 水下三维视觉'), ('Peking University','北京大学')),
]
industry_experience = [
 ('Jun – Sep 2026', ('Embodied Agent Algorithms Intern','人形机器人具身 Agent 算法实习'), ('Midea Central Research Institute','美的中央研究院')),
 ('Apr – Jun 2026', ('Underwater Robotics Simulation Intern','水下机器人具身智能仿真算法实习'), ('Bianji Lingyu','边际领域')),
 ('Mar 2025 – Apr 2026', ('Multi-Robot Navigation Algorithms Intern','空地协同机器人导航算法实习'), ('Dalian Hangjia Robotics','大连航佳机器人')),
]

competition_groups = [
 (('National Awards','国家级奖项'), [
  ('14th APMCM Asia-Pacific Mathematical Contest in Modeling — National Second Prize','第十四届APMCM亚太地区大学生数学建模竞赛国家二等奖'),
  ('14th National College Mathematics Competition — National Third Prize','第十四届全国大学生数学竞赛国家三等奖'),
  ('2024 China Collegiate Computing Contest, AIGC Innovation Competition — National Third Prize','2024年中国高校计算机大赛-AIGC创新赛国家三等奖'),
  ('13th National College Student Digital Media Technology Competition (2026) — National Third Prize','2026年第十三届全国大学生数字媒体科技大赛国家三等奖'),
  ('21st May Day Mathematical Modeling Competition — National Third Prize','第二十一届五一数学建模竞赛国家三等奖'),
 ]),
 (('Provincial & Regional Awards','省级与区域级奖项'), [
  ('2026 Mathematical Modeling League of the Three Northeastern Provinces — Provincial First Prize','2026年东北三省数学建模联赛省一等奖'),
  ('2024 Mathematical Modeling League of the Three Northeastern Provinces — Provincial First Prize','2024年东北三省数学建模联赛省一等奖'),
  ('14th MathorCup Mathematical Application Challenge — Northeast Region Third Prize','第十四届MathorCup数学应用挑战赛东北赛区三等奖'),
 ]),
 (('University-Level Awards','校级奖项'), [
  ('Dalian University of Technology Mathematical Modeling Competition — University-Level First Prize','大连理工大学数学建模竞赛校一等奖'),
  ('4th Dalian University of Technology Artificial Intelligence Challenge — University-Level First Prize','大连理工大学第四届人工智能挑战赛校一等奖'),
  ('17th National Computer Design Competition, Big Data Track — University-Level First Prize','第十七届全国计算机设计大赛大数据赛道校一等奖'),
  ('17th National Computer Design Competition, Software Applications and Development Track — University-Level Second Prize','第十七届全国计算机设计大赛软件应用与开发赛道校二等奖'),
  ('12th National College Student Digital Media Technology Competition (2024) — University-Level Third Prize','2024年第十二届全国大学生数字媒体科技大赛校三等奖'),
  ('1st Dalian University of Technology “AI+” Interdisciplinary Innovation and Application Competition, Intelligent Vehicles Track — University-Level Third Prize','大连理工大学首届“人工智能+”交叉学科创新应用大赛智能车辆赛道校三等奖'),
 ]),
]

def competition_group(title, items):
    rows = ''.join(f'<li>{b(*item)}</li>' for item in items)
    return f'<div class="competition-group"><h3 class="award-group-title">{b(*title)}</h3><ul class="honors-list">{rows}</ul></div>'

def dated_award_group(title, items):
    rows = []
    for item in items:
        rows.append(f'<li><span class="award-date">{e(item["date"])}</span><span class="award-name">{b(item["en"],item["zh"])}</span></li>')
    return f'<div class="award-group"><h3 class="award-group-title">{b(*title)}</h3><ul class="dated-awards">' + ''.join(rows) + '</ul></div>'

def tenure_group(title, items):
    rows = ''.join(f'<li><span class="tenure-role">{b(item["en"],item["title"])}</span><span class="tenure-date">{b(item["date"].replace("至今","Present"),item["date"])}</span></li>' for item in items)
    return f'<div class="tenure-group"><h3 class="award-group-title">{b(*title)}</h3><ul class="tenure-list">{rows}</ul></div>'

memberships = [
    ('IEEE Graduate Student Member', 'IEEE 学生会员'),
    ('IEEE RAS Student Member', 'IEEE RAS 学生会员'),
    ('CAAI Student Member', 'CAAI 学生会员'),
    ('CCF Student Member', 'CCF 学生会员'),
    ('CSIG Student Member', 'CSIG 学生会员'),
    ('CAA Provisional Member', 'CAA 预备会员'),
]
reviewing = ['ICRA 2026, 2027', 'IROS 2026', 'ICARCV 2026', 'RA-L', 'TMM', 'T-FR']

page=f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="theme-color" content="#070b16">
  <meta name="description" content="Xiang Li (CharlyX), master's student in Artificial Intelligence at Dalian University of Technology. Robotics, 3D vision, and embodied AI.">
  <title>Xiang Li | CharlyX · Robotics &amp; 3D Vision</title>
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="style.css">
  <script src="script.js" defer></script>
</head>
<body data-motion="on" data-view="research" id="top">
  <a class="skip-link" href="#about">{b('Skip to CV','跳转到简历')}</a>
    <div class="nightscape" aria-hidden="true">
      <img class="nightscape-art" src="assets/nightscape.webp" alt="" width="2172" height="724" loading="eager">
      <div class="nightscape-aurora"></div><div class="nightscape-grid"></div>
      <div class="nightscape-stars">{'<i></i>' * 12}</div><div class="nightscape-meteor">{'<i></i>' * 3}</div>
    </div>
  <canvas id="starfield" aria-hidden="true"></canvas><div class="nebula" aria-hidden="true"></div><div class="scanlines" aria-hidden="true"></div><div class="scan-beam" aria-hidden="true"></div>
  {symbols}
  <header class="site-header shell">
    <a class="brand" href="#top" {attrs('CharlyX — back to top','CharlyX——返回顶部')}><span class="brand-mark"><svg viewBox="0 0 36 36" aria-hidden="true"><path d="m18 2 15 8v16l-15 8-15-8V10Z"/><path d="M24 11h-8l-5 7 5 7h8M22 15l5 6m0-6-5 6"/></svg></span><span>CHARLYX<span class="brand-dot">.</span></span></a>
    {view_switch()}
    <div class="header-tools"><button id="language-toggle" class="control-button language-button" type="button" aria-label="Switch to Chinese">中文</button><button id="motion-toggle" class="control-button" type="button" aria-pressed="true" {attrs('Toggle motion effects','切换动态效果')}><span class="motion-icon" aria-hidden="true"><i></i><i></i><i></i><i></i></span><span class="motion-label" data-motion-label>Motion on</span></button></div>
  </header>
  <div class="layout shell">
    <aside class="profile" {attrs('Profile and contact','个人信息与联系方式')}>
      <div class="profile-art"><div class="orbit" aria-hidden="true"></div><div class="moon-portrait"><img src="assets/moon-wolf.webp" alt="Animated wolf and moon" data-label-en="Animated wolf and moon" data-label-zh="月亮与狼的动态头像" width="320" height="320" fetchpriority="high"></div></div>
      <h1 class="profile-name">Xiang Li <span class="chinese-name">李响</span></h1>
      <p class="nickname">@CharlyX</p>
      <p class="profile-role">{b("Artificial Intelligence · Master's Student",'人工智能 · 硕士研究生')}</p>
      <p class="profile-affiliation">{university('Dalian University of Technology','大连理工大学')}</p>
      <p class="profile-location">{b('Dalian, China','中国 · 大连')}</p>
      <p class="profile-mbti">MBTI · ENFJ-T</p>
      <nav class="social-links" {attrs('Social and academic profiles','社交与学术主页')}>{social_html}</nav>
      <div class="profile-actions">{email_widget()}<a id="cv-preview" class="cv-button" href="cv.html?lang=en" target="_blank" rel="noopener" {attrs('View Chinese CV in a new tab','在新标签页查看中文简历')}>{icon('document')}{b('View CV · Chinese PDF','查看简历 · 中文 PDF')}</a></div>
      <div class="profile-motto"><p>{b('Steadfast effort. A life lived without complacency.','一以贯之的努力，不得懈怠的人生。')}</p></div>
    </aside>
    <main class="content">
      <span id="view-status" class="visually-hidden" role="status" aria-live="polite"></span>
      <section class="section" id="about" aria-labelledby="about-title">
        <div class="section-heading"><h2 id="about-title">{b('Hi, I’m Xiang.','你好，我是李响。')}</h2></div>
        <div data-audience="research">
        <p class="intro-lead">{b('Building perception that brings robots closer to the real world.','让机器人更好地感知、理解与探索真实世界。')}</p>
        <div class="about-copy"><p>{b('I am a master’s student in Artificial Intelligence at Dalian University of Technology. My research sits at the intersection of robotics, 3D vision, and embodied AI, with a focus on vision-language navigation, underwater reconstruction and depth estimation, and robust robot perception.','我目前是大连理工大学人工智能专业硕士研究生，研究方向聚焦机器人、三维视觉与具身智能，主要关注视觉语言导航、水下三维重建与深度估计，以及机器人感知的鲁棒性。')}</p>
        <p>{b('I enjoy connecting algorithms with real robots—from UAV goal planning and humanoid agents to underwater simulation and multi-robot navigation. I have also worked as a research assistant at Peking University and Nanyang Technological University.','我关注从算法到真实机器人的落地，研究与实践涵盖无人机目标规划、人形机器人智能体、水下仿真与多机器人协同导航，也曾在北京大学和南洋理工大学担任科研助理。')}</p></div>
        </div>
        <div data-audience="campus">
          <p class="intro-lead">{b('Learning and growing through university life.','在科研之外，参与学生工作与校园生活。')}</p>
          <div class="about-copy"><p>{b('My time at Dalian University of Technology spans undergraduate studies in Digital Media Technology and graduate studies in Artificial Intelligence.','我目前是大连理工大学人工智能专业硕士研究生，本科就读于数字媒体技术专业。本页按研究生与本科阶段列出任职职务、荣誉称号和奖学金。')}</p><p>{b('My university honors include the DUT Outstanding Student Model distinction and the Qu Bochuan Scholarship, alongside recognition for innovation, social practice, organizational service, sports, and the arts.','曾获大连理工大学优秀学生标兵、屈伯川奖学金，并在创新创业、社会实践、组织服务、体育竞技与文化艺术等方面获得奖励。')}</p></div>
        </div>
        {section_navigation()}
      </section>
      <section class="section" id="research" data-audience="research">{section_head('paper','Publications','论文成果')}
        <div class="research-list">{''.join(research_item(r) for r in research)}</div>
      </section>
      <section class="section" id="education">{section_head('education','Education','教育经历')}
        <article class="education-item"><div class="education-meta"><h3>{university('Dalian University of Technology','大连理工大学')}</h3><span class="timeline-date">{b('2025.09 – Present','2025.09 – 至今')}</span></div><p class="education-school">{university('School of Computer Science and Technology','计算机科学与技术学院')}</p><p class="education-degree">{b('Master’s in Artificial Intelligence (Rank: 1 / 197)','硕士 · 人工智能（排名：1 / 197）')}</p></article>
        <article class="education-item"><div class="education-meta"><h3>{university('Dalian University of Technology','大连理工大学')}</h3><span class="timeline-date">{b('Sep 2021 – Jun 2025','2021.09 – 2025.06')}</span></div><p class="education-school">{university('School of International Information and Software','国际信息与软件学院')}</p><p class="education-degree">{b('Bachelor’s in Digital Media Technology (Rank: 11 / 120)','学士 · 数字媒体技术（排名：11 / 120）')}</p></article>
      </section>
      <section class="section" id="research-experience" data-audience="research">{section_head('flask','Research Experience','科研经历')}<div class="timeline">{''.join(timeline_item(*x) for x in research_experience)}</div></section>
      <section class="section" id="experience" data-audience="research">{section_head('briefcase','Industry Experience','实习经历')}<div class="timeline">{''.join(timeline_item(*x) for x in industry_experience)}</div></section>
      <section class="section" id="academic-services" data-audience="research">{section_head('people','Academic Services','学术任职')}
        <div class="services-grid">
          <article class="service-group"><h3>{icon('people')}{b('Professional Memberships','学会会员')}</h3><ul class="service-list">{''.join(f'<li>{b(*item)}</li>' for item in memberships)}</ul></article>
          <article class="service-group"><h3>{icon('paper')}{b('Reviewer','审稿人')}</h3><ul class="service-list">{''.join(f'<li>{e(item)}</li>' for item in reviewing)}</ul></article>
        </div>
      </section>
      <section class="section" id="skills" data-audience="research">{section_head('skills','Skills','专业技能')}
        <div class="skills-grid"><div class="skill-group"><h3>{b('Programming','编程')}</h3><p>Python · C++ · PyTorch</p></div><div class="skill-group"><h3>{b('Robotics & Tools','机器人与工具')}</h3><p>Isaac Sim · MuJoCo · ROS · Qt · Git · Docker</p></div><div class="skill-group"><h3>{b('Languages','语言')}</h3><p>{b('English: CET-4 & CET-6','英语：CET-4、CET-6')}</p></div></div>
      </section>
      <section class="section" id="leadership" data-audience="campus">{section_head('people','Student Leadership','学生工作任职')}
        {tenure_group(('Graduate Studies','研究生阶段'),graduate_roles)}{tenure_group(('Undergraduate Studies','本科阶段'),undergraduate_roles)}
      </section>
        <section class="section" id="honors" data-audience="campus">{section_head('trophy','Honors & Distinctions','荣誉称号')}
          <div class="honors-groups">{dated_award_group(('Graduate Studies','研究生阶段'),graduate_honors)}{dated_award_group(('Undergraduate Studies','本科阶段'),undergraduate_honors)}</div>
        </section>
        <section class="section" id="scholarships" data-audience="campus">{section_head('education','Scholarships','奖学金')}
          <div class="honors-groups">{dated_award_group(('Graduate Studies','研究生阶段'),graduate_scholarships)}{dated_award_group(('Undergraduate Studies','本科阶段'),undergraduate_scholarships)}</div>
        </section>
      <section class="section" id="competitions" data-audience="campus">{section_head('medal','Competitions','竞赛经历')}
        <div class="honors-groups">{''.join(competition_group(title,items) for title,items in competition_groups)}</div>
      </section>
      <section class="section contact-section" id="contact"><p class="section-kicker">LET’S CONNECT</p><div class="contact-heading"><h2>{b('Ideas are better shared.','让想法相遇。')}</h2>{email_widget()}</div><p data-audience="research">{b('Let’s connect on embodied intelligence, robot perception, and 3D vision.','欢迎交流具身智能、机器人感知与三维视觉相关研究。')}</p><p data-audience="campus">{b('Let’s connect on university life and shared interests.','欢迎交流学生工作、校园生活与共同关注的话题。')}</p></section>
    </main>
  </div>
  <div class="page-ending">
  <footer class="site-footer shell"><span>© 2026 Xiang Li <span class="brand-dot">/</span> CharlyX</span><p class="footer-note">{b('Look to the stars and dream. Face setbacks undaunted.','仰望星空树理想，直面挫折不彷徨。')}</p><a class="back-top" href="#top">{b('Back to top','返回顶部')} ↑</a></footer>
  </div>
</body>
</html>
'''
(ROOT/'dist/index.html').write_text(page,encoding='utf-8')
print('Bilingual CV page built.')
