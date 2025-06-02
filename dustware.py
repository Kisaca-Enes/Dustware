import os
a = r"""
$$$$$$$\                        $$\                                                 
$$  __$$\                       $$ |                                                
$$ |  $$ |$$\   $$\  $$$$$$$\ $$$$$$\   $$\  $$\  $$\  $$$$$$\   $$$$$$\   $$$$$$\  
$$ |  $$ |$$ |  $$ |$$  _____|\_$$  _|  $$ | $$ | $$ | \____$$\ $$  __$$\ $$  __$$\ 
$$ |  $$ |$$ |  $$ |\$$$$$$\    $$ |    $$ | $$ | $$ | $$$$$$$ |$$ |  \__|$$$$$$$$ |
$$ |  $$ |$$ |  $$ | \____$$\   $$ |$$\ $$ | $$ | $$ |$$  __$$ |$$ |      $$   ____|
$$$$$$$  |\$$$$$$  |$$$$$$$  |  \$$$$  |\$$$$$\$$$$  |\$$$$$$$ |$$ |      \$$$$$$$\ 
\_______/  \______/ \_______/    \____/  \_____\____/  \_______|\__|       \_______|
                                                                                    
                                                                                    
                                                                                    
                                                                        
"""
print(a)
print("kisaca-enes")
print("""
------------------
1:c2
2.ramsoware pyload
3:server
4:macro exploits
5:kalıcılık
6:bypass
7:generator
-----------------
""")
x = input("seçin: ")
if x == "1":
	os.system("python3 c2.py")
elif x == "2":
	os.system("python3 r.py")
elif x == "3":
	os.system("python3 server.py")
elif x == "4":
	os.system("python3 macro.py")
elif x == "5":
	os.system("python3 kalıcılık.py")
elif x == "6":
	os.system("python3 bypass.py")
elif x == "7":
	os.system("python3 generator.py")
