from cx_Freeze import setup, Executable


# On appelle la fonction setup

setup(

    name = "Sputefix Game Engine",

    version = "1.0",

    description = "This is a easy-to-use Game Engine, you just code a game on a separate file and launch it with the executable! (Text editor NOT included)",

    executables = [Executable("Sputefix Game Engine.py")],

)