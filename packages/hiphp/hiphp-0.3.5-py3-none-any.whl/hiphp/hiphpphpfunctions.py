#!/usr/bin/env python
# coding:utf-8
#   |                                                         |   #
# --+---------------------------------------------------------+-- #
#   |    Code by: yasserbdj96                                 |   #
#   |    Email: yasser.bdj96@gmail.com                        |   #
#   |    GitHub: github.com/yasserbdj96                       |   #
#   |    Sponsor: github.com/sponsors/yasserbdj96             |   #
#   |    BTC: bc1q2dks8w8uurca5xmfwv4jwl7upehyjjakr3xga9      |   #
#   |                                                         |   #
#   |    All posts with #yasserbdj96                          |   #
#   |    All views are my own.                                |   #
# --+---------------------------------------------------------+-- #
#   |                                                         |   #

#START{
#
def scandir(dirx="./"):
    x="""
$path='"""+dirx+"""';
if(!is_dir($path)) {
    echo json_encode(["[✗] The Directory '{$path}' not exists"]);
    exit();
}

$fileList=array();
if($handle=opendir($path)){
    while(false!==($entry=readdir($handle))){
        if($entry!="." && $entry!=".."){
            if(is_dir($entry)){
                $entry=$path.$entry."/";
            }else{
                $entry=$path.$entry;
            }
            $fileList[]=$entry;
        }
    }
    closedir($handle);
}
echo json_encode($fileList);"""
    return x
#
def scandir_all(dirx="./"):
    x="""
function getDirContents($dir="./",$relativePath=false){

    if(!is_dir($dir)) {
        return ["[✗] The Directory '{$dir}' not exists"];
    }

    $fileList=array();
    $iterator=new RecursiveIteratorIterator(new RecursiveDirectoryIterator($dir));
    foreach($iterator as $file){
        if ($file->isDir()) continue;
        $path=$file->getPathname();
        if ($relativePath) {
            $path=str_replace($dir,'',$path);
            $path=ltrim($path, '/');
        }

        $perms = fileperms($path);

        switch ($perms & 0xF000) {
            case 0xC000: // socket
                $info = 's';
                break;
            case 0xA000: // symbolic link
                $info = 'l';
                break;
            case 0x8000: // regular
                $info = 'r';
                break;
            case 0x6000: // block special
                $info = 'b';
                break;
            case 0x4000: // directory
                $info = 'd';
                break;
            case 0x2000: // character special
                $info = 'c';
                break;
            case 0x1000: // FIFO pipe
                $info = 'p';
                break;
            default: // unknown
                $info = 'u';
        }

        // Owner
        $info .= (($perms & 0x0100) ? 'r' : '-');
        $info .= (($perms & 0x0080) ? 'w' : '-');
        $info .= (($perms & 0x0040) ?
                    (($perms & 0x0800) ? 's' : 'x' ) :
                    (($perms & 0x0800) ? 'S' : '-'));

        // Group
        $info .= (($perms & 0x0020) ? 'r' : '-');
        $info .= (($perms & 0x0010) ? 'w' : '-');
        $info .= (($perms & 0x0008) ?
                    (($perms & 0x0400) ? 's' : 'x' ) :
                    (($perms & 0x0400) ? 'S' : '-'));

        // World
        $info .= (($perms & 0x0004) ? 'r' : '-');
        $info .= (($perms & 0x0002) ? 'w' : '-');
        $info .= (($perms & 0x0001) ?
                    (($perms & 0x0200) ? 't' : 'x' ) :
                    (($perms & 0x0200) ? 'T' : '-'));

        $file_stats = stat($path);

        //
        $last_use=date('M d H:m',$file_stats["mtime"]);

        //
        $bytes=filesize($path);
        if ($bytes >= 1073741824){
            $bytes = number_format($bytes / 1073741824, 2) . ' GB';
        }elseif ($bytes >= 1048576){
            $bytes = number_format($bytes / 1048576, 2) . ' MB';
        }elseif ($bytes >= 1024){
            $bytes = number_format($bytes / 1024, 2) . ' KB';
        }elseif ($bytes > 1){
            $bytes = $bytes . ' bytes';
        }elseif ($bytes == 1){
                $bytes = $bytes . ' byte';
        }else{
            $bytes = '0 bytes';
        }

        if(strlen($bytes)<11){
            $s=11-strlen($bytes);
            $bytes=str_repeat(" ",$s).$bytes;
        }

        //
        $fileList[]=$info." ".$last_use." ".$bytes." ".$path;
    }
    return $fileList;
}
echo json_encode(getDirContents('"""+dirx+"""'));"""
    return x
#
def file_get_contents(dirx):
    return f"""echo file_get_contents('{dirx}');"""

def simulate_mv(path, newpath):
    php_code = f"""
    // Check if the source file or directory exists
    if (!file_exists('{path}')) {{
        echo "[✗] Source doesn't exist.";
        return;
    }}

    // Check if the destination exists
    if (file_exists('{newpath}')) {{
        echo "[!] Destination already exists. Please choose a different destination.";
        return;
    }}

    // Check if the source is a file
    if (is_file('{path}')) {{
        // Move the file to the destination
        if (rename('{path}', '{newpath}')) {{
            echo "[✓] File moved successfully.";
        }} else {{
            echo "[✗] Error moving the file.";
        }}
    }} elseif (is_dir('{path}')) {{
        // Move the directory to the destination
        if (mkdir('{newpath}') && rename('{path}', '{newpath}/' . basename('{path}'))) {{
            echo "[✓] Directory moved successfully.";
        }} else {{
            echo "[✗] Error moving the directory.";
        }}
    }} else {{
        echo "[✗] Unsupported source type.";
    }}
    """

    return php_code



#
def zip_path(path="./"):
    php_zip_code="""// Get real path for our folder
$rootPath = realpath('"""+path+"""');

$path_name=str_replace(DIRECTORY_SEPARATOR, '_', '"""+path+"""');

$hash=$path_name."_".date("ymdHis");

// Initialize archive object
$zip = new ZipArchive();
$zip->open($hash.'.zip', ZipArchive::CREATE | ZipArchive::OVERWRITE);

// Create recursive directory iterator
/** @var SplFileInfo[] $files */
$files = new RecursiveIteratorIterator(
    new RecursiveDirectoryIterator($rootPath),
    RecursiveIteratorIterator::LEAVES_ONLY
);

foreach ($files as $name => $file)
{
    // Skip directories (they would be added automatically)
    if (!$file->isDir())
    {
        // Get real and relative path for current file
        $filePath = $file->getRealPath();
        $relativePath = substr($filePath, strlen($rootPath) + 1);

        // Add current file to archive
        $zip->addFile($filePath, $relativePath);
    }
}

// Zip archive will be created only after closing object
$zip->close();
echo $hash.".zip";"""
    return php_zip_code

#
def file_to_b64(path):
    code="""
$file='"""+path+"""';
$fp=fopen($file, "rb");
$binary=fread($fp,filesize($file));
echo base64_encode($binary);"""
    return code

#
def DIRECTORY_SEPARATOR():
    code="echo DIRECTORY_SEPARATOR;"
    return code

#
def rm(t, path):
    if t == "-f":
        code = """
$filename = '""" + path + """';
if (unlink($filename)){
    echo 'The file "'.$filename.'" was deleted successfully!';
} else {
    echo 'There was an error deleting the file "'.$filename.'"';
}"""
    elif t == "-d":
        code = """
function deleteDirectory($dir) {
    if (!file_exists($dir)) {
        return true;
    }
    if (!is_dir($dir)) {
        return unlink($dir);
    }
    foreach (scandir($dir) as $item) {
        if ($item == '.' || $item == '..') {
            continue;
        }
        if (!deleteDirectory($dir . DIRECTORY_SEPARATOR . $item)) {
            return false;
        }
    }
    if (rmdir($dir)){
        echo 'The Directory "'.$dir.'" was deleted successfully!';
    }else{
        echo 'There was an error deleting the Directory "'.$dir.'"';
    }
}
deleteDirectory('""" + path + """');
"""
    else:
        raise ValueError("Invalid type option for rm function")

    return code

#
def chmod(permissions,path):
    code="""
    if (chmod('"""+path+"""', """+permissions+""")) {
    echo "Permissions changed successfully for the file.";
    } else {
    echo "Failed to change permissions for the file.";
    }"""
    return code

#
def php_info():
    code="""
$data = array(
    'OS' => php_uname(),
    'Your IP' => $_SERVER['REMOTE_ADDR'],
    'HTTP_HOST' => $_SERVER['HTTP_HOST'],
    'Request Method' => $_SERVER['REQUEST_METHOD'],
    'Server Admin' => $_SERVER['SERVER_ADMIN'],
    'Server Port' => htmlentities($_SERVER['SERVER_PORT'], ENT_QUOTES, 'UTF-8'),
    'Server IP' => gethostbyname($_SERVER["HTTP_HOST"]),
    'PHP Self' => $_SERVER['PHP_SELF'],
    'Gateway Interface' => $_SERVER['GATEWAY_INTERFACE'],
    'Server Address' => $_SERVER['SERVER_ADDR'],
    'Server Name' => $_SERVER['SERVER_NAME'],
    'Server Protocol' => $_SERVER['SERVER_PROTOCOL'],
    'Request Time' => date('Y-m-d H:i:s', $_SERVER['REQUEST_TIME']),
    'Query String' => $_SERVER['QUERY_STRING'],
    'HTTP Accept' => $_SERVER['HTTP_ACCEPT'],
    'HTTP Accept Charset' => $_SERVER['HTTP_ACCEPT_CHARSET'],
    'HTTP Referer' => $_SERVER['HTTP_REFERER'],
    'HTTPS' => isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on' ? 'Enabled' : 'Disabled',
    'Remote Host' => isset($_SERVER['REMOTE_HOST']) ? $_SERVER['REMOTE_HOST'] : 'Unknown',
    'Remote Port' => $_SERVER['REMOTE_PORT'],
    'Script Filename' => $_SERVER['SCRIPT_FILENAME'],
    'Server Signature' => $_SERVER['SERVER_SIGNATURE'],
    'Path Translated' => $_SERVER['PATH_TRANSLATED'],
    'Script Name' => $_SERVER['SCRIPT_NAME'],
    'Script URI' => $_SERVER['SCRIPT_URI'],
    'Server Software' => getenv("SERVER_SOFTWARE"),
    'PHP Version' => phpversion(),
    'Zend Version' => htmlentities(zend_version(), ENT_QUOTES, 'UTF-8'),
    'Oracle' => function_exists('ocilogon') ? 'ON' : 'OFF',
    'MySQL' => function_exists('mysql_connect') ? 'ON' : 'OFF',
    'MSSQL' => function_exists('mssql_connect') ? 'ON' : 'OFF',
    'PostgreSQL' => function_exists('pg_connect') ? 'ON' : 'OFF',
    'Disabled Functions' => $r = ini_get('disable_functions') ? $r : 'None',
    'Directory Separator' => DIRECTORY_SEPARATOR,
    'Current Date and Time' => date('Y-m-d H:i:s')
);

$maxKeyLength = max(array_map('strlen', array_keys($data)));

foreach ($data as $key => $value) {
    printf("%-{$maxKeyLength}s : %s\n", $key, $value);
}"""
    return code
#}END.
