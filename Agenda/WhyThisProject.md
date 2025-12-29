- i want to simulate real GPU that will show in task manager, dxdiag and settings on windows.
- Windows Softwares and Applications can detect it even though there is no physical GPU.

## the Agenda
Imagine i convinced my friend that my PC has Nvidia Dedicated GPU (1650 (4GB VRAM)) even though it is not. Now, my friend will want to verify so they will check task manager, dxdiag and settings. They will then want to find, open and verify the Nvidia Control Panel.

I want to simulate real GPU and This Control Panel will be the main standalone app that will be installed to trick and convince my friend that it is the real Nvidia Control Panel and its values should match the spoofed values that is showing up in

Future Enhancement(don't worry about it now): will show in task manager, dxdiag and settings on windows.


# The Flow
1. Push changes with tag to github
2. Github Action trigger to build and release NvidiaControlPanel.exe
3. I download NvidiaControlPanel.exe from GitHub releases
4. Install and open NvidiaControlPanel
5. open NvidiaControlPanel.exe (e.g., GTX 1650)
6. Present my PC to my friend for verification
