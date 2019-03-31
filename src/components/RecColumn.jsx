import React, { Component, Fragment } from "react";

class RecColumn extends Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedIndex: null,
      wordBoxStyle: ""
    };
  }

  componentDidMount() {
    console.log("Column Did Mount");
  }

  handleWordClick = index => {
    let chosenWordObj = this.props.providedWords[index];
    this.props.handleAddColumn(chosenWordObj, this.props.colIndex);
    this.changeStyling(index);
  };

  changeStyling = index => {
    this.setState({
      wordBoxStyle: "wordBoxSelect",
      selectedIndex: index
    });
  };

  returnStyling = index => {
    if (index === this.state.selectedIndex)
      return "wordBox " + this.state.wordBoxStyle;
    else return "wordBox";
  };

  renderWordColumn() {
    if (this.props.providedWords == undefined) return;

    let wordBoxes = [];

    this.props.providedWords.map((item, i) => {
      wordBoxes.push(
        <Fragment key={i}>
          <div
            onClick={() => this.handleWordClick(i)}
            className={this.returnStyling(i)}
          >
            {item.word + " | " + item.freq}
          </div>
          <br />
        </Fragment>
      );
    });

    return wordBoxes;
  }

  render() {
    return <Fragment>{this.renderWordColumn()}</Fragment>;
  }
}

export default RecColumn;
