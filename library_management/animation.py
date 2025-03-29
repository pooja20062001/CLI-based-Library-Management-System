import sys
import time

def loader(message, duration):
    chars = [ ' | ', ' / ',' - ',' \\ ' ]
    print(message, end="", flush=True)
    for _ in range (duration +2):
       for char in chars:
        sys.stdout.write(f'\r{message} {char}')
        sys.stdout.flush()
        time.sleep(0.25) #Char accleration speed if needed
    sys.stdout.write('\r' + ' ' * (len(message) + 2) + '\r') #Clear line
    
def dot_loader(message, duration):
    dots = ["",".","..","...","....",".....","....","...","..","."]
    start_time = time.time()
    while time.time() - start_time < duration:
        for dot in dots:
            sys.stdout.write(f'\r{message} {dot}  ') #Space to clear previous dot
            sys.stdout.flush()
            time.sleep(0.3)
    sys.stdout.write('\r' + ' ' * (len(message)  + 6) + '\r') #Clear line