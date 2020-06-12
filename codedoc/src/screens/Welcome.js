import React, { useState } from 'react'
import { AppBar, Chip, Toolbar, IconButton, Button, Typography, Container } from '@material-ui/core'
// import { ToggleButton } from '@material-ui/lab'
import { AccountCircle } from '@material-ui/icons'
export const Welcome = ({ name = 'Marcus' }) => {
  const symptoms = [
    { label: 'headache', value: 'headache' },
    { label: 'fatigue', value: 'fatigue' },
    { label: 'stomachache', value: 'stomachache' },
    { label: 'nausea', value: 'nausea' },
    { label: 'bloating', value: 'bloating' }
  ]

  const [symptomsState, setSymptomsState] = useState(['fatigue'])

  return (
    <div>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6">
            CodeDoc
          </Typography>
          <div>
            <IconButton
              aria-label="account of current user"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              color="inherit"
            >
              <AccountCircle />
            </IconButton>
          </div>
        </Toolbar>
      </AppBar>
      <Container>
        <Typography variant='h2'>Welcome Back, {name}!</Typography>
        {
          symptoms.map(symptom => {
            console.log('sym', symptom, symptomsState.includes(symptom.value))
            return (
            <ToggleButton
              value={symptom.value}
              selected={symptomsState.includes(symptom.value)}
              onClick={() => {
                let currentState = symptomsState
                if (currentState.includes(symptom.value)) {
                  let id = currentState.indexOf(symptom.value)
                  currentState.splice(id, 1)
                } else {
                  currentState.push(symptom.value)
                }
                setSymptomsState(currentState)
              }}
            >
              {symptom.label}
            </ToggleButton>
          )})
        }

      </Container>
    </div>
  )
}