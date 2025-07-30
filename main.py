
import os 
from add_logo import add_logo_to_image
def main():
    # Get user input
    # image_path = input("Enter the path to your image (e.g., image.jpg): ").strip()
    # language = input("Enter the language of the logo (e.g., urdu, english): ").strip().lower()
    image_path ="image.jpg"
    language = "India"
# BBC_News_Linear_Urdu_LTR_RGB
    logo_filename = f"BBC_News_Linear_{language}_RGB.png"
    logo_path =f"logos/{language}/Linear/Web/RGB/{logo_filename}"
    if not os.path.exists(image_path):
        print(f"Image file not found: {image_path}")
        return
    if not os.path.exists(logo_path):
        print(f"Logo file for language '{language}' not found in 'logos/' folder.")
        return
    add_logo_to_image(image_path, logo_path,language)


if __name__ == "__main__":
    main()