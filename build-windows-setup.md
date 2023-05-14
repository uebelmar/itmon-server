1. go to buildserver via teamviewer
2. open terminal and cd into "C:\Users\admin\OneDrive\Documents\GitHub\itmon-server"
3. run "pyinstaller .\windows.spec"
4. open inno setup & use "server-watchdog-windows-setup
5. increase version number in MyAppVersion
6. Build => Compile (new windows setup is now available under "C:\Users\admin\OneDrive\Documents\GitHub\server-watchdog-agent\Output"
7. cd into "C:\Users\admin\OneDrive\Documents\GitHub\server-watchdog-agent\releases"
8. create new folder for version (if not existing yet)
9. cd ..
9. mv Output/server-watchdog-agent-setup-<version>.exe releases/<version>/
10. git add *
11. git commit & git push