import React, { Component } from "react";

import "./style.css"

class App extends Component {
  render() {
    return (
      <React.Fragment>
        <center>
          <h1 className="fancy-font">Wordswordswords</h1>
        </center>
        <hr />
        <p>Enter some words:</p>
        <input type="text"></input>
      </React.Fragment>
    );
  }
}

export default App;
