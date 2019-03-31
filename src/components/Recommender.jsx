import React, { Component } from "react";

import axios from "axios";
import RecColumn from "./RecColumn";

class Recommender extends Component {
  constructor(props) {
    super(props);
    this.state = {
      latestCol: 0,
      recentWord: null,
      columnData: []
    };
  }

  componentDidMount() {
    console.log("Recommender Did Mount");
    this.setStartingWords();
  }

  getNumColumns = () => this.state.columns.length;

  setStartingWords = () => {
    axios.get("http://localhost:3000/starters").then(res => {
      let arrayStartWords = res.data;
      this.setState(prevState => ({
        columnData: [...prevState.columnData, arrayStartWords]
      }));
    });
  };

  renderWordColumns = () => {
    if (this.state.columnData == undefined) return;

    let cols = [];

    this.state.columnData.map((item, index) => {
      cols.push(
        <div style={{ float: "left", marginRight: 5 }} key={index}>
          <RecColumn
            providedWords={item}
            handleAddColumn={chosenWordObj => this.addWordColumn(chosenWordObj)}
          />
        </div>
      );
    });

    return cols;
  };

  addWordColumn = chosenWordObj => {
    this.setState({
      recentWord: chosenWordObj.word
    });

    // CHANGE THIS
    axios.get("http://localhost:3000/words/" + "").then(res => {
      let arrayNewWords = res.data;
      this.setState(prevState => ({
        columnData: [...prevState.columnData, arrayNewWords]
      }));
    });
  };

  render() {
    return (
      <React.Fragment>
        <h1>{"HI: " + this.state.recentWord}</h1>
        <h1>Recommended Words:</h1>
        {this.renderWordColumns()}
      </React.Fragment>
    );
  }
}

export default Recommender;
