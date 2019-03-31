import React, { Component } from "react";

import "./style.css";
import Recommender from "./Recommender";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    return (
      <React.Fragment>
        <Recommender />
      </React.Fragment>
    );
  }
}

export default App;
