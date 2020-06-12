import React, { useState } from 'react'
import { FileUploader } from 'carbon-components-react'
export const Profile = ({ name = 'John Doe' }) => {
    return (
      <div style={{
        padding: 40
      }}>
          <h2>{name}</h2>
          <br />
          <FileUploader
            accept={[
                '.jpg',
                '.png'
            ]}
            buttonKind="primary"
            buttonLabel="Add files"
            filenameStatus="edit"
            iconDescription="Clear file"
            labelDescription="only .jpg files at 500mb or less"
            labelTitle="Upload"
            />
          <br />
          <h4>PERSONAL DETAILS</h4>   
          <body>Full name: John Doe
              <br /> Age: 60
              <br /> Sex: M
              <br /> Email: john@gmail.com
              <br /> Phone: 0400 000 001</body>   
          <br />
          <h4>MEDICAL HISTORY</h4>
            <body> 2006 - current: high blood pressure 
              <br /> 2014: hernia removal surgery 
            </body>
          <br />
          <h4>CURRENT MEDICATION</h4>
            <body> 2006 - current: Amlodipine
            </body>
            <br />
          <h4>DOCTOR CONTACT DETAILS</h4>
             <h6>Dr Dohn Joe</h6>
             <body>Number: 9423 5123
                 <br /> Clinic: Sydney Medical Centre
             </body>
             <br />
             <h6>Dr Jane Koe</h6>
             <body>Number: 9447 5156
                 <br /> Clinic: Chatswood Medical Centre
             </body>
      </div>

    )
}