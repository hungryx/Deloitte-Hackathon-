import React, { useState } from 'react'
import { Toggler } from './Components'


export const Symptoms = ({ symptoms }) => {
  return (
    <div style={{ marginTop: 24 }}>
      <h4>Did you have any of these symptoms today?</h4>
      <div style={{ marginTop: 12 }}>
        {symptoms.map(symptom => {
          return (
            <Toggler label={symptom.label} color='#CD5C5C' />
          )
        })}
      </div>
    </div>
  )
}