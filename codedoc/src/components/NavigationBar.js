import React from 'react';
import { Nav, Navbar, Form, FormControl } from 'react-bootstrap';
import styled from 'styled-components';

const Styles = styled.div`
  .navbar { background-color: #222; }
  a, .navbar-nav, .navbar-light .nav-link {
    transition: all ease 0.2s;
    color: #0f62fe;
    &:hover { color: #4a89ff; }
  }
  .navbar-brand {
    font-size: 1.4em;
    transition: all ease 0.2s;
    color: #0f62fe;
    &:hover { color: #4a89ff; }
  }
  .form-center {
    position: absolute !important;
    left: 25%;
    right: 25%;
  }
`;

export const NavigationBar = () => (
  <Styles>
    <Navbar bg="light" expand="lg">
      <Navbar.Brand href="/">CODEDOC</Navbar.Brand>
      <Navbar.Toggle aria-controls="basic-navbar-nav"/>
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="ml-auto">
          <Nav.Item><Nav.Link href="/">PROFILE</Nav.Link></Nav.Item> 
          <Nav.Item><Nav.Link href="/about">CALENDAR</Nav.Link></Nav.Item>
        </Nav>
      </Navbar.Collapse>
    </Navbar>
  </Styles>
)
