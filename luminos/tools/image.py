import openai
import os
import requests
from luminos.tools.basetool import BaseTool

class ImageTool(BaseTool):
    name = "ImageTool"
    
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
    
    def generate_image(self, prompt: str) -> str:
        """
        openai.function: generate_image
        Generate an image using OpenAI DALL-E 3 based on the given prompt. Returns the absolute path of the saved image.
        
        Arguments:
        - prompt: str -- The description of the image to generate.
        
        Returns:
        - str -- The absolute path to the saved image.
        """
        self.safe(f"Generate image with prompt: {prompt}")
        
        try:
            response = openai.Image.create(
                prompt=prompt,
                n=1,  # Number of images to generate
                size="1024x1024"  # Size of the generated image
            )
            image_url = response['data'][0]['url']
            image_data = requests.get(image_url).content

            # Ensure the directory exists
            image_dir = os.path.expanduser("~/.config/luminos/images")
            os.makedirs(image_dir, exist_ok=True)

            # Create the file name
            image_path = os.path.join(image_dir, f"{prompt.replace(' ', '_')[:50]}.png")

            # Save the image
            with open(image_path, "wb") as image_file:
                image_file.write(image_data)

            return image_path
        except Exception as e:
            raise RuntimeError(f"Failed to generate image: {e}")

# Example usage:
if __name__ == "__main__":
    prompt = "A futuristic city skyline at sunset"
    image_tool = ImageTool()
    print(image_tool.generate_image(prompt))
