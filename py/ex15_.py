Dim con As ADODB.Connection
Dim rs As ADODB.Recordset

Private Sub cmdback_Click()
    Unload Me
End Sub

Private Sub cmdsave_Click()
    ' Check for blank records using IsNull or empty string comparison
    If Trim(txtreg.Text) = "" Or Trim(txtpname.Text) = "" Or Trim(txtaddress.Text) = "" Or _
       Trim(txtphno.Text) = "" Or Trim(txtage.Text) = "" Or Trim(txtsex.Text) = "" Or _
       Trim(txtdiagnosis.Text) = "" Or Trim(txtptype.Text) = "" Or Trim(txtguardian.Text) = "" Or _
       Trim(txtrelation.Text) = "" Or Trim(txtroom.Text) = "" Or Trim(txtadmitdate.Text) = "" Or _
       Trim(txtadmittime.Text) = "" Or Trim(txtreferdr.Text) = "" Or Trim(txtcondr.Text) = "" Or _
       Trim(txtcasehistory.Text) = "" Then
        MsgBox "Blank records cannot be saved", vbExclamation, "Validation Error"
    Else
        On Error GoTo ErrorHandler

        Set rs = New ADODB.Recordset
        
        ' Use parameterized queries to prevent SQL injection and handle data types correctly
        Dim strSQLCheck As String
        strSQLCheck = "SELECT Regd_no FROM Admission WHERE Regd_no = ?"
        
        With con.CreateCommand
            .CommandText = strSQLCheck
            .Parameters.Append .CreateParameter("RegdNoParam", adVarChar, adParamInput, 255, Trim(txtreg.Text)) ' Adjust size as needed
            Set rs = .Execute
        End With

        If Not rs.EOF Then
            MsgBox "Duplicate ID, please change it.", vbExclamation, "Duplicate Entry"
            txtreg.SetFocus
        Else
            Dim strSQLInsert As String
            strSQLInsert = "INSERT INTO Admission VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            
            With con.CreateCommand
                .CommandText = strSQLInsert
                ' Append parameters for each field, specifying data type and size
                .Parameters.Append .CreateParameter("RegdNo", adVarChar, adParamInput, 255, Trim(txtreg.Text))
                .Parameters.Append .CreateParameter("PName", adVarChar, adParamInput, 255, Trim(txtpname.Text))
                .Parameters.Append .CreateParameter("Address", adVarChar, adParamInput, 255, Trim(txtaddress.Text))
                .Parameters.Append .CreateParameter("PhNo", adVarChar, adParamInput, 20, Trim(txtphno.Text)) ' Assuming phone number as string
                .Parameters.Append .CreateParameter("Age", adInteger, adParamInput, , CInt(Trim(txtage.Text))) ' Assuming age as integer
                .Parameters.Append .CreateParameter("Sex", adVarChar, adParamInput, 10, Trim(txtsex.Text))
                .Parameters.Append .CreateParameter("Diagnosis", adVarChar, adParamInput, 255, Trim(txtdiagnosis.Text))
                .Parameters.Append .CreateParameter("PType", adVarChar, adParamInput, 50, Trim(txtptype.Text))
                .Parameters.Append .CreateParameter("Guardian", adVarChar, adParamInput, 255, Trim(txtguardian.Text))
                .Parameters.Append .CreateParameter("Relation", adVarChar, adParamInput, 50, Trim(txtrelation.Text))
                .Parameters.Append .CreateParameter("Room", adVarChar, adParamInput, 50, Trim(txtroom.Text))
                .Parameters.Append .CreateParameter("AdmitDate", adDate, adParamInput, , CDate(Trim(txtadmitdate.Text)))
                .Parameters.Append .CreateParameter("AdmitTime", adDBTime, adParamInput, , CDate(Trim(txtadmittime.Text))) ' Or adDate if storing as part of date
                .Parameters.Append .CreateParameter("ReferDr", adVarChar, adParamInput, 255, Trim(txtreferdr.Text))
                .Parameters.Append .CreateParameter("ConDr", adVarChar, adParamInput, 255, Trim(txtcondr.Text))
                .Parameters.Append .CreateParameter("CaseHistory", adVarChar, adParamInput, 255, Trim(txtcasehistory.Text))
                
                .Execute
            End With

            MsgBox "Record Saved Successfully!", vbInformation, "Save Record"
            ' Clear textboxes after successful save
            txtreg.Text = ""
            txtpname.Text = ""
            txtaddress.Text = ""
            txtphno.Text = ""
            txtage.Text = ""
            txtsex.Text = ""
            txtdiagnosis.Text = ""
            txtptype.Text = ""
            txtguardian.Text = ""
            txtrelation.Text = ""
            txtroom.Text = ""
            txtadmitdate.Text = ""
            txtadmittime.Text = ""
            txtreferdr.Text = ""
            txtcondr.Text = ""
            txtcasehistory.Text = ""
        End If
        
        Exit Sub ' Exit subroutine after successful execution

ErrorHandler:
        MsgBox "An error occurred: " & Err.Description, vbCritical, "Error"
    End If
End Sub

Private Sub cmdview_Click()
    frmviewadm.Show
    frmviewadm.Top = 0
    frmviewadm.Left = 0
    frmviewadm.Width = 8595
    frmviewadm.Height = 7650
End Sub

Private Sub Form_Load()
    Set con = New ADODB.Connection
    ' Ensure the path to the database is correct for deployment
    con.Open "Provider=Microsoft.Jet.OLEDB.4.0;Data Source=" & App.Path & "\SANJIVANI\sanjivani.mdb;Persist Security Info=False"
End Sub

Private Sub optfemale_Click()
    txtsex.Text = "Female"
End Sub

Private Sub optmale_Click()
    txtsex.Text = "Male"
End Sub

Private Sub txtage_KeyPress(KeyAscii As Integer) ' Changed from Change to KeyPress for immediate validation
    If KeyAscii = vbKeyBack Then Exit Sub
    If Not IsNumeric(Chr(KeyAscii)) Then
        KeyAscii = 0
        MsgBox "Only numbers are accepted for Age.", vbExclamation, "Input Error"
    End If
End Sub

Private Sub txtphno_KeyPress(KeyAscii As Integer)
    If KeyAscii = vbKeyBack Then Exit Sub
    If Not IsNumeric(Chr(KeyAscii)) Then
        KeyAscii = 0
        MsgBox "Only numbers are accepted for Phone Number.", vbExclamation, "Input Error"
    End If
End Sub