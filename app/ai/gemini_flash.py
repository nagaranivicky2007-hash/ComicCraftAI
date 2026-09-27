import json
from typing import Any

from app.config import get_settings
from app.schemas import PanelOutline, PromptRequest


def _demo_outline(
    request: PromptRequest
) -> list[PanelOutline]:

    return [
        PanelOutline(
            panel_number=1,
            title="The Beginning",
            scene_description=(
                f"{request.character_name} arrives at "
                f"{request.setting} and discovers that "
                f"something unusual is happening."
            ),
            image_prompt=(
                f"{request.art_style} comic panel, "
                f"{request.character_name} entering "
                f"{request.setting}, mysterious atmosphere, "
                "expressive character, cinematic composition"
            )
        ),

        PanelOutline(
            panel_number=2,
            title="A Strange Discovery",
            scene_description=(
                f"{request.character_name} follows a clue "
                "and discovers an unexpected secret."
            ),
            image_prompt=(
                f"{request.art_style} comic panel, "
                f"{request.character_name} discovering a "
                f"mysterious clue in {request.setting}, "
                "dynamic perspective, vivid storytelling"
            )
        ),

        PanelOutline(
            panel_number=3,
            title="The Challenge",
            scene_description=(
                "A difficult obstacle appears, forcing "
                f"{request.character_name} to make a brave choice."
            ),
            image_prompt=(
                f"{request.art_style} comic panel, heroic "
                f"challenge for {request.character_name}, "
                f"dramatic action in {request.setting}, "
                "strong expressions"
            )
        ),

        PanelOutline(
            panel_number=4,
            title="The Turning Point",
            scene_description=(
                f"{request.character_name} uses courage "
                "and creativity to change the situation."
            ),
            image_prompt=(
                f"{request.art_style} comic panel, "
                f"{request.character_name} overcoming a "
                "challenge, triumphant movement, dramatic lighting"
            )
        ),

        PanelOutline(
            panel_number=5,
            title="A New Chapter",
            scene_description=(
                f"The adventure ends with a hopeful discovery "
                f"and a promise of another journey for "
                f"{request.character_name}."
            ),
            image_prompt=(
                f"{request.art_style} comic panel, "
                f"{request.character_name} looking toward "
                f"a hopeful horizon at {request.setting}, "
                "warm cinematic ending"
            )
        )
    ]


def generate_outline(
    request: PromptRequest
) -> tuple[list[PanelOutline], bool]:

    settings = get_settings()

    # Demo mode
    if not settings.gemini_api_key:

        if settings.ai_strict:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured."
            )

        return _demo_outline(request), True

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(
            api_key=settings.gemini_api_key
        )

        prompt = f"""
Create a cohesive 5-panel comic outline.

Story idea:
{request.story_prompt}

Main character:
{request.character_name}

Setting:
{request.setting}

Tone:
{request.tone}

Art style:
{request.art_style}

Return ONLY valid JSON.

Return exactly 5 objects.

Each object must contain:

panel_number
title
scene_description
image_prompt

Rules:

1. panel_number must be 1 through 5.
2. Keep the story continuous.
3. Keep the main character consistent.
4. scene_description should contain 1-2 sentences.
5. image_prompt should describe the visual scene.
6. Do not include Markdown.
"""

        response = client.models.generate_content(
            model=settings.outline_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.8,
                max_output_tokens=2500,
                response_mime_type="application/json"
            )
        )

        raw = response.text or "[]"

        data: Any = json.loads(raw)

        panels = [
            PanelOutline.model_validate(item)
            for item in data
        ]

        if len(panels) != 5:
            raise RuntimeError(
                "Gemini did not return exactly 5 panels."
            )

        return panels, False

    except Exception as exc:

        if settings.ai_strict:
            raise RuntimeError(
                f"Gemini outline generation failed: {exc}"
            ) from exc

        return _demo_outline(request), True