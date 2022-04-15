# vkpurge-pyqt
This little program is basically just a GUI wrapper/frontend for the [Void Linux](https://voidlinux.org/) tool named [vkpurge](https://man.voidlinux.org/vkpurge.8). It is built using Python with PyQt5, and is made out of curiosity.

This project is not affiliated with Void Linux in any way.

<p align="center">
<img src="https://imgur.com/x3jLouz.png" width="560" ><br/>
</p>

<p align="center">
<img src="https://imgur.com/cwXAavG.png" width="560" ><br/>
</p>

## Required Packages
* python3
* python3-PyQt5
* (and obviously, their dependencies)

## How to use
1. Install the prerequisites

    sudo xbps-install -Su python3 python3-PyQt5

2. Clone this repo

3. Switch to the newly created directory and run main.py

    python3 main.py

## Notes
* The removal window might or might not write the console output in it, I couldn't test it further because I've run out of removable kernels. It should work otherwise.
* You can use Shift + Left Click to select multiple kernels in the list.