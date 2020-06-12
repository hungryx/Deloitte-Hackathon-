import React, { useState } from 'react'
import { Symptoms, Medication } from '../components'
export const Welcome = ({ name = 'Marcus Lo' }) => {
  const symptoms = [
    { label: 'Headache', value: 'Headache' },
    { label: 'Fatigue', value: 'Fatigue' },
    { label: 'Stomachache', value: 'Stomachache' },
    { label: 'Nausea', value: 'Nausea' },
    { label: 'Bloating', value: 'Bloating' }
  ]

  const medication = [
    { label: 'Atorvastatin', value: 'Atorvastatin' },
    { label: 'Rosuvastatin', value: 'Rosuvastatin' },
    { label: 'Perindopril', value: 'Perindopril' },
    { label: 'Amlodipine', value: 'Amlodipine' },
    { label: 'Irbesartan', value: 'Irbesartan' }
  ]
  return (
    <div style={{
      padding: 40
    }}>
        <h2>Welcome Back, {name}!</h2>
        <Medication medication={medication} />
        <Symptoms symptoms={symptoms} />
    </div>
  )
}