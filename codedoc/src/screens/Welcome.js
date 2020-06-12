import React, { useState } from 'react'
import { Symptoms, Medication } from '../components'
export const Welcome = ({ name = 'John' }) => {      
  const symptoms = [
    { label: 'Headache', value: 'Headache' },
    { label: 'Sore Throat', value: 'Sore Throat' },
    { label: 'Fever', value: 'Fever' },
    { label: 'Coughing', value: 'Coughing' },
    { label: 'Rashes', value: 'Rashes' }
  ]

  const medication = [
    { label: 'Amlodipine', value: 'Amlodipine' },
    { label: 'Amoxicillin', value: 'Amoxicillin' },
    { label: 'Penicillin', value: 'Penicillin' },
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