import React, { useState, useEffect } from 'react';
import './App.css';
import PatientSlices from './component/PatientSlices/PatientSlices';

const fetchPatients = async() => {
  const res = await fetch('http://localhost:5000/patients');
  if (!res.ok) throw new Error(`Error on: ${res.status}`);
  return await res.json();
}

function App() {
  const [data, setData] = useState({});
  const [patients, setPatients] = useState([]);
  const [answer, setAnswer] = useState({});
  const [patientNum, setPatientNum] = useState(0);
  const [saveMsg, setSaveMsg] = useState('');

  useEffect(() => {
    fetchPatients().then(
      result => {
        setData(result);
        setPatients(Object.keys(result).sort());
        setAnswer(Object.keys(result).reduce((ans, key) => {
          ans[key] = {};
          return ans;
        }, {}));
      },
      error => console.log('Error while loading patients')
    );
  }, []);

  const getPrevPatient = () => {
    if (patientNum > 0) setPatientNum(patientNum - 1);
  }
  const getNextPatient = () => {
    if (patientNum < Object.keys(patients).length - 1) setPatientNum(patientNum + 1);
  }

  const selectSlice = (scanDate, slice) => {
    setAnswer(answer => {
      return {
        ...answer,
        [patients[patientNum]]: {
          ...answer[patients[patientNum]],
          [scanDate]: slice 
        }
      }
    });
  }

  const isAnswered = () => {
    const patient = patients[patientNum];
    if (answer[patient]) return Object.keys(answer[patient]).length === Object.keys(data[patient]).length;
    return false;
  }

  const countScans = (dataAll) => {
    return Object.keys(dataAll)
      .reduce((sum, key) => sum + Object.keys(dataAll[key]).length, 0);
  }

  const saveAnswer = () => {
    if (countScans(data) !== countScans(answer)) setSaveMsg('未回答の検査があります．');
    else fetch('http://localhost:5000/answer', {method: 'PUT', body: JSON.stringify(answer)})
      .then(res => res.json())
      .then(result => setSaveMsg(result));
  }

  return (
    <div className="App">
      <h1 style={{color: isAnswered() ? "green" : "red"}}>
        Patient ({patientNum + 1}/{patients.length}): {patients[patientNum]}
      </h1>
      <h4>{ saveMsg }</h4>
      <button onClick={saveAnswer}>提出</button><br></br>
      <button onClick={getPrevPatient}>前の患者</button>
      <button onClick={getNextPatient}>次の患者</button>
      <br></br>
      <PatientSlices
        patient={patients[patientNum]}
        slices={data[patients[patientNum]]}
        answer={answer[patients[patientNum]]}
        selectSlice={selectSlice}
      />
    </div>
  );
}

export default App;
