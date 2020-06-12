import React, { useState } from 'react'
import { Toggler } from './Components'


export const Medication = ({ medication }) => {
  return (
    <div style={{ marginTop: 24 }}>
      <h4>Have you taken your daily medication?</h4>
      <div style={{ marginTop: 12 }}>
        {medication.map(med => {
          return (
            <Toggler label={med.label} />
          )
        })}
      </div>
    </div>
  )
}