Const OpenAsASCII = 0  ' Opens the file as ASCII (TristateFalse)
Const OverwriteIfExist = -1

' file where result is to be saved
sFile = "c:\apps.txt"

sComputer =  "."   ' use . for local computer

Set oFSO = CreateObject("Scripting.FileSystemObject")
Set fFile = oFSO.CreateTextFile(sFile, _
                    OverwriteIfExist, OpenAsASCII)

fFile.Write InstalledApplications(sComputer)
fFile.Close


Function InstalledApplications(node)
 Const HKLM = &H80000002 'HKEY_LOCAL_MACHINE
 Set oRegistry = _
  GetObject("winmgmts:{impersonationLevel=impersonate}!\\" _
  & node & "/root/default:StdRegProv")
 sBaseKey = _
  "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\"
 iRC = oRegistry.EnumKey(HKLM, sBaseKey, arSubKeys)
 For Each sKey In arSubKeys
  iRC = oRegistry.GetStringValue( _
   HKLM, sBaseKey & sKey, "DisplayName", sValue)
  If iRC <> 0 Then
   oRegistry.GetStringValue _
    HKLM, sBaseKey & sKey, "QuietDisplayName", sValue
  End If
  If sValue <> "" Then
   InstalledApplications = _
    InstalledApplications & sValue & vbCrLf
  End If
 Next
End Function


