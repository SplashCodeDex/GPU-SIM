- i want to simulate real GPU that will show in task manager, dxdiag and settings on windows.
- Windows Softwares and Applications can detect it even though there is no physical GPU.

## the Agenda
Imagine i convinced my friend that my PC has Nvidia Dedicated GPU (780ti (4GB VRAM)) even though it is not. Now, my friend will want to verify so they will check task manager, dxdiag and settings. They will then want to find, open and verify the Nvidia Control Panel.

so now i want to simulate real GPU that will show in task manager, dxdiag and settings on windows by which this project is doing(can be enhanced): W:\CodeDeX\GPU-SIM\dist\GPU-SIM.exe

I also want a dedicated Nvidia Control Panel app exactly identical to the real control panel with logo, colors, branding. W:\CodeDeX\GPU-SIM\Agenda\512x512.png
W:\CodeDeX\GPU-SIM\Agenda\dark-mode.png
W:\CodeDeX\GPU-SIM\Agenda\ligth-mode.png
W:\CodeDeX\GPU-SIM\Agenda\NVIDIA-Control-Panel.jpg

This Control Panel will be the main standalone app that will be installed to trick and convince my friend that it is the real Nvidia Control Panel and its values should match the spoofed values that is showing up in settings, dxdiag and Task manager. The GeForce Experience app will be additional app to be installed and will be more convincing.

The idea is that, this project should be able to build the GPU-SIM.exe version tagged on Github so before i present my PC to my friend for verification, I will head to the github repo release and download the latest GPU-SIM.exe, install and open it. I then configure it according to the profile i want, make it reflect in windows settings, dxdiag and Task manager. Then i click a button to install the control panel, optional GeForce Experience, and then present my PC to my friend.

# The Flow
1. Go to GitHub releases → Download GPU-SIM.exe
2. Install and open GPU-SIM
3. Select a GPU profile (e.g., GTX 780 Ti), configure other settings to user's preference.
4. Click "Apply" → Registry changes make Windows think I have that GPU.
5. Click a button in GPU-SIM to install NVIDIA Control Panel (so your friend can open it)
6. Optional button in GPU-SIM to install GeForce Experience and can also install it later from the installed NVIDIA Control Panel App
7. Present your PC to your friend for verification
