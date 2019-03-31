import React, { Component, Fragment } from "react";

class RecColumn extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  componentDidMount() {
    console.log("Column Did Mount");
  }

  handleWordClick = index => {
    let chosenWordObj = this.props.providedWords[index];
    this.props.handleAddColumn(chosenWordObj);
  };

  returnWordColumn() {
    if (this.props.providedWords == undefined) return;

    let wordBoxes = [];

    this.props.providedWords.map((item, i) => {
      wordBoxes.push(
        <Fragment key={i}>
          <div onClick={() => this.handleWordClick(i)} className="wordBox">
            {item.word}
          </div>
          <br />
        </Fragment>
      );
    });

    return wordBoxes;
  }

  render() {
    return <Fragment>{this.returnWordColumn()}</Fragment>;
  }
}

export default RecColumn;
