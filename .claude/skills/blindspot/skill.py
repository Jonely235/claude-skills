#!/usr/bin/env python3
"""
Blind Spot Offense Generator
Generates short, punchy corrections to cognitive blind spots.
"""

import sys

def main():
    # Get input from command line args or stdin
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        user_input = sys.stdin.read().strip() if not sys.stdin.isatty() else ""

    # Detect language
    has_chinese = any('\u4e00' <= c <= '\u9fff' for c in user_input)
    lang = "zh" if has_chinese else "en"

    # Build prompt based on language
    if lang == "zh":
        if user_input:
            prompt = f"""你是认知偏差纠错专家。用户输入："{user_input}"

任务：生成 1 条反直觉的认知纠偏，直接攻击用户陈述背后的假设。

严格规则：
1. 字数 ≤ 25 字
2. 禁止解释，禁止说教，禁止"你应该"
3. 不是提醒，而是纠偏
4. 方向必须反过来（反向思考）
5. 具体行为切入，不要抽象哲学
6. 只输出 1 条，不要多条
7. 不要任何前缀（如"建议："、"思考："）

反例（不要这样）：
- "你应该关注完成而非完美"
- "完美主义是个陷阱"
- "记住完成大于完美"

正例（要这样）：
- "完成大于完美"
- "你不是主角"
- "先做起来，再修"

直接输出结果，不要其他文字。"""
        else:
            prompt = f"""你是认知偏差纠错专家。

任务：从日常行为模式中，生成 1 条反直觉的认知纠偏。

常见盲区：完美主义、主角综合症、计划谬误、分析瘫痪、确认偏误、沉没成本

严格规则：
1. 字数 ≤ 25 字
2. 禁止解释，禁止说教
3. 不是提醒，而是纠偏
4. 方向必须反过来
5. 具体行为切入
6. 只输出 1 条

直接输出结果，不要前缀。"""
    else:
        if user_input:
            prompt = f"""You are a cognitive bias correction expert. User input: "{user_input}"

Task: Generate 1 counter-intuitive blind-spot correction that attacks the assumption behind their statement.

STRICT RULES:
1. Max 25 characters
2. No explanations, no preaching, no "you should"
3. Not reminders, but CORRECTIONS
4. Reverse the direction - think opposite
5. Specific behaviors, not abstract philosophy
6. Output only ONE insight, never multiple
7. No prefixes like "Insight:", "Think:", "Tip:"

BAD examples (don't do this):
- "You should focus on completion over perfection"
- "Perfectionism is a trap"
- "Remember that done is better than perfect"

GOOD examples (do this):
- "Done > Perfect"
- "You're not the protagonist"
- "Ship broken, fix later"

Output the result directly, nothing else."""
        else:
            prompt = f"""You are a cognitive bias correction expert.

Task: Generate 1 counter-intuitive blind-spot correction from common daily behavior patterns.

Common blind spots: perfectionism, protagonist syndrome, planning fallacy, analysis paralysis, confirmation bias, sunk cost

STRICT RULES:
1. Max 25 characters
2. No explanations, no preaching
3. Not reminders, but CORRECTIONS
4. Reverse the direction
5. Specific behaviors only
6. Output only ONE insight

Output the result directly, no prefix."""

    # Output the prompt for Claude to process
    print(prompt)

if __name__ == "__main__":
    main()
