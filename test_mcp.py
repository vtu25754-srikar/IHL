"""
Test script to invoke the write_and_save_story tool directly.
"""
from server import write_and_save_story

if __name__ == "__main__":
    print("Testing Creative Story Generator Tool...")
    topic = "A mysterious compass that points to what the holder lost most recently"
    genre = "gothic fantasy"
    filename = "test_story.txt"

    print(f"Topic: {topic}")
    print(f"Genre: {genre}")
    print(f"Output File: {filename}")
    print("-" * 50)
    
    result = write_and_save_story(topic=topic, filename=filename, genre=genre)
    print(result)
