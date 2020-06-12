import React, { useState } from 'react'
import { Symptoms, Medication } from '../components'
export const Welcome = ({ name = 'Marcus' }) => {
  const symptoms = [
    { label: 'headache', value: 'headache' },
    { label: 'fatigue', value: 'fatigue' },
    { label: 'stomachache', value: 'stomachache' },
    { label: 'nausea', value: 'nausea' },
    { label: 'bloating', value: 'bloating' }
  ]

  const medication = [
    { label: 'headache', value: 'headache' },
    { label: 'fatigue', value: 'fatigue' },
    { label: 'stomachache', value: 'stomachache' },
    { label: 'nausea', value: 'nausea' },
    { label: 'bloating', value: 'bloating' }
  ]
  return (
    <div style={{
      padding: 40
    }}>
        <h2>Welcome Back, {name}!</h2>
        <Symptoms symptoms={symptoms} />
        <Medication medication={medication} />
    </div>
  )
}