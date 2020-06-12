import React, { useState } from 'react'
import { Toggler } from './Components'
import { ToastNotification } from 'carbon-components-react'


export const Medication = ({ medication }) => {
  const notifications = [
    {
      title: `You have 1 week's worth of Atorvastatin left.`,
      caption: `Don't forget to visit your pharmacy.`
    },
    {
      title: `You have 1 prescription left for Rosuvastatin.`,
      caption: `Visit your GP to renew your precsriptions.`
    },
    {
      title: `You have 1 week's worth of Perindopril left.`,
      caption: `Don't forget to visit your pharmacy.`
    }
  ]
  return (
    <div style={{ marginTop: 24 }}>
      <h4>Have you taken your daily medication?</h4>
      <div style={{
        display: 'flex',
        overflow: 'scroll'
      }}>
        {notifications.map(notif => (
          <ToastNotification
            style={{ minWidth: 300 }}
            lowContrast
            kind={'warning'}
            title={notif.title}
            caption={notif.caption}
          />
        ))}
      </div>


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