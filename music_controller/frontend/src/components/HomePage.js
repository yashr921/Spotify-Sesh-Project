import React, { Component } from "react";
import RoomJoinPage from "./RoomJoinPage";
import CreateRoomPage from "./CreateRoomPage";
import Room from './Room';
import {Grid, Button, ButtonGroup, Typography} from '@material-ui/core'

import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
  Navigate,
} from "react-router-dom";

// const HomePage = (props) => {
//   /* This routes to the correct page */
//   //the : in the roomCode url allows us to put in a variable in the url meaning it is a dynamic url

//     const renderHomePage = () => {
//       console.log("rendering")
//       return (
//         <Grid container={3}>
//           <Grid item xs={12} align="center">
//             <Typography variant="h3" compact="h3">
//               Spotify Sesh
//             </Typography>
//           </Grid>
//           <Grid item xs={12} align="center">
//             <ButtonGroup disableElevation variant="contained" color="primary">
//               <Button color="primary" to="/join" component={Link}>
//                 Join Room
//               </Button>
//               <Button color="secondary" to="/create" component={Link}>
//                 Create Room
//               </Button>
//             </ButtonGroup>
//           </Grid>
//         </Grid>
//       )
//     }
   
//     return (
//     <Router>
//         <Routes>
//         <Route exact path="/" element={renderHomePage}></Route>
//         <Route path="/join" element={<RoomJoinPage/>}></Route>
//         <Route path="/create" element={<CreateRoomPage/>}></Route>
//         <Route path="/room/:roomCode" element={<Room/>}></Route>
//         </Routes>
//     </Router>
//     )
// }
// export default HomePage

export default class HomePage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      roomCode: null,
    };
    this.clearRoomCode = this.clearRoomCode.bind(this);
  }

  async componentDidMount() {
    fetch("/api/user-in-room")
      .then((response) => response.json())
      .then((data) => {
        this.setState({
          roomCode: data.code,
        });
      });
      }

  renderHomePage() {
    return (
      <Grid container spacing={3}>
        <Grid item xs={12} align="center">
          <Typography variant="h3" compact="h3">
            Spotify Sesh
          </Typography>
        </Grid>
        <Grid item xs={12} align="center">
          <ButtonGroup disableElevation variant="contained" color="primary">
            <Button color="primary" to="/join" component={Link}>
              Join Room
            </Button>
            <Button color="secondary" to="/create" component={Link}>
              Create Room
            </Button>
          </ButtonGroup>
        </Grid>
      </Grid>
    );
  }

  clearRoomCode() {
    this.setState({
      roomCode: null
    });
  }


  render() {
    return (
          <Router>
              <Routes>
              <Route path="/" element={this.state.roomCode == null ? this.renderHomePage() : <Navigate to={`/room/${this.state.roomCode}`}/>}></Route>
              <Route path="/join" element={<RoomJoinPage/>}></Route>
              <Route path="/create" element={<CreateRoomPage/>}></Route>
              <Route path="/room/:roomCode" element={<Room {...this.props} leaveRoomCallback={this.clearRoomCode}/>}></Route>
              </Routes>
          </Router>
          )
  }
}