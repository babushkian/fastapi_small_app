
import React, { useState, useContext, useEffect, useRef } from "react";


import {
    Alert,
    Box,
    Button,
    FormControl,
    IconButton,
    InputAdornment,
    InputLabel,
    OutlinedInput,
    Snackbar,
    Stack,
    TextField,
    Typography,
    List,
    ListItemText,
    ListItem,
    Divider,
    ListItemButton,
} from "@mui/material";

import axios from "axios";

import { Visibility, VisibilityOff, Edit, Delete } from "@mui/icons-material";

type studentType = {id:number, name:string}

function App() {
  const [list, setList] = useState<studentType[]>([])
  const [newStudent, setNewStudent] = useState("")

   const loader = async () => {
    const result = await axios.get('http://127.0.0.1:8000/students/')
    if (result) {
      console.log(result.data)
    setList(result.data) 
    }
  }

  const deleteStudent = (studentId: number) => {
    
    const newList = list.filter((item)=> item.id != studentId)
    setList(newList)
  }

  const addNewStudent = () => {
    const maxId = Math.max(...list.map(item => item.id), 0)
    
    console.log("--------------")
    console.log(maxId)
    setList(old =>[...old, {id:maxId+1, name: newStudent}])
    setNewStudent("")
  }

  useEffect(() => console.log(list), [addNewStudent])
  


  return (
    <>
      <div className="card">
          <Typography variant="h5" align="center" gutterBottom>
              пример добавление и удаления записей
          </Typography>

        <Box sx={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
          <Button variant="contained" onClick={loader}> Загрузить данные</Button>
          <ul>
          {list.map((item)=><li key={item.id}>{item.name} <Button variant="outlined" onClick={() => deleteStudent(item.id)} startIcon={<Delete/>} /></li>)}
          </ul>
    
          <Box>
            <TextField
              name="new student"
              size="small"
              value={newStudent}
              onChange={(e) => setNewStudent(e.target.value)}
              label="Новый Студент"
              sx={{ m: 1 }}
              variant="outlined"
              helperText="Поле некрооектно заполнено"
            />
            <Button variant="contained" startIcon={<Edit/>} onClick={addNewStudent}>добавить</Button>
          </Box>
        </Box>
      </div>
    </>
  )
}

export default App
