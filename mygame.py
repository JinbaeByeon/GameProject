import game_framework
import start_state
import platform
import os

if platform.architecture()[0] == '32bit':
    os.environ["PYSDL_DLL_PATH"] = "./SDL2/x86"
else:
    os.environ["PYSDL_DLL_PATH"] = "./SDL2/x64"

game_framework.run(start_state)