from PIL import Image

def resize_image(image, new_width=100):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image
def grayify(image):
    return image.convert("L")
def pixels_to_ascii(image, ascii_chars):
    pixels = image.getdata()
    ascii_str = ""
    num_chars = len(ascii_chars)
    for pixel in pixels:
        intensity = pixel
        index = int(intensity / 256 * (num_chars - 1))
        ascii_str += ascii_chars[index]
    return ascii_str
def image_to_ascii(image_path, new_width=100, ascii_chars=None):
    try:
        image = Image.open(image_path)
        image = resize_image(image, new_width)
        image = grayify(image)
        ascii_str = pixels_to_ascii(image, ascii_chars)
        img_width = image.width
        ascii_str_len = len(ascii_str)
        ascii_img = ""
        for i in range(0, ascii_str_len, img_width):
            ascii_img += ascii_str[i:i + img_width] + "\n"
        return ascii_img
    except Exception as e:
        print("Error:", e)
        return None
def save_ascii_image(ascii_img, output_file="output.txt"):
    with open(output_file, "w") as f:
        f.write(ascii_img)
def get_ascii_symbols():
    print("Choose how many symbols you'd like to use for the ASCII art:")
    num_symbols = int(input("Enter the number of symbols (e.g., 2, 4, 6, 8): "))
    if num_symbols < 2:
        print("Minimum number of symbols is 2. Using 2 symbols by default.")
        num_symbols = 2
    available_symbols = ['.', ',', '-', '+', '*', '%', '#', '@', '&', '$']
    symbols = []
    for i in range(num_symbols):
        symbol = input(f"Enter symbol {i + 1}: ")
        if not symbol:
            symbol = available_symbols[i % len(available_symbols)]
        symbols.append(symbol)
    return symbols
if __name__ == "__main__":
    image_path = input("Enter the path to the image: ")
    try:
        new_width = int(input("Enter the desired width for the ASCII art: "))
    except ValueError:
        print("Invalid width entered. Using default width of 100.")
        new_width = 100
    ascii_chars = get_ascii_symbols()
    ascii_image = image_to_ascii(image_path, new_width, ascii_chars)
    if ascii_image:
        print(ascii_image)
        save_ascii_image(ascii_image)
        print("The ASCII art has been saved to 'output.txt'.")
