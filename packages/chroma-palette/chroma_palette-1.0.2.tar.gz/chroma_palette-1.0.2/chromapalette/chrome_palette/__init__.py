class TextStyle:
 
    # ANSI escape codes for text styles.
    
    RESET = '\033[0m'
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    STRIKETHROUGH = '\033[9m'

class TextColor:

    # ANSI escape codes for text colors.

    DEFAULT = '\033[39m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    LIGHT_GRAY = '\033[37m'
    DARK_GRAY = '\033[90m'
    LIGHT_RED = '\033[91m'
    LIGHT_GREEN = '\033[92m'
    LIGHT_YELLOW = '\033[93m'
    LIGHT_BLUE = '\033[94m'
    LIGHT_MAGENTA = '\033[95m'
    LIGHT_CYAN = '\033[96m'
    WHITE = '\033[97m'

class BackgroundColor:
  
    # ANSI escape codes for background colors.
 
    DEFAULT = '\033[49m'
    BLACK = '\033[40m'
    RED = '\033[41m'
    GREEN = '\033[42m'
    YELLOW = '\033[43m'
    BLUE = '\033[44m'
    MAGENTA = '\033[45m'
    CYAN = '\033[46m'
    LIGHT_GRAY = '\033[47m'
    DARK_GRAY = '\033[100m'
    LIGHT_RED = '\033[101m'
    LIGHT_GREEN = '\033[102m'
    LIGHT_YELLOW = '\033[103m'
    LIGHT_BLUE = '\033[104m'
    LIGHT_MAGENTA = '\033[105m'
    LIGHT_CYAN = '\033[106m'
    WHITE = '\033[107m'

class TextDecoration:

    # ANSI escape codes for text decorations.

    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    BLINK_FAST = '\033[6m'
    REVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    STRIKETHROUGH = '\033[9m'

class TextAlignment:

    # ANSI escape codes for text alignment.
  
    LEFT = '\033[0m'
    CENTER = '\033[1m'
    RIGHT = '\033[2m'



def styled_text(text, style='', color='', background='', decoration='', alignment='', shadow=''):
   
    # Apply styling, color, decoration, alignment, and shadow to the given text.
    
    shadow_style = f'\033[38;2;{shadow};48;2;{shadow}m' if shadow else ''
    return f"{alignment}{style}{color}{background}{decoration}{shadow_style}{text}{TextStyle.RESET}"

def dynamic_color_selection(r, g, b):
    
    # Convert RGB color values to ANSI escape code for dynamic color selection.
    
    return f'\033[38;2;{r};{g};{b}m'


def help():
    
    # Display an interactive help menu with a stylized layout.
    
    print("╔═══════════════════════════════════════╗")
    print("║     Text Styling Library Help         ║")
    print("╠═══════════════════════════════════════╣")
    print("║ Available Features:                   ║")
    print("║ 1. Text Styles                        ║")
    print("║ 2. Text Colors                        ║")
    print("║ 3. Background Colors                  ║")
    print("║ 4. Text Decorations                   ║")
    print("║ 5. Text Alignments                    ║")
    print("║ 6. Usage                              ║")
    print("║ 7. Exit                               ║")
    print("╚═══════════════════════════════════════╝")

    while True:
        choice = input("Enter the number of the feature you want to learn more about (or 'exit' to quit): ").strip().lower()

        if choice == 7 or choice == 'exit':
            print("Exiting help menu.")
            break
        elif choice == '1':
            print("\nText Styles:")
            print("  - BOLD: Makes the text bold and more prominent.")
            print("  - ITALIC: Slants the text slightly for emphasis.")
            print("  - UNDERLINE: Adds a line beneath the text.")
            print("  - STRIKETHROUGH: Draws a line through the text.")
        elif choice == '2':
            print("\nText Colors:")
            print("  - BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, LIGHT_GRAY, DARK_GRAY,")
            print("    LIGHT_RED, LIGHT_GREEN, LIGHT_YELLOW, LIGHT_BLUE, LIGHT_MAGENTA, LIGHT_CYAN, WHITE")
        elif choice == '3':
            print("\nBackground Colors:")
            print("  - BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, LIGHT_GRAY, DARK_GRAY,")
            print("    LIGHT_RED, LIGHT_GREEN, LIGHT_YELLOW, LIGHT_BLUE, LIGHT_MAGENTA, LIGHT_CYAN, WHITE")
        elif choice == '4':
            print("\nText Decorations:")
            print("  - BOLD: Makes the text bold and more prominent.")
            print("  - DIM: Applies a dim effect to the text.")
            print("  - ITALIC: Slants the text slightly for emphasis.")
            print("  - UNDERLINE: Adds a line beneath the text.")
            print("  - BLINK: Causes the text to blink.")
            print("  - BLINK_FAST: Causes the text to blink rapidly.")
            print("  - REVERSE: Reverses the foreground and background colors.")
            print("  - HIDDEN: Hides the text.")
            print("  - STRIKETHROUGH: Draws a line through the text.")
        elif choice == '5':
            print("\nText Alignments:")
            print("  - LEFT: Aligns text to the left.")
            print("  - CENTER: Centers the text horizontally.")
            print("  - RIGHT: Aligns text to the right.")
        elif choice == '6':
            print("\nUsage:")
            print("  styled_text(text, style='', color='', background='', decoration='', alignment='')")
        else:
            print("Invalid input. Please enter a valid feature number or 'exit' to quit.")
