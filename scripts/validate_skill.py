#!/usr/bin/env python3
"""Validate the portable structure of field-watch-skill-builder.

This intentionally uses only the Python standard library so GitHub Actions and
minimal local environments can run it without installing PyYAML.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "field-watch-skill-builder"
SKILL_MD = SKILL_DIR / "SKILL.md"
OPENAI_YAML = SKILL_DIR / "agents" / "openai.yaml"
OPENCLAW_ADAPTER = ROOT / "adapters" / "openclaw-frontmatter.yaml"

ALLOWED_TOP_LEVEL_KEYS = {"name", "description", "metadata", "license", "allowed-tools"}


def fail(message: str) -> int:
    print(f"[FAIL] {message}")
    return 1


def read(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(path)
    return path.read_text(encoding="utf-8")


def frontmatter(text: str) -> str:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise ValueError("SKILL.md must start with YAML frontmatter delimited by ---")
    return match.group(1)


def top_level_keys(fm: str) -> list[str]:
    keys: list[str] = []
    for line in fm.splitlines():
        if not line.strip() or line.startswith(" "):
            continue
        if ":" not in line:
            raise ValueError(f"invalid top-level frontmatter line: {line}")
        keys.append(line.split(":", 1)[0].strip())
    return keys


def main() -> int:
    try:
        skill_text = read(SKILL_MD)
        fm = frontmatter(skill_text)
        keys = top_level_keys(fm)

        unexpected = sorted(set(keys) - ALLOWED_TOP_LEVEL_KEYS)
        if unexpected:
            return fail(f"unexpected SKILL.md frontmatter keys: {', '.join(unexpected)}")

        if "name" not in keys:
            return fail("missing name in SKILL.md frontmatter")
        if "description" not in keys:
            return fail("missing description in SKILL.md frontmatter")
        if not re.search(r"^name:\s*field-watch-skill-builder\s*$", fm, re.MULTILINE):
            return fail("skill name must be field-watch-skill-builder")

        description_match = re.search(r"^description:\s*(.+)$", fm, re.MULTILINE)
        if not description_match:
            return fail("description must be a single-line frontmatter field")
        if len(description_match.group(1)) > 1024:
            return fail("description exceeds 1024 characters")

        required_sections = [
            "## 角色定位",
            "## 兼容性原则",
            "## 输入理解",
            "## 领域分析流程",
            "## 输出结构",
            "## 生成后的技能固定逻辑",
            "## 批判性阅读底线",
            "## 卡片模板",
            "## 禁止事项",
            "## 成功标准",
        ]
        missing_sections = [section for section in required_sections if section not in skill_text]
        if missing_sections:
            return fail(f"missing required sections: {', '.join(missing_sections)}")

        openai_text = read(OPENAI_YAML)
        if "default_prompt:" not in openai_text or "$field-watch-skill-builder" not in openai_text:
            return fail("agents/openai.yaml default_prompt must mention $field-watch-skill-builder")

        openclaw_text = read(OPENCLAW_ADAPTER)
        for needle in ("version: 1.0.0", "user-invocable: true", "openclaw:"):
            if needle not in openclaw_text:
                return fail(f"OpenClaw adapter missing {needle}")

    except Exception as exc:  # noqa: BLE001 - validation CLI should report any issue plainly.
        return fail(str(exc))

    print("[OK] field-watch-skill-builder structure is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
