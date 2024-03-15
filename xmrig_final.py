import sys, os, fnmatch, glob, shutil
import tarfile, zipfile
import secrets

# make function to find all archives related to xmrig

def findXMRigFiles():
    from sys import platform
    result = []
    # username = pwd.getpwuid(os.getuid()).pw_name
    if platform == "linux" or platform == "linux2":
        findPath = "/home/"+os.getlogin()+"/Downloads"
    elif platform == "win32":
        findPath = "C:\\Users\\"+os.getlogin()+"\\Downloads"
    elif platform == "darwin":
        findPath = "/Users/"+os.getlogin()+"/Downloads"
    else:
        # assume unix-like
        findpath = "/home/"+os.getlogin()+"/Downloads"
    for root, dirs, files in os.walk(findPath):
        for name in files:
            if fnmatch.fnmatch(name, 'xmrig*'):
                result.append(os.path.join(root,name))
    return result

# function to download from XMRig API and download them to Downloads folders

def downloadXMRigFiles():
    from sys import platform
    import requests
    result = []
    # username = pwd.getpwuid(os.getuid()).pw_name
    savepath ="/"
    url = "https://api.xmrig.com/1/latest_release/xmrig"
    r = requests.get(url)
    if r.status_code == 200:
        r = r.json()
        if platform == "linux" or platform == "linux2":
            useId = "linux-x64"
        elif platform == "win32":
            useId = "msvc-win64"
        elif platform == "darwin":
            useId = "macos-x64"
        else:
            useId = "freebsd-static-x64"
        for i in range(len(r["assets"])):
            if r['assets'][i]['id'] == useId:
                useIndex = i
                downloadURL = r['assets'][i]['url']
        down = requests.get(downloadURL)
        with open(savepath+"/"+r['assets'][useIndex]["name"], 'wb') as file:
            file.write(down.content)
        result.append(savepath+"/"+r['assets'][useIndex]["name"])
        return result
    else:
        return []



# make function to unarchive them all to /tmp
# find exe and add hash

def addRandomBytes(file):
    with open(file, 'ab+') as fd:
        fd.write(secrets.token_bytes(20))

# archive them all again
def prepare_archive(dirPath, ext):
    if ext == "zip":
        newFile = dirPath + '.zip'
        with zipfile.ZipFile(newFile, 'w', zipfile.ZIP_DEFLATED) as zipRef:
            for path, dirNames, files in os.walk(dirPath):
                if sys.platform == "win32":
                    replacePath = "Users\\AppData\\Local\\Uptycs"
                else:
                    replacePath = "/tmp/uptycs"
                fPath = path.replace(dirPath, dirPath.replace(replacePath, ''))
                fPath = fPath and fPath + os.sep
                # write each file
                for file in files:
                    zipRef.write(os.path.join(dirPath, file), fPath + file)
            zipRef.close()
    elif ext == "tar.gz":
        with tarfile.open(dirPath+'.tar.gz', "w:gz") as tar:
            tar.add(dirPath, arcname=os.path.basename(dirPath))


def main():
    # find all XMRigFiles
    #files = findXMRigFiles()
    files = downloadXMRigFiles()
    print("File Downloaded. Changing hashes...")
    if sys.platform == "win32":
        basePath = "C:\\Users\\AppData\\Local\\Uptycs"
    else:
        # assume Unix-like
        basePath = "/tmp/uptycs"
    for i in files:
        if i[-3:] == "zip":
            with zipfile.ZipFile(i, 'r') as zip_ref:
                zip_ref.extractall(basePath)
        elif i[-6:] == "tar.gz":
            with tarfile.open(i) as tar_ref:
                tar_ref.extractall(basePath)
        xmrFiles = glob.glob(basePath+'/xmrig*/xmrig*', recursive=True)
        for file in xmrFiles:
            addRandomBytes(file)
        # archive again
        path = glob.glob(basePath+'/xmrig*')[0]
        if file[-3:] == "exe":
            # it's windows
            prepare_archive(path, 'zip')
        else:
            # assume tar.gz
            prepare_archive(path, 'tar.gz')
        for file in xmrFiles:
            os.system(file)
        # delete xmrig folder after everything
        shutil.rmtree(glob.glob(basePath+'/xmrig**/')[0])
        # username = pwd.getpwuid(os.getuid()).pw_name
        for file in glob.glob(basePath+'/xmrig*'):
            print(file, i)
            shutil.copy(file, i)
        print("successfully copied", len(i), "files")
        shutil.rmtree(basePath)


main()
