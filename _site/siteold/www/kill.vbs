' folder to start search in...
path = "c:\temp"

' delete files older than 7 days...
killdate = date() - 7

arFiles = Array()
set fso = createobject("scripting.filesystemobject")

' Don't do the delete while you still are looping through a
' file collection returned from the File System Object (FSO).
' The collection may get mixed up.
' Create an array of the file objects to avoid this.
'
SelectFiles path, killdate, arFiles, true

nDeleted = 0
for n = 0 to ubound(arFiles)
  '=================================================
  ' Files deleted via FSO methods do *NOT* go to the recycle bin!!!
  '=================================================
  on error resume next 'in case of 'in use' files...
  arFiles(n).delete true
  if err.number <> 0 then
    wscript.echo "Unable to delete: " & arFiles(n).path
  else
    nDeleted = nDeleted + 1
  end if
  on error goto 0
next

msgbox nDeleted & " of " & ubound(arFiles)+1 _
  & " eligible files were deleted"


sub SelectFiles(sPath,vKillDate,arFilesToKill,bIncludeSubFolders)
  on error resume next
  'select files to delete and add to array...
  '
  set folder = fso.getfolder(sPath)
  set files = folder.files

  for each file in files
    ' uses error trapping around access to the
    ' Date property just to be safe
    '
    dtlastmodified = null
    on error resume Next
    dtlastmodified = file.datelastmodified
    on error goto 0
    if not isnull(dtlastmodified) Then
      if dtlastmodified < vKillDate then
        count = ubound(arFilesToKill) + 1
        redim preserve arFilesToKill(count)
        set arFilesToKill(count) = file
      end if
    end if
  next

  if bIncludeSubFolders then
    for each fldr in folder.subfolders
      SelectFiles fldr.path,vKillDate,arFilesToKill,true
    next
  end if
end sub


