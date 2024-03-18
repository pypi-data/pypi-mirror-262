# Chroma Palette - Text Styling Library

The Chroma Palette is a Python module designed to provide comprehensive text styling capabilities for terminal applications. It utilizes ANSI escape codes to apply various styles, colors, decorations, alignments, and shadow effects to text output, enhancing the visual presentation of terminal-based interfaces.

## Installation

Install the librery by using `pip install chroma_palette` .


## Features

### Text Styles

- **Bold:** Make text bold and prominent.
  ```python
  styled_text = chroma_palette.styled_text("Hello, world!", style=chroma_palette.TextStyle.BOLD)
  print(styled_text)
  ```

- **Italic:** Slant text slightly for emphasis.
  ```python
  styled_text = chroma_palette.styled_text("Hello, world!", style=chroma_palette.TextStyle.ITALIC)
  print(styled_text)
  ```

- **Underline:** Add a line beneath the text.
  ```python
  styled_text = chroma_palette.styled_text("Hello, world!", style=chroma_palette.TextStyle.UNDERLINE)
  print(styled_text)
  ```

- **Strikethrough:** Draw a line through the text.
  ```python
  styled_text = chroma_palette.styled_text("Hello, world!", style=chroma_palette.TextStyle.STRIKETHROUGH)
  print(styled_text)
  ```

### Text Colors

Choose from a range of foreground text colors including black, red, green, yellow, blue, magenta, cyan, light gray, dark gray, and more.

- **Example:**
  ```python
  styled_text = chroma_palette.styled_text("Hello, world!", color=chroma_palette.TextColor.RED)
  print(styled_text)
  ```

### Background Colors

Set background colors for text to improve readability and aesthetics.

- **Example:**
  ```python
  styled_text = chroma_palette.styled_text("Hello, world!", background=chroma_palette.BackgroundColor.GREEN)
  print(styled_text)
  ```

### Text Decorations

- **Bold:** Make text bold and prominent.
  ```python
  styled_text = chroma_palette.styled_text("Hello, world!", decoration=chroma_palette.TextDecoration.BOLD)
  print(styled_text)
  ```

- **Dim:** Apply a dim effect to the text.
  ```python
  styled_text = chroma_palette.styled_text("Hello, world!", decoration=chroma_palette.TextDecoration.DIM)
  print(styled_text)
  ```

- **Italic:** Slant text slightly for emphasis.
  ```python
  styled_text = chroma_palette.styled_text("Hello, world!", decoration=chroma_palette.TextDecoration.ITALIC)
  print(styled_text)
  ```

- **Underline:** Add a line beneath the text.
  ```python
  styled_text = chroma_palette.styled_text("Hello, world!", decoration=chroma_palette.TextDecoration.UNDERLINE)
  print(styled_text)
  ```

- **Blink:** Cause the text to blink.
  ```python
  styled_text = chroma_palette.styled_text("Hello, world!", decoration=chroma_palette.TextDecoration.BLINK)
  print(styled_text)
  ```

- **Reverse:** Reverse the foreground and background colors.
  ```python
  styled_text = chroma_palette.styled_text("Hello, world!", decoration=chroma_palette.TextDecoration.REVERSE)
  print(styled_text)
  ```

- **Hidden:** Hide the text.
  ```python
  styled_text = chroma_palette.styled_text("Hello, world!", decoration=chroma_palette.TextDecoration.HIDDEN)
  print(styled_text)
  ```

- **Strikethrough:** Draw a line through the text.
  ```python
  styled_text = chroma_palette.styled_text("Hello, world!", decoration=chroma_palette.TextDecoration.STRIKETHROUGH)
  print(styled_text)
  ```

### Text Alignments

Align text to the left, center, or right within the terminal window.

- **Example:**
  ```python
  styled_text = chroma_palette.styled_text("Hello, world!", alignment=chroma_palette.TextAlignment.CENTER)
  print(styled_text)
  ```

### Dynamic Color Selection

Convert RGB color values to ANSI escape codes for dynamic color selection.

- **Example:**
  ```python
  dynamic_color = chroma_palette.dynamic_color_selection(255, 0, 0)  # Red
  styled_text = chroma_palette.styled_text("Hello, world!", color=dynamic_color)
  print(styled_text)
  ```

### Interactive Help Menu

Display an interactive help menu with detailed information on available features and usage instructions.

- **Example:**
  ```python
  chroma_palette.help()
  ```


## Documentation

For detailed documentation including function signatures, parameters, and usage examples, refer to the code comments within the `chroma_palette.py` file.

## Contributing

Contributions to the Chroma Palette are welcome! If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request on the GitHub repository.

## License

This project is licensed under the [MIT License](LICENSE).
