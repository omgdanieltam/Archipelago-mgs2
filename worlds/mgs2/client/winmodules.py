"""
List loaded modules (EXE + DLLs) of a process, by calling the Windows API
directly via ctypes instead of relying on pymem's own (inconsistent across
versions) module-listing helpers.
"""

import ctypes
from ctypes import wintypes

psapi = ctypes.WinDLL("psapi", use_last_error=True)

LIST_MODULES_ALL = 0x03
MAX_MODULES = 2048


class MODULEINFO(ctypes.Structure):
    _fields_ = [
        ("lpBaseOfDll", wintypes.LPVOID),
        ("SizeOfImage", wintypes.DWORD),
        ("EntryPoint", wintypes.LPVOID),
    ]


psapi.EnumProcessModulesEx.argtypes = [
    wintypes.HANDLE,
    ctypes.POINTER(wintypes.HMODULE),
    wintypes.DWORD,
    ctypes.POINTER(wintypes.DWORD),
    wintypes.DWORD,
]
psapi.EnumProcessModulesEx.restype = wintypes.BOOL

psapi.GetModuleBaseNameW.argtypes = [
    wintypes.HANDLE,
    wintypes.HMODULE,
    wintypes.LPWSTR,
    wintypes.DWORD,
]
psapi.GetModuleBaseNameW.restype = wintypes.DWORD

psapi.GetModuleInformation.argtypes = [
    wintypes.HANDLE,
    wintypes.HMODULE,
    ctypes.POINTER(MODULEINFO),
    wintypes.DWORD,
]
psapi.GetModuleInformation.restype = wintypes.BOOL

psapi.GetModuleFileNameExW.argtypes = [
    wintypes.HANDLE,
    wintypes.HMODULE,
    wintypes.LPWSTR,
    wintypes.DWORD,
]
psapi.GetModuleFileNameExW.restype = wintypes.DWORD


def main_module_path(process_handle: int) -> str | None:
    """Full path of the process's own executable -- which is how we locate the
    game's install directory without asking for it."""
    buf = ctypes.create_unicode_buffer(32768)
    written = psapi.GetModuleFileNameExW(
        wintypes.HANDLE(process_handle), None, buf, len(buf)
    )
    return buf.value if written else None


class Module:
    def __init__(self, name: str, base: int, size: int):
        self.name = name
        self.base = base
        self.size = size

    def contains(self, address: int) -> bool:
        return self.base <= address < self.base + self.size


def list_modules(process_handle: int) -> list[Module]:
    handle = wintypes.HANDLE(process_handle)

    hmods = (wintypes.HMODULE * MAX_MODULES)()
    needed = wintypes.DWORD()

    ok = psapi.EnumProcessModulesEx(
        handle,
        hmods,
        ctypes.sizeof(hmods),
        ctypes.byref(needed),
        LIST_MODULES_ALL,
    )
    if not ok:
        raise ctypes.WinError(ctypes.get_last_error())

    count = min(MAX_MODULES, needed.value // ctypes.sizeof(wintypes.HMODULE))

    modules = []
    for i in range(count):
        hmod = hmods[i]

        name_buf = ctypes.create_unicode_buffer(260)
        psapi.GetModuleBaseNameW(handle, hmod, name_buf, 260)

        info = MODULEINFO()
        psapi.GetModuleInformation(handle, hmod, ctypes.byref(info), ctypes.sizeof(info))

        base = int(info.lpBaseOfDll or 0)
        modules.append(Module(name_buf.value, base, info.SizeOfImage))

    return modules
