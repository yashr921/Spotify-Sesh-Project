import React, {Component} from "react";
import {render} from "react-dom"
import HomePage from "./HomePage";

/**
 * This component returns the render that is to be rendered by the static part of the template in the app div of the templates/frontend/index.html file
 */
export default class App extends Component {
    constructor(props) {
        super(props);
    }
    /* This the the part to be rendered, we are returning the router that routes to the correct page */
    render() {
      console.log("at home page")
        return (
            <div className="center">
              <HomePage />
            </div>
          );
    }
}
/* This is the code to render the component inside of the app container*/
const appDiv = document.getElementById("app"); /* This part accesses the app container in the index.html file */
render(<App />, appDiv); /* This line renders the app component in the app div */