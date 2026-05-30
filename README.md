# Field Watch Skill Builder

`field-watch-skill-builder` 是一个“技能生成器”技能：给它一个研究领域、子方向或交叉学科主题，它会生成一个可安装的专属文献推送 `SKILL.md`。

它不是直接做每日文献推送，而是帮助你批量生产高信噪比的领域文献监控技能。生成出的技能会内置核心团队、核心期刊、核心关键词、纳入/排除标准、默认时间逻辑和“慢老师文献推送卡片”格式。

## Repository Layout

```text
.
├── field-watch-skill-builder/
│   ├── SKILL.md
│   └── agents/
│       └── openai.yaml
├── adapters/
│   └── openclaw-frontmatter.yaml
├── examples/
│   └── prompts.md
├── LICENSE
└── README.md
```

## Install

### Codex

Copy the `field-watch-skill-builder` folder into your Codex skills directory:

```bash
~/.codex/skills/field-watch-skill-builder/
```

Then invoke it with:

```text
Use $field-watch-skill-builder to generate a literature-watch skill for AI agent evaluation.
```

### Claude-style SKILL.md agents

Use the same `field-watch-skill-builder/SKILL.md` file in any agent environment that supports folder-based `SKILL.md` skills with YAML frontmatter.

### OpenClaw

The main `SKILL.md` keeps OpenClaw metadata under `metadata.openclaw` for broad compatibility. If your OpenClaw runtime expects top-level `version` and `user-invocable` fields, use `adapters/openclaw-frontmatter.yaml` as the publishing frontmatter reference.

## Example Prompts

See [examples/prompts.md](examples/prompts.md).

## Validation

Run the repository validator:

```bash
python scripts/validate_skill.py
```

For Codex-compatible validation when PyYAML is available:

```bash
python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ./field-watch-skill-builder
```

## Publishing Checklist

- Confirm `field-watch-skill-builder/SKILL.md` validates.
- Confirm GitHub Actions passes after the first push.
- Add a GitHub repository description such as: `Generate field-specific literature-watch skills for Codex, Claude, OpenClaw, and similar agents.`
- Tag the first release as `v1.0.0`.
- Keep platform-specific manifest variants in `adapters/`, not inside the skill folder unless the target platform requires them.

## License

MIT License. See [LICENSE](LICENSE).
