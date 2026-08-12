import sys
import os
from server import write_and_save_story

if __name__ == "__main__":
    if len(sys.argv) > 1:
        topic = sys.argv[1]
    else:
        topic = "An ancient clock tower that ticks backward"

    if len(sys.argv) > 2:
        filename = sys.argv[2]
    else:
        filename = "story_output.txt"

    if len(sys.argv) > 3:
        genre = sys.argv[3]
    else:
        genre = "fantasy"

    print(f"Generating story for topic: '{topic}'...")
    print(f"Output filename: '{filename}'...")
    
    result = write_and_save_story(topic=topic, filename=filename, genre=genre)
    print(result)
