#画像をsample[0-9*].jpgに置き換える
#動かすには、以下のディレクトリに画像があることが前提です。
#・$workDir(env.txtにて設定)\honmei
#・$workDir(env.txtにて設定)\giri
Add-Type -AssemblyName System.Drawing

#画像変換用関数
function convert($inputPath) {
    cd $inputPath
    
    $i = 0
    foreach($l in ls -r | where { $_.Name -match ".jpg|.bmp|.jpeg" } ){
        $target = $inputPath + $l
        $image = [System.Drawing.Image]::FromFile($target)
        #png変換
        $image.Save((pwd).Path + "\convertAfter" + $i + ".png", [System.Drawing.Imaging.ImageFormat]::png)
        $image.Dispose()
        
        #png/bmpファイルを削除
        Remove-Item $target
        $i++
    }
    
    #画像名変換
    ls | % {$i = 1} { $NewName = "replace_{0:00}.png" -f $i, $_.Name ; mv $_.Name $NewName; $i++ }
}

#プロパティの呼び出し
$workDir = powershell "..\readProp.ps1 workDir"

$currentDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$honmeiChocoDir = $workDir + "\honmei\"
$giriChocoDir = $workDir + "\giri\"


#画像変換処理（本命）
convert $honmeiChocoDir
#画像変換処理（義理）
convert $giriChocoDir


#作業ディレクトリを戻す
cd $currentDir
