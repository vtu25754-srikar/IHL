import os
from fastmcp import FastMCP
from openai import OpenAI

# ==============================================================
# CONFIGURATION
# ==============================================================
# All generated stories are saved inside this subfolder
STORIES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stories")

# Ensure the stories folder exists on startup
os.makedirs(STORIES_DIR, exist_ok=True)

# LM Studio local API URL (must be running)
LM_STUDIO_URL = "http://localhost:1234/v1"

# Initialize FastMCP server
mcp = FastMCP("Story Generator")

# Initialize LM Studio client
client = OpenAI(
    base_url=LM_STUDIO_URL,
    api_key="lm-studio"  # LM Studio does not need a real API key
)


def get_model() -> str:
    """Auto-detect the loaded model from LM Studio."""
    try:
        models = client.models.list()
        for m in models.data:
            if "embed" not in m.id.lower():
                return m.id
        if models.data:
            return models.data[0].id
    except Exception:
        pass
    return "local-model"


# ==============================================================
# MCP TOOL: generate_story
# This is what shows up in MCP Inspector
# ==============================================================
@mcp.tool()
def generate_story(story_idea: str, filename: str) -> str:
    """
    Generate a creative story using LM Studio and save it to the stories folder.

    Args:
        story_idea: Your story idea or topic (e.g. 'A dragon who loves books').
        filename: Name of the output text file (e.g. 'dragon.txt').
    """

    # Always save inside the 'stories' folder
    if not filename.endswith(".txt"):
        filename = filename + ".txt"

    save_path = os.path.join(STORIES_DIR, filename)

    # Detect available model
    model_id = get_model()

    # Prompt engineering for creative output
    system_prompt = (
        "You are an award-winning creative author. "
        "Write rich, vivid, imaginative stories with strong characters, "
        "sensory details, emotional depth, and an unexpected twist. "
        "Avoid clichés. Make every sentence count."
    )

    user_prompt = (
        f"Write a highly creative and engaging story based on this idea:\n\n"
        f"{story_idea}\n\n"
        f"The story should be at least 5 paragraphs long."
    )

    try:
        # Call LM Studio model
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt}
            ],
            temperature=0.9,
            max_tokens=1500,
        )

        story_text = response.choices[0].message.content

        # Write the story file inside stories/
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(f"STORY IDEA : {story_idea}\n")
            f.write(f"MODEL USED : {model_id}\n")
            f.write("=" * 50 + "\n\n")
            f.write(story_text)

        return (
            f"Story saved successfully!\n"
            f"File    : {save_path}\n"
            f"Model   : {model_id}\n\n"
            f"Preview :\n{story_text[:400]}..."
        )

    except Exception as e:
        return (
            f"ERROR: Could not connect to LM Studio.\n"
            f"Details: {str(e)}\n\n"
            f"Please:\n"
            f"  1. Open LM Studio\n"
            f"  2. Load a model\n"
            f"  3. Go to Local Model API and turn the server ON (toggle = blue)\n"
            f"  4. Then try again from MCP Inspector"
        )


if __name__ == "__main__":
    print(f"Starting Story Generator MCP Server...")
    print(f"Stories will be saved to: {STORIES_DIR}")
    mcp.run()
