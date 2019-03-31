import React, { Component, Fragment } from "react";

class RecColumn extends Component {
  constructor(props) {
    super(props);
    this.state = {
      wordBoxStyle: "wordBox"
    };
  }

  componentDidMount() {
    console.log("Column Did Mount");
  }

  handleWordClick = index => {
    let chosenWordObj = this.props.providedWords[index];
    this.props.handleAddColumn(chosenWordObj, this.props.colIndex, index, false);
  };

  returnStyling(wordInd) {
    console.log(
      "View, Col, Latest, selectedIndex: " +
        this.props.colIndex +
        this.props.latestIndex +
        this.props.selectedIndex
    );
    if (
      wordInd === this.props.selectedIndex &&
      this.props.colIndex < this.props.latestIndex
    )
      return "wordBoxSelect";

    return;
  }

  renderWordColumn() {
    if (this.props.providedWords == undefined) return;

    let wordBoxes = [];

    this.props.providedWords.map((item, i) => {
      let styling = this.returnStyling(i);
      wordBoxes.push(
        <Fragment key={i}>
          <div
            onClick={() => this.handleWordClick(i)}
            className={"wordBox centerText " + styling}
          >
            <p>{item.word + " | " + (item.freq * 100).toFixed(2) + "%"}</p>
          </div>
          <br/>
        </Fragment>
      );
    });

    return wordBoxes;
  }

  render() {
    return (
      <Fragment>
        <table>
          <tbody>
            <tr>
              <td>
                <button onClick={() => this.props.handleBackPress()} className="navButton bigFont">
                  Back
                </button>
              </td>
            </tr>
            <tr>
              <td>
                <button onClick={() => this.props.handleForwardPress()} className="navButton bigFont">
                  Forward
                </button>
              </td>
            </tr>
            <tr><td><p></p></td></tr>
            <tr><td>{this.renderWordColumn()}</td></tr>
          </tbody>
        </table>
      </Fragment>
    );
  }
}

export default RecColumn;
