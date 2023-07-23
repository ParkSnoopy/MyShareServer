UNSAFES_BASE = set(filter(bool, open('localutils/unsafes/base.txt', 'r', encoding='utf-8').read().split()))
UNSAFES_ROOT = set(filter(bool, open('localutils/unsafes/root.txt', 'r', encoding='utf-8').read().split())) | UNSAFES_BASE
UNSAFES_USER = set(filter(bool, open('localutils/unsafes/user.txt', 'r', encoding='utf-8').read().split())) | UNSAFES_BASE

def safe_filename(filename, is_superuser=False) -> [bool, str]:
    # print(f"filename validation start, for {filename=}; {is_superuser=}")
    if is_superuser:
        # print("  is superuser")
        for unsafe in UNSAFES_ROOT:
            # print(f"    {unsafe=}")
            if unsafe in filename:
                # print("      hit")
                return False, unsafe
        return True, ''
    
    # print("  not superuser")
    for unsafe in UNSAFES_USER:
        # print(f"    {unsafe=}")
        if unsafe in filename:
            # print("      hit")
            return False, unsafe
    return True, ''
