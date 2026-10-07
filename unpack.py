import os, sys, shutil, tarfile, io, lzma, base64

if not os.path.exists('chunks'):
    print('Chunks already unpacked or not present.')
    sys.exit(0)

print('Reassembling archive chunks...')
b64 = ''
for i in range(1, 7):
    chunk_path = f'chunks/part_{i}.b64'
    if os.path.exists(chunk_path):
        with open(chunk_path, 'r', encoding='utf-8') as f:
            b64 += f.read().strip()

print(f'Total base64 length: {len(b64)}')
raw = base64.b64decode(b64)
with tarfile.open(fileobj=io.BytesIO(raw), mode='r:*') as tar:
    tar.extractall('.')
print('Extracted base files (code, JSONs, new textures).')

print('Restoring remaining textures and structures from DoctorAnantModv4...')
v4_dir = '/tmp/v4_repo'
if os.path.exists(v4_dir):
    shutil.rmtree(v4_dir)

res = os.system(f'git clone --depth 1 https://github.com/ananttomar232-tech/DoctorAnantModv4.git {v4_dir}')
if res == 0 and os.path.exists(v4_dir):
    src_tex = os.path.join(v4_dir, 'src/main/resources/assets/dranant/textures')
    dst_tex = 'src/main/resources/assets/dranant/textures'
    if os.path.exists(src_tex):
        os.makedirs(dst_tex, exist_ok=True)
        os.system(f'cp -rn {src_tex}/* {dst_tex}/')
        print('Restored textures from v4')

    src_struct = os.path.join(v4_dir, 'src/main/resources/data/dranant/structure')
    dst_struct = 'src/main/resources/data/dranant/structure'
    if os.path.exists(src_struct):
        os.makedirs(dst_struct, exist_ok=True)
        os.system(f'cp -rn {src_struct}/* {dst_struct}/')
        print('Restored structures from v4')

    src_gw = os.path.join(v4_dir, 'gradle/wrapper/gradle-wrapper.jar')
    if os.path.exists(src_gw):
        os.makedirs('gradle/wrapper', exist_ok=True)
        shutil.copy2(src_gw, 'gradle/wrapper/gradle-wrapper.jar')
        print('Restored gradle-wrapper.jar')

shutil.rmtree('chunks', ignore_errors=True)
if os.path.exists('unpack.py'):
    os.remove('unpack.py')

print('Unpack complete!')
