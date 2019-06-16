#プロパティを読み込む
$envDir="..\..\env.txt"
$i=1
$ret=@{}

foreach ($l in Get-Content -Encoding UTF8 $envDir) {
    #空文字は対象外
    if([String]::IsNullOrEmpty($l)) {
        continue
    }
    #コメント行は対象外
    if($l.Substring(0, 1) -eq "#") {
        continue
    }
    $prop = $l -split "="
    $key = $prop[0]
    $val = $prop[1]
    
    $ret.Add($key, $val)
    
    $i++
}

return $ret[$args[0]]