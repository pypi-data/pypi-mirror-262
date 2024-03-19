Get-ChildItem examples -Filter *.qml -Recurse | Foreach-Object {
    Write-Output $_.FullName
    pyside6-qmllint.exe $_.FullName -I stubs
}
Get-ChildItem QuickGraphLib -Filter *.qml -Recurse | Foreach-Object {
    Write-Output $_.FullName
    pyside6-qmllint.exe $_.FullName -I stubs
}