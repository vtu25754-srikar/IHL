import os
import sys
from fastmcp import FastMCP
from openai import OpenAI

# Project directory where stories will be saved
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# Initialize the MCP Server named "Creative Story Generator"
mcp = FastMCP("Creative Story Generator")

# Connect to LM Studio's OpenAI-compatible local server
LM_STUDIO_URL = os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1")
lm_studio_client = OpenAI(
    base_url=LM_STUDIO_URL,
    api_key="lm-studio"  # LM Studio does not require a real API key
)

def get_available_model() -> str:
    """Fetch the first non-embedding model from LM Studio, or fallback to 'local-model'."""
    try:
        models = lm_studio_client.models.list()
        for m in models.data:
            if "embed" not in m.id.lower():
                return m.id
        if models.data:
            return models.data[0].id
    except Exception:
        pass
    return "local-model"

@mcp.tool()
def write_and_save_story(
    topic: str, 
    filename: str = "creative_story.txt", 
    genre: str = "fantasy",
    model_name: str = ""
) -> str:
    """
    Generates a highly creative story using a local LM Studio model 
    and saves the story into a text file.

    Args:
        topic: The plot idea, theme, or concept for the story.
        filename: The output filename (e.g., 'my_story.txt').
        genre: The genre of the story (e.g., 'fantasy', 'sci-fi', 'gothic mystery').
        model_name: Optional model ID to use. If left blank, automatically detects loaded LM Studio model.
    """

    # Ensure output file path is always inside the VTU25754 folder
    if not os.path.isabs(filename):
        save_path = os.path.join(PROJECT_DIR, filename)
    else:
        save_path = filename

    # Automatically detect model if not specified
    target_model = model_name if model_name else get_available_model()

    # Highly creative system prompt
    system_prompt = (
        "You are an award-winning master author known for rich sensory details, "
        "deep emotional resonance, vivid character voices, and unexpected narrative twists. "
        "Avoid generic tropes, clichés, and superficial descriptions. "
        "Craft prose with rhythm, elegance, and deep imagination."
    )

    user_prompt = f"Write an engaging, highly imaginative {genre} story based on this topic:\n{topic}"

    try:
        # Request story generation from local LM Studio model
        response = lm_studio_client.chat.completions.create(
            model=target_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.9,      # Higher temperature = more creativity and variety
            max_tokens=1500       # Token limit for story generation
        )

        story_content = response.choices[0].message.content

        # Save the generated story to a text file
        with open(save_path, "w", encoding="utf-8") as file:
            file.write(f"TITLE / TOPIC: {topic.upper()}\n")
            file.write(f"GENRE: {genre.capitalize()}\n")
            file.write(f"MODEL USED: {target_model}\n")
            file.write("=" * 50 + "\n\n")
            file.write(story_content)

        return f"Successfully generated story using '{target_model}' and saved to:\n{save_path}\n\nPreview:\n{story_content[:300]}..."

    except Exception as e:
        error_msg = (
            f"Error connecting to LM Studio at {LM_STUDIO_URL}: {str(e)}\n"
            "Please ensure LM Studio is running, a model is loaded, and Local Server is ON."
        )
        return error_msg

if __name__ == "__main__":
    mcp.run()
