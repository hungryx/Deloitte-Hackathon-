import React, { useState } from 'react'
import CalendarComponent from 'react-calendar'
import 'react-calendar/dist/Calendar.css';
export const Calendar = ({ name = 'Marcus' }) => {
  const [day, setDay] = useState(new Date())
  return (
    <div style={{
      padding: 40
    }}>
      <div>
        <CalendarComponent onChange={setDay} value={day} />
      </div>
      <div>
        
      </div>
    </div>
  )
}