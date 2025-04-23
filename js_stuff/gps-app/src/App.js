"use client"
import './App.css';
import {useEffect, useState} from 'react';
import Box from '@mui/material/Box';
import * as React from 'react';
import Button from '@mui/material/Button';
import { GoogleMap, LoadScript, Marker } from '@react-google-maps/api';
//mui stuff
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';



function App() {
  const reportUrl = process.env.REACT_APP_REPORT_URL
  const emailUrl = process.env.REACT_APP_EMAIL_URL
  const uploadUrl = process.env.REACT_APP_UPLOAD_URL
  const mapsApi = process.env.REACT_APP_GOOGLE_MAPS_API_KEY

  const [userStatus, setUserStatus] = useState({
    account_id: "2",
    latitude: "Nan",
    longitude: "Nan"
  })

  const changeAccountId = (event) => {
    setUserStatus(prevState => ({
      ...prevState,  
      account_id: event.target.value
    }));
  };

  

  const [address, setAddress] = useState("Nan")

  const [addressList, setAddressList] = useState([])


  //use effect to return the address given a change in lat and long
  function commitPothole() {
    if(userStatus.latitude !== "Nan"){
      console.log("coordinates: ", userStatus)
      fetch(uploadUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(userStatus)
      })
      .then(response => response.json())
      .then(data => {
        console.log("Address: ", data)
        setAddress(data); // sets address for frontend to read
      })
      .catch(error => {
        // Handle any errors
        console.error('Error:', error);
      });
    }
  }

  
  function getAddresses(user_id) {
    fetch(reportUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({account_id: user_id})
    })
    .then(response => response.json())
    .then(data => {
      setAddressList(data); // sets address for frontend to read
      console.log("addressList: ", addressList)
    })
    .catch(error => {
      // Handle any errors
      console.error('Error:', error);
    });
  }

  function getPosition(position) {
    setUserStatus(prevCoordinates => ({
      ...prevCoordinates,
      latitude: position.coords.latitude, 
      longitude: position.coords.longitude
    }));
  }

  function getLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(getPosition);
    } else {
      console.log("Geolocation is not supported by this browser.");
    }
  }

  function sendEmail(user_id){
    fetch(emailUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({account_id: user_id})
    })
  }


  const mapContainerStyle = {
    width: '100%',
    height: '400px'
  };


  function returnMap() {
    return (
      <LoadScript googleMapsApiKey={mapsApi}>
        <GoogleMap
          mapContainerStyle={mapContainerStyle}
          center={{
            lat: userStatus.latitude,
            lng: userStatus.longitude
          }}
          zoom={17}
          options={{
            draggable: false, // Prevent moving the map
            zoomControl: false, // Disable zoom buttons
            scrollwheel: false, // Prevent zooming with scroll wheel
            disableDoubleClickZoom: true, // Prevent zooming on double-click
          }}
        >
          {userStatus.latitude !== "Nan" && (
            <Marker
              position={{
                lat: parseFloat(userStatus.latitude),
                lng: parseFloat(userStatus.longitude),
              }}
              draggable={true} // Allows only the marker to be moved
              onDragEnd={(event) => {
                setUserStatus({
                  ...userStatus,
                  latitude: event.latLng.lat(),
                  longitude: event.latLng.lng(),
                });
              }}
            />
          )}
        </GoogleMap>
      </LoadScript>
    );
  }

  return (
    <Box component="section" sx={{ p: 2, border: '2px dashed grey' }}>

      <Button onClick={getLocation} variant="contained">POTHOLE</Button>
      <Button onClick={() => getAddresses(userStatus.account_id)} variant="contained">ADDRESSES</Button>
      <Button onClick={() => sendEmail(userStatus.account_id)} variant="contained"> Send Email: UserId: {userStatus.account_id}</Button>
      <div>
        <text>Account Id:</text>
        <input type="text" value={userStatus.account_id} onChange={changeAccountId} />
      </div>
      <button>{userStatus.account_id}</button>
      <div>
        <p> Latitude: {userStatus.latitude} </p>
        <p> Longitude: {userStatus.longitude} </p>
        <p> Address: {address}</p>
        {returnMap()}
        <List
          sx={{
            width: '100%',
            bgcolor: 'background.paper',
            position: 'relative',
            overflow: 'auto',
            maxHeight: 300,
            '& ul': { padding: 0 },
          }}
          subheader={<li />}
        >
          <ListItem>
            {addressList.map((item, index) => (
              <li key = {index}>{item}</li>
            ))}
          </ListItem>
        </List>
      </div>
      <Button onClick={commitPothole} variant="contained"> Commit to Database</Button>
    </Box>
      
     
      
    
  );
}

export default App;
