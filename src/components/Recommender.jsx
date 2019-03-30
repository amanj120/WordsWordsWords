import React, { Component } from "react";

import axios from "axios";

class Recommender extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <React.Fragment>
        <h1>Recommended Words:</h1>
        <h3>{this.props.lastWord}</h3>
      </React.Fragment>
    );
  }
}

export default Recommender;
