# 安装指南

## 先确定当前 profile

Hermes 的 skills 属于当前 profile。默认 profile 使用主目录下的 `.hermes/skills`；设置了 `HERMES_HOME` 时使用该位置；其他 profile 必须选择其实际 `skills` 路径。不要为了安装本技能改动其他 profile。

## 没有 Git / Python 时

1. GitHub 页面 Code → Download ZIP。
2. 解压后找到 `qzone-archive/SKILL.md`。
3. 把包含此文件的 `qzone-archive` 文件夹复制到当前 profile 的 `skills` 文件夹。
4. 最终路径必须是 `skills/qzone-archive/SKILL.md`，不是 `skills/qzone-archive-skill-main/qzone-archive/SKILL.md`。
5. 已存在同名技能时先备份和比较；不要覆盖个人改进。
6. 开启新会话并要求 Hermes 加载 `qzone-archive`。

## 有 Python 时

仓库解压根目录执行：

```bash
python3 scripts/install.py --dry-run
python3 scripts/install.py
```

Windows 可将 `python3` 换成 `py -3`。脚本仅用 Python 标准库，不需要 pip 安装。

指定技能目录：

```bash
python3 scripts/install.py --skills-dir "/path/to/profile/skills" --dry-run
python3 scripts/install.py --skills-dir "/path/to/profile/skills"
```

`--skills-dir` 接收 **skills 父目录**，不要传入最终的 `qzone-archive` 目录。路径含空格时必须加引号。

## 安装成功的标准

- 目标 `qzone-archive/SKILL.md` 存在且包含 frontmatter。
- 新会话中的 Hermes 可加载该技能。
- 没有更改 `.env`、`config.yaml`、认证信息或已有归档。

脚本成功只证明文件安装完成，不证明 QQ 登录或归档已经成功。真正归档还需浏览器工具、可用模型、授权和可写 Vault。

## 更新 / 卸载

更新时先备份已有技能，人工比较新旧版本。安装脚本故意不提供覆盖参数。卸载只移除当前 profile 下的 `skills/qzone-archive`；不要删除 Obsidian 归档。技能卸载不会自动删除私人原始数据。

## 当前测试范围

安装脚本在 macOS 实际运行并通过标准库单元测试。代码采用跨平台 pathlib，未声称在 Windows/Linux 机器上实测；手动复制方式不依赖 shell 专用命令。
