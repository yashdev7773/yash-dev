' ADO Object Declarations: Should be declared globally for the form
Dim con As ADODB.Connection
Dim rs As ADODB.Recordset

Private Sub cmdback_Click()
    ' Ensure the connection is closed when the form unloads
    If Not con Is Nothing Then
        If con.State = adStateOpen Then con.Close
        Set con = Nothing
    End If
    Unload Me
End Sub

Private Sub cmdsave_Click()
    On Error GoTo ErrorHandler

    ' 1. Input Validation: Check for blank fields
    If txtreg.Text = "" Or txtpname.Text = "" Or txtaddress.Text = "" Or txtphno.Text = "" Or txtage.Text = "" Or txtsex.Text = "" Or txtdiagnosis.Text = "" Or txtptype.Text = "" Or txtguardian.Text = "" Or txtrelation.Text = "" Or txtroom.Text = "" Or txtadmitdate.Text = "" Or txtadmittime.Text = "" Or txtreferdr.Text = "" Or txtcondr.Text = "" Or txtcasehistory.Text = "" Then
        MsgBox "Blank records cannot be saved. Please fill all fields.", vbExclamation
        Exit Sub
    End If

    ' --- Check for Duplicate Registration ID using Parameterized Query ---
    Dim cmdCheck As ADODB.Command
    Set cmdCheck = New ADODB.Command

    With cmdCheck
        Set .ActiveConnection = con
        .CommandText = "SELECT Regd_no FROM Admission WHERE Regd_no = ?"
        .CommandType = adCmdText
        .Parameters.Append .CreateParameter("Regd_noParam", adVarChar, adParamInput, Len(Trim(txtreg.Text)), Trim(txtreg.Text))
    End With

    Set rs = cmdCheck.Execute()

    If Not rs.EOF Then
        MsgBox "Duplicate ID, Change it.", vbCritical
        txtreg.Text = ""
        txtreg.SetFocus
    Else
        ' --- Insert Record using Parameterized Query (Safer) ---
        Dim cmdInsert As ADODB.Command
        Set cmdInsert = New ADODB.Command

        Dim sqlInsert As String
        sqlInsert = "INSERT INTO Admission (Regd_no, PName, Address, PhNo, Age, Sex, Diagnosis, PType, Guardian, Relation, Room, AdmitDate, AdmitTime, ReferDr, ConDr, CaseHistory) " & _
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

        With cmdInsert
            Set .ActiveConnection = con
            .CommandText = sqlInsert
            .CommandType = adCmdText
            
            ' Append parameters in the correct order as defined in the table schema
            .Parameters.Append .CreateParameter("@Regd_no", adVarChar, adParamInput, , Trim(txtreg.Text))
            .Parameters.Append .CreateParameter("@PName", adVarChar, adParamInput, , Trim(txtpname.Text))
            .Parameters.Append .CreateParameter("@Address", adVarChar, adParamInput, , Trim(txtaddress.Text))
            .Parameters.Append .CreateParameter("@PhNo", adVarChar, adParamInput, , Trim(txtphno.Text))
            .Parameters.Append .CreateParameter("@Age", adInteger, adParamInput, , Val(Trim(txtage.Text))) ' Assuming Age is Numeric
            .Parameters.Append .CreateParameter("@Sex", adVarChar, adParamInput, , Trim(txtsex.Text))
            .Parameters.Append .CreateParameter("@Diagnosis", adVarChar, adParamInput, , Trim(txtdiagnosis.Text))
            .Parameters.Append .CreateParameter("@PType", adVarChar, adParamInput, , Trim(txtptype.Text))
            .Parameters.Append .CreateParameter("@Guardian", adVarChar, adParamInput, , Trim(txtguardian.Text))
            .Parameters.Append .CreateParameter("@Relation", adVarChar, adParamInput, , Trim(txtrelation.Text))
            .Parameters.Append .CreateParameter("@Room", adVarChar, adParamInput, , Trim(txtroom.Text))
            .Parameters.Append .CreateParameter("@AdmitDate", adDate, adParamInput, , Trim(txtadmitdate.Text)) ' Assuming Date format is consistent
            .Parameters.Append .CreateParameter("@AdmitTime", adVarChar, adParamInput, , Trim(txtadmittime.Text))
            .Parameters.Append .CreateParameter("@ReferDr", adVarChar, adParamInput, , Trim(txtreferdr.Text))
            .Parameters.Append .CreateParameter("@ConDr", adVarChar, adParamInput, , Trim(txtcondr.Text))
            .Parameters.Append .CreateParameter("@CaseHistory", adVarChar, adParamInput, , Trim(txtcasehistory.Text))
            
            .Execute
        End With

        MsgBox "Record Saved Successfully.", vbInformation

        ' Clear fields after successful save
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
        
        ' Clean up command objects
        Set cmdInsert = Nothing
    End If

    ' Cleanup
    If Not rs Is Nothing Then Set rs = Nothing
    If Not cmdCheck Is Nothing Then Set cmdCheck = Nothing
    
    Exit Sub ' Exit to avoid executing the error handler

ErrorHandler:
    MsgBox "An error occurred: " & Err.Description & vbCrLf & "Error Number: " & Err.Number, vbCritical
End Sub

Private Sub cmdview_Click()
    ' Ensure proper handling of form visibility/loading
    ' This assumes frmviewadm exists and is an independent form
    Load frmviewadm
    frmviewadm.Show
    ' Using Move method is generally better than setting Top/Left/Width/Height separately
    frmviewadm.Move 0, 0, 8595, 7650
End Sub

Private Sub Form_Load()
    ' Centralized database connection logic
    On Error GoTo ErrorHandlerLoad
    Set con = New ADODB.Connection
    con.Open "Provider=Microsoft.Jet.OLEDB.4.0;Data Source=..\SANJIVANI\sanjivani.mdb;Persist Security Info=False"
    Exit Sub

ErrorHandlerLoad:
    MsgBox "Database connection error: " & Err.Description, vbCritical, "Connection Failed"
    ' Disable controls or unload form if connection fails
    Me.Enabled = False
End Sub

Private Sub optfemale_Click()
    txtsex.Text = "Female"
End Sub

Private Sub optmale_Click()
    txtsex.Text = "Male"
End Sub

' --- Key Validation Corrections ---

Private Sub txtage_KeyPress(KeyAscii As Integer) ' Change Change event to KeyPress for input validation
    If KeyAscii = vbKeyBack Or KeyAscii = vbKeyDelete Then Exit Sub ' Allow backspace/delete
    If Not IsNumeric(Chr(KeyAscii)) Then
        KeyAscii = 0
        ' Use a single message box for consistency
        MsgBox "Only numeric digits are accepted.", vbExclamation
    End If
End Sub

Private Sub txtphno_KeyPress(KeyAscii As Integer)
    If KeyAscii = vbKeyBack Or KeyAscii = vbKeyDelete Then Exit Sub
    If Not IsNumeric(Chr(KeyAscii)) Then
        KeyAscii = 0
        MsgBox "Only numeric digits are accepted.", vbExclamation
    End If
End Sub

' Note: For date/time fields (txtadmitdate, txtadmittime), you should implement masked input or date picker logic, 
' but for simple correction, I've left them as standard text boxes.
