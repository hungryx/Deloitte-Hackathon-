import React, { useState } from 'react'
import { FormGroup, TextArea } from 'carbon-components-react'
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
      <div style={{ marginTop: 24 }}>
        <h4>Additional Notes</h4>
        <FormGroup>
          <TextArea
            style={{
              border: '2px solid #FFC222'
            }}
            placeholder="Today I felt..."
          />
        </FormGroup>
      </div>
    </div>
  )
}