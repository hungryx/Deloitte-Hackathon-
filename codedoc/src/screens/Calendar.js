import React, { useState } from 'react'
import { StructuredListWrapper, StructuredListHead, StructuredListRow, StructuredListCell, StructuredListBody } from 'carbon-components-react'
import CalendarComponent from 'react-calendar'
import 'react-calendar/dist/Calendar.css';
export const Calendar = ({ name = 'Marcus' }) => {
  const [day, setDay] = useState(new Date())
  const symptoms = [
    { symptom: 'Fatigue', occurences: 13 },
    { symptom: 'Headaches', occurences: 8 },
    { symptom: 'Stomachaches', occurences: 6 }
  ]

  return (
    <div style={{
      padding: 40,
      display: 'flex'
    }}>
      <div>
        <CalendarComponent onChange={setDay} value={day} />
      </div>
      <div style={{
        paddingLeft: 48
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
            {symptoms.map((symptom, index) => (
              <StructuredListRow>
              <StructuredListCell noWrap><b>{index + 1}</b></StructuredListCell>
              <StructuredListCell>{symptom.symptom}</StructuredListCell>
              <StructuredListCell>{symptom.occurences}</StructuredListCell>
            </StructuredListRow>
            ))}
          </StructuredListBody>
        </StructuredListWrapper>
      </div>
    </div>
  )
}