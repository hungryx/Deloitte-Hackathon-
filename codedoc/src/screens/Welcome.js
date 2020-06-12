import React from 'react'
import { Button, Typography, Container } from '@material-ui/core'

export const Welcome = ({ name='Marcus' }) => {
    return (
        <Container fixed>
            <Typography variant='h2'>Welcome Back, {name}!</Typography>
        </Container>
    )
}