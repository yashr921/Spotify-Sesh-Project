import React, {Component, useState} from "react";
import { TextField, Button, Grid, Typography } from "@material-ui/core";
import { Link, useNavigate } from "react-router-dom";

const RoomJoinPage = (props) => {
    const [roomData, setRoomData] = useState({
        roomCode: "",
        error: ""
    });
    
    const history = useNavigate();

    //updates the room code every time the text field is changed
    const handleTextFieldChange = (e) => {
        setRoomData({
            ...roomData,
            roomCode: e.target.value
        })
    }

    const roomButtonPressed = (e) => {
        const requestOptions = {
            method: 'POST',
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify({
                code:roomData.roomCode
            })
        };
        fetch("/api/join-room", requestOptions).then((response) => {
            if (response.ok) {
                console.log("rerouting")
                history(`/room/${roomData.roomCode}`);
            } else {
                setRoomData({
                    error: "Room Not Found"
                });
            }
        }).catch((error) => {
            console.log(error);
        });
        console.log(roomData);
    }
        //html for the page, just adds the buttons and creates the form
        return (
            <Grid container spacing={1} align="center">
                <Grid item xs={12}>
                    <Typography variant="h4" component="h4">
                        Join a Room
                    </Typography>
                </Grid>
                <Grid item xs={12}>
                    <TextField 
                        error={roomData.error} 
                        label="Code"
                        placeholder="Enter a Room Code"
                        value={roomData.roomCode}
                        helperText={roomData.error}
                        variant="outlined"
                        onChange={handleTextFieldChange}
                    />
                </Grid>
                <Grid item xs={12}>
                <Grid item xs={12}>
                    <Button variant="contained" color="primary" onClick={roomButtonPressed}>
                        Enter Room
                    </Button>
                </Grid>
                </Grid>
                <Grid item xs={12}>
                    <Button variant="contained" color="secondary" to="/" component={Link}>
                        Back
                    </Button>
                </Grid>
        </Grid>
        )
}
export default RoomJoinPage