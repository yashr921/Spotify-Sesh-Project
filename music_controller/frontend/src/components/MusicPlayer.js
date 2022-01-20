import React, {Component} from 'react';
import {Grid, Typography, Card, IconButton, LinearProgress} from "@material-ui/core"
import PlayArrowIcon from '@material-ui/icons/PlayArrow'
import PauseIcon from '@material-ui/icons/Pause'
import SkipNextIcon from '@material-ui/icons/SkipNext'

// displays the card that shows all the song info, play/pause and skip buttons
export const MusicPlayer = (props) => {

    const pauseSong = () => {
        const requestOptions = {
            'method': 'PUT',
            headers: {'Content-Type':'application/json'},
        };
        fetch('/spotify/pause', requestOptions);
    }

    const playSong = () => {
        const requestOptions = {
            'method': 'PUT',
            headers: {'Content-Type':'application/json'},
        };
        fetch('/spotify/play', requestOptions);
    }

    const skipSong = () => {
        console.log("skipsong called")
        const requestOptions = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
        };
        fetch('/spotify/skip', requestOptions);
    }

    return (
        <Card>
            <Grid container alignItems='center'>
                <Grid item align='center' xs={4}>
                    <img src={props.image_url} height='100%' width='100%' />
                </Grid>
                <Grid item align='center' xs={8}>
                    <Typography component="h5" variant="h5">
                        {props.title}
                    </Typography>
                    <Typography color="textSecondary" variant='subtitle1'>
                        {props.artist}
                    </Typography>
                    <div>
                        <IconButton onClick={() => {props.is_playing ? pauseSong() : playSong()}}>
                            {props.is_playing ? <PauseIcon /> : <PlayArrowIcon />}
                        </IconButton>
                        <IconButton onClick={() => skipSong()}>
                            <SkipNextIcon /> {props.votes} / {props.votes_required}
                        </IconButton>
                    </div>
                </Grid>
            </Grid>
            <LinearProgress variant='determinate' value = {props.time / props.duration * 100} />
        </Card>
    )
}
export default MusicPlayer