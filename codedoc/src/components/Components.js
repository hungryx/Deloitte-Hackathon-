import React, { useState } from 'react'
import { Button } from 'carbon-components-react'

export const Toggler = ({ label, color }) => {
    const [selected, setSelected] = useState(false)
    return (
      <Button
        kind={selected ? 'primary' : 'tertiary'}
        onClick={() => setSelected(!selected)}
        style={{ 
          margin: 8,
          borderRadius: 8,
        }}
      >
        {label}
      </Button>
    )
  }