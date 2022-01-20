import React, { Component, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Button, Grid, Typography, TextField, FormControl, Radio, RadioGroup, FormControlLabel, FormHelperText, Collapse } from "@material-ui/core";
import Alert from '@material-ui/lab';

const CreateRoomPage = ({votesToSkip = 2, guestCanPause = false, update = false, roomCode = null, updateCallBack = () => {}}) => {
  
  const history = useNavigate();
  //sets the dafault state for votes to skip and guest can pause
  const [roomData, setRoomData] = useState({
    guestCanPause: guestCanPause,
    votesToSkip: votesToSkip,
    errorMsg: "",
    successMsg: ""
  });

  //method that changes the votes to skip to the value entered
  const handleVotesChange = (e) => {
    setRoomData({
      ...roomData,
      votesToSkip: e.target.value,
    });
  };

  //toggles the status of guest can pause whenever the button is clicked
  const handleGuestCanPauseChange = (e) => {
    setRoomData({
      ...roomData,
      guestCanPause: e.target.value === "true" ? true : false,
    });
  };

  const handleRoomButtonPressed = (e) => {
    const requestOptions = {
      method: "POST", //signals that were sending a post request
      headers: { "Content-Type": "application/json" }, //tells us what type of content we are sending
      body: JSON.stringify({
        //allows us to take a js object that will be converted into a json string that we can send
        votes_to_skip: roomData.votesToSkip,
        guest_can_pause: roomData.guestCanPause,
      }),
    };
    fetch("/api/create-room", requestOptions)
      .then(
        (response) => response.json() //this says send the payload to the url under api/create-room then once we get a response do something with it
      )
      .then((data) => history("/room/" + data.code)); 
  };

  const handleUpdateButtonPressed = () => {
    const requestOptions = {
      method: "PATCH", //signals that were sending a post request
      headers: { "Content-Type": "application/json" }, //tells us what type of content we are sending
      body: JSON.stringify({
        //allows us to take a js object that will be converted into a json string that we can send
        votes_to_skip: roomData.votesToSkip,
        guest_can_pause: roomData.guestCanPause,
        code: roomCode
      }),
    };
    fetch("/api/update-room", requestOptions)
      .then(
        (response) => {
          if (response.ok) {
            setRoomData({
              ...roomData,
              successMsg: "Successfully updated room"
            });
          } else {
            setRoomData({
              ...roomData,
              errorMsg: "Error updating room"
            });
          }
          updateCallBack();
        }
      )
  }


  const renderCreateButtons = () => {
    return <Grid container spacing={1}>
      <Grid item xs={12} align="center">
        <Button
          color="primary"
          variant="contained"
          onClick={handleRoomButtonPressed}
        >
          Create Room
        </Button>
      </Grid>
      <Grid item xs={12} align="center">
        <Button color="secondary" variant="contained" to="/" component={Link}>
          Back
        </Button>
      </Grid>
    </Grid>
  }

  const renderUpdateButtons = () => {
    return <Grid item xs={12} align="center">
        <Button
          color="primary"
          variant="contained"
          onClick={handleUpdateButtonPressed}
        >
          Update Room
        </Button>
      </Grid>
  }

  /*
    This render function uses HTML to create the page then changes the state based on the values entered then sends that state to the handleRoomButtonPressed function which stores it in the database
    */
   const title = update ? "Update Room" : "Create Room";
  return (
    <Grid container spacing={1}>
      <Grid item xs={12} align="center">
        <Collapse in={roomData.errorMsg != "" || roomData.successMsg != ""}>
          {roomData.successMsg}
        </Collapse>
      </Grid>
      <Grid item xs={12} align="center">
        <Typography component="h4" variant="h4">
          {title}
        </Typography>
      </Grid>
      <Grid item xs={12} align="center">
        <FormControl component="fieldset">
          <FormHelperText>
            <div align="center">Guest Control of Playback State</div>
          </FormHelperText>
          <RadioGroup
            row
            defaultValue={guestCanPause.toString()}
            onChange={handleGuestCanPauseChange}
          >
            <FormControlLabel
              value="true"
              control={<Radio color="primary" />}
              label="Play/Pause"
              labelPlacement="bottom"
            />
            <FormControlLabel
              value="false"
              control={<Radio color="secondary" />}
              label="No Control"
              labelPlacement="bottom"
            />
          </RadioGroup>
        </FormControl>
      </Grid>
      <Grid item xs={12} align="center">
        <FormControl>
          <TextField
            required="true"
            type="number"
            onChange={handleVotesChange}
            defaultValue={roomData.votesToSkip}
            inputProps={{
              min: 1,
              style: { textAlign: "center" },
            }}
          />
          <FormHelperText>
            <div align="center">Votes Required to Skip Song</div>
          </FormHelperText>
        </FormControl>
      </Grid>
      {update ? renderUpdateButtons() : renderCreateButtons()}
    </Grid>
  );
};
export default CreateRoomPage;
