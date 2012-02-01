

'--------------------8<----------------------
strComputer = "."   ' use "." for local computer

Const HKLM = &H80000002

On Error Resume Next
Set objWMIService = GetObject("winmgmts:" _
         & "{impersonationLevel=impersonate}!\\" & strComputer & "\root\cimv2")

Set colSettings = objWMIService.ExecQuery _
         ("Select * from Win32_OperatingSystem")

' Caption value for different OS:
' Microsoft Windows 2000 Professional
' Microsoft Windows XP Professional
' Microsoft(R) Windows(R) Server 2003, ..... Edition
For Each objOperatingSystem in colSettings
     strOSCaption = LCase(objOperatingSystem.Caption)
     Select Case True
      Case InStr(strOSCaption, "windows 2000") > 0
        strOS = "Windows 2000"
      Case InStr(strOSCaption, "windows xp") > 0
        strOS = "Windows XP"
      Case InStr(strOSCaption, "windows(r) server 2003") > 0
        strOS = "Windows Server 2003"
     End Select
Next

strRegBaseUpdate = "SOFTWARE\Microsoft\Updates\" & strOS

Set objReg = GetObject("WinMgmts:{impersonationLevel=impersonate}!//" _
                     & strComputer & "/root/default:StdRegProv")

Set colItems = objWMIService.ExecQuery _
         ("Select * from Win32_QuickFixEngineering",,48)

For Each objItem in colItems
     If objItem.HotFixID <> "File 1" Then
       Wscript.Echo "Description: " & objItem.Description
       Wscript.Echo "HotFixID: " & objItem.HotFixID
       Wscript.Echo "InstalledBy: " & objItem.InstalledBy
       strInstallDate = Null  ' init value
       If objItem.ServicePackInEffect <> "" Then
         strRegKey = strRegBaseUpdate & "\" & objItem.ServicePackInEffect _
                           & "\" & objItem.HotFixID
         objReg.GetStringValue HKLM, strRegKey, _
                      "InstalledDate", strInstallDate
       End If

       If IsNull(strInstallDate) Then
         strInstallDate = "(none found)"
       End If
       Wscript.Echo "InstallDate: " & strInstallDate
       Wscript.Echo   ' blank line
     End If
Next
'--------------------8<----------------------


