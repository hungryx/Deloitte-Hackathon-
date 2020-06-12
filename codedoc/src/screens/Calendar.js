import React, { useState } from 'react'
import CalendarComponent from 'react-calendar'
export const Calendar = ({ name = 'Marcus' }) => {
  return (
    <div style={{
      padding: 40
    }}>
        <h2>History</h2>
        <CalendarComponent
          onChange={this.onChange}
          value={this.state.date}
        />
    </div>
  )
}