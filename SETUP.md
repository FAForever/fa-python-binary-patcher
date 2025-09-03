# Python

To patch an exe you with Python patcher you obviously need Python interpreter.
Install newest version [here](https://www.python.org/downloads/).

# Compilers

You will need GCC and Clang compilers.

## Clang

Clang compiler installation:

* Goto [github releases of llvm](https://github.com/llvm/llvm-project/releases)
* Download latest one with **-x86_64-pc-windows-msvc** suffix
* Unpack into preferred location
* You need path to `/bin/clang++.exe`

## Visual Studio

* Goto [Visual Studio]( https://visualstudio.microsoft.com) official website
* Download latest version and install it
* Via *Visual Studio Installer* install **C++ x64/x86 build tools** (althrough I'm not sure if this is only one needed component, I'd suggest installing 'Desktop development with C++')

## GCC

GCC compiler installation:

* Install [chocolatey](https://chocolatey.org/)
* Run `choco install mingw --x86 -y --no-progress` which is gonna be installed at `C:\ProgramData\mingw64`.
* You need paths to `/mingw32/bin/g++.exe` and `/mingw32/bin/ld.exe`

# Patcher

After everything installed you need to clone patches repo.

Now you can setup build script:

```bat
python main.py [Path to patches folder] [Path to clang++.exe] [Path to ld.exe] [Path to g++.exe]
```

After you successfully build, you have to test what you've got.
You have 2 options:

* Running patched game with files from FAF client gamedata
* Running patched game with files from FAF repo

In both cases for better testing results you have to use [debugger](https://github.com/FAForever/FADeepProbe).

# IDE

For creating of patches **Visual Studio Code** is used with `ms-vscode.cpptools` extension, which can be installed with Extensions tab.
In preferences set default C++ formatter to `ms-vscode.cpptools`.

# Decompiler

TODO
