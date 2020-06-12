import React, { useState } from 'react'
import { StructuredListWrapper, StructuredListHead, StructuredListRow, StructuredListCell, StructuredListBody, ComposedModal, ModalHeader, ModalBody } from 'carbon-components-react'
import CalendarComponent from 'react-calendar'
import './Calendar.css';
export const Calendar = ({ name = 'Marcus' }) => {
  const [day, setDay] = useState(new Date())
  const [modalOpen, setModalOpen] = useState(false)
  const symptoms1 = [
    { symptom: 'Fatigue', occurences: 13 },
    { symptom: 'Headaches', occurences: 8 },
    { symptom: 'Stomachaches', occurences: 6 }
  ]
  
  const symptoms2 = [
    { symptom: 'Headaches', occurences: 9 },
    { symptom: 'Fatigue', occurences: 4 },
    { symptom: 'Stomachaches', occurences: 2 }
  ]
  
  const symptoms3 = [
    { symptom: 'Fatigue', occurences: 14 },
    { symptom: 'Headaches', occurences: 4 },
    { symptom: 'Stomachaches', occurences: 3 }
  ]
  
  const symptoms = [ symptoms1, symptoms2, symptoms3 ]
  const [dataSet, setDataSet] = useState(symptoms[0])

  return (
    <div style={{
      padding: 40,
    }}>
      <center>
        <CalendarComponent onChange={(date) => {
          let max = 2
          let min = 0
          setModalOpen(true)
          setDataSet(symptoms[Math.floor(Math.random() * (max - min + 1)) + min])
          setDay(date)
        }} value={day} />
      </center>
      <div style={{
        marginTop: 48
      }}>
        <h4>Your most frequent symptoms</h4>
        <StructuredListWrapper>
          <StructuredListHead>
            <StructuredListRow head>
              <StructuredListCell head />
              <StructuredListCell head>Symptom</StructuredListCell>
              <StructuredListCell head>Occurences</StructuredListCell>
            </StructuredListRow>
          </StructuredListHead>
          <StructuredListBody>
            {symptoms1.map((symptom, index) => (
              <StructuredListRow>
              <StructuredListCell noWrap><b>{index + 1}</b></StructuredListCell>
              <StructuredListCell>{symptom.symptom}</StructuredListCell>
              <StructuredListCell>{symptom.occurences}</StructuredListCell>
            </StructuredListRow>
            ))}
          </StructuredListBody>
        </StructuredListWrapper>
        <ComposedModal
          size='sm'
          open={modalOpen}
          onClose={() => setModalOpen(false)}
          modalHeading='heading'
          modalLabel='label'
          >
          <ModalHeader title={'Your stats for ' + day.toLocaleDateString('en-AU')} />
          <ModalBody>
          <StructuredListWrapper>
          <StructuredListHead>
            <StructuredListRow head>
              <StructuredListCell head>Symptom</StructuredListCell>
              <StructuredListCell head>Occurences</StructuredListCell>
            </StructuredListRow>
          </StructuredListHead>
          <StructuredListBody>
            {dataSet.map((symptom, index) => (
              <StructuredListRow>
              <StructuredListCell>{symptom.symptom}</StructuredListCell>
              <StructuredListCell>{symptom.occurences}</StructuredListCell>
            </StructuredListRow>
            ))}
          </StructuredListBody>
        </StructuredListWrapper>
          </ModalBody>
          </ComposedModal>
      </div>
    </div>
  )
}