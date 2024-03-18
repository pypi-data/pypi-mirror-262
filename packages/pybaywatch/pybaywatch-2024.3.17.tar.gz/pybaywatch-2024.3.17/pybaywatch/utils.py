import colorama as ca

def p_header(text):
    # return cprint(text, 'cyan', attrs=['bold'])  # lib: termcolor
    print(ca.Fore.CYAN + ca.Style.BRIGHT + text)
    print(ca.Style.RESET_ALL, end='')

def p_hint(text):
    # return cprint(text, 'grey', attrs=['bold'])  # lib: termcolor
    print(ca.Fore.LIGHTBLACK_EX + ca.Style.BRIGHT + text)
    print(ca.Style.RESET_ALL, end='')

def p_success(text):
    # return cprint(text, 'green', attrs=['bold'])  # lib: termcolor
    print(ca.Fore.GREEN + ca.Style.BRIGHT + text)
    print(ca.Style.RESET_ALL, end='')

def p_fail(text):
    # return cprint(text, 'red', attrs=['bold'])  # lib: termcolor
    print(ca.Fore.RED + ca.Style.BRIGHT + text)
    print(ca.Style.RESET_ALL, end='')

def p_warning(text):
    # return cprint(text, 'yellow', attrs=['bold'])  # lib: termcolor
    print(ca.Fore.YELLOW + ca.Style.BRIGHT + text)
    print(ca.Style.RESET_ALL, end='')