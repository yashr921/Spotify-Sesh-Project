import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { Grid, Button, ButtonGroup, Typography } from "@material-ui/core";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import CreateRoomPage from "./CreateRoomPage";
import MusicPlayer from "./MusicPlayer";

export const Room = (props) => {
  const initialState = {
    votesToSkip: 2,
    guestCanPause: false,
    isHost: true,
    song: {}
  };
  const [roomData, setRoomData] = useState(initialState);
  const [showSettings, setShowSettings] = useState(false);
  const [roomCode, setRoomCode] = useState(useParams().roomCode); //by default it passes a parameter called match which tells us how it matched the url we went to with the roomCode variable so it returns the roomCode value
  //the react router by default passes some props to the room component that will have information relating to how it got there
  const nav = useNavigate();
  const [call, setCall] = useState(false);
  const [spotifyAuthenticated, setSpotifyAuthenticated] = useState(false);

  //this method is called whenever the update details button is pressed so it triggers the useEffect function to update the details of the room
  const updateDetails = () => {
    setCall(!call);
  };

  const authenticateSpotify = () => {
    console.log("authenticate called");
    fetch("/spotify/is-authenticated").then((response) => response.json()) //checks if user is authenticated
    .then((data) => {
      setSpotifyAuthenticated(data.status);
      console.log("authenticated: " + spotifyAuthenticated.toString());
      if (!data.status) {
        fetch('/spotify/get-auth-url')
        .then((response) => {
          console.log(response);
          return response.json()}) //calls the backend function which returns the url we need to redirect the user to so they can log in
        .then((data) => {
          console.log("opening window")
          window.location.replace(data.url); //js function to open a new window that takes us to the url to log in
        })
      }
    })
  }

  const getCurrentSong = () => {
    fetch('/spotify/current-song').then((response) => {
      if (!response.ok) {
        return {};
      } else {
        return response.json();
      }
    }).then((data) => setRoomData({
      ...roomData,
      song: data
    }));
  }

  useEffect(() => {
    let interval = setInterval(getCurrentSong, 1000);
    return () => {
      clearInterval(interval);
    }
  }, []);

  useEffect(() => {
    console.log("getting room details")
    console.log(roomCode)
    fetch("/api/get-room" + "?code=" + roomCode) //sends a fetch request to the url above and gets the data from that
      .then((response) => {
        if (!response.ok) {
          props.leaveRoomCallback();
          nav("/");
        }
        return response.json();
      }) // then converts it to a json file
      .then((data) => {
        //then sets the state of the current room using the data from that file
        setRoomData({
          ...roomData,
          votesToSkip: data.votes_to_skip,
          guestCanPause: data.guest_can_pause,
          isHost: data.is_host,
        });
        console.log("roomdata is host: " + roomData.isHost.toString())
        if (roomData.isHost) {
          console.log("calling")
          authenticateSpotify();
      }
      });
  }, [roomCode, call]); //this list is what it is dependent on so it changes when roomCode or call changes and it sets the roomdata

  const leaveButtonPressed = () => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    };
    fetch("/api/leave-room", requestOptions).then((_response) => {
      props.leaveRoomCallback();
      nav("/");
    });
  };

  const updateShowSettings = (value) => {
    setShowSettings(value);
  };

  const renderSettingsButton = () => {
    return (
      <Grid item xs={12} align="center">
        <Button
          variant="contained"
          color="primary"
          onClick={() => updateShowSettings(true)}
        >
          Settings
        </Button>
      </Grid>
    );
  };

  const renderSettings = () => {
    return (
      <Grid container spacing={1}>
        <Grid item xs={12} align="center">
          <CreateRoomPage
            update={true}
            votesToSkip={roomData.votesToSkip}
            guestCanPause={roomData.guestCanPause}
            roomCode={roomCode}
            updateCallBack={updateDetails}
          />
        </Grid>
        <Grid item xs={12} align="center">
          <Button
            variant="contained"
            color="secondary"
            onClick={() => updateShowSettings(false)}
          >
            Close
          </Button>
        </Grid>
      </Grid>
    );
  };
  if (showSettings) {
    return renderSettings();
  } else {
    return (
      <Grid container spacing={1}>
        <Grid item xs={12} align="center">
          <Typography variant="h4" component="h4">
            Code: {roomCode.toString()}
          </Typography>
        </Grid>
        <MusicPlayer {...roomData.song}/>
        {roomData.isHost ? renderSettingsButton() : null}
        <Grid item xs={12} align="center">
          <Button
            variant="contained"
            color="secondary"
            onClick={leaveButtonPressed}
          >
            Leave Room
          </Button>
        </Grid>
      </Grid>
    );
  }
};
export default Room;
