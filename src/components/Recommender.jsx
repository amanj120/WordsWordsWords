import React, { Component } from "react";

import axios from "axios";
import RecColumn from "./RecColumn";
import { timingSafeEqual } from "crypto";

const AMAN_URL = "https://128.61.46.216:5000/";
const FAKE_URL = "http://localhost:3000/";
const GC_URL = "http://35.237.17.108:5000/";
const ACT_URL = GC_URL;
const wordRegex = /\w+(?:\'\w+)?(?:-\w+(?:\'\w+)?)*(?:\s*[.,:;!?–—]|-+)?/g;

class Recommender extends Component {
  constructor(props) {
    super(props);
    this.state = {
      latestColIndex: 0,
      viewIndex: 0,
      recentWord: null,
      columnData: [],
      selectedIndices: [],
      words: null,
      lastWord: undefined,
      textContent: "",
      currSentence: ""
    };
  }

  getWordCount = () => {
    if (this.state.words === null || this.state.words == "") return 0;
    return this.state.words.length;
  };

  getLastWord = () => {
    let wordCount = this.getWordCount();
    if (wordCount >= 1) return this.state.words[wordCount - 1];
    else return undefined;
  };

  updateInputValue = evt => {
    this.setState(
      {
        words: evt.target.value.match(wordRegex)
      },
      () => {
        this.setState({
          lastWord: this.getLastWord()
        });
      }
    );
  };

  handleWordEnter = () => {
    let chosenWordObj = {
      word: this.state.textContent,
      freq: 0
    };

    console.log(chosenWordObj);
    this.addWordColumn(chosenWordObj, this.state.colIndex, 0, true);
  };

  handleKeyDown = evt => {
    if (evt.key === "Enter") {
      if (this.state.textContent !== "") {
        this.handleWordEnter();
        this.setState({
          textContent: ""
        });
      }
    } else if (evt.key === "Backspace") {
      this.setState({
        textContent: this.state.textContent.substring(
          0,
          this.state.textContent.length - 1
        )
      });
    } else if (/[a-zA-Z0-9-_ ]/.test(String.fromCharCode(evt.keyCode))) {
      this.setState({
        textContent: this.state.textContent + evt.key
      });
    }
  };

  handleSubmitPress = () => {};

  componentDidMount() {
    console.log("Recommender Did Mount");
    this.setStartingWords();
  }

  getNumColumns = () => this.state.columns.length;

  setStartingWords = () => {
    axios.get(ACT_URL + "starters").then(res => {
      let arrayStartWords = res.data;
      this.setState(prevState => ({
        columnData: [...prevState.columnData, arrayStartWords]
      }));
    });
  };

  renderWordColumns = () => {
    if (this.state.columnData == undefined) return;

    /*
    let cols = [];

    this.state.columnData.map((item, index) => {
      cols.push(
        <div style={{ float: "left", marginRight: 5 }} key={index}>
          <RecColumn
            providedWords={item}
            handleAddColumn={(chosenWordObj, ind) => this.addWordColumn(chosenWordObj, ind)}
            colIndex={index}
          />
        </div>
      );
    });
    */

    let ind = this.state.viewIndex;
    return (
      <React.Fragment>
        <RecColumn
          providedWords={this.state.columnData[ind]}
          handleAddColumn={(chosenWordObj, ind, selectedIndex, isCustom) =>
            this.addWordColumn(chosenWordObj, ind, selectedIndex, isCustom)
          }
          colIndex={ind}
          latestIndex={this.state.latestColIndex}
          selectedIndex={this.state.selectedIndices[ind]}
          handleBackPress={() => this.decColView()}
          handleForwardPress={() => this.incColView()}
        />
      </React.Fragment>
    );

    // return cols;
  };

  decColView = () => {
    if (this.state.viewIndex > 0) {
      this.setState(
        {
          viewIndex: this.state.viewIndex - 1
        },
        () => {
          this.updateCurrSentence();
        }
      );
    }
  };

  incColView = () => {
    if (this.state.viewIndex < this.state.latestColIndex) {
      this.setState(
        {
          viewIndex: this.state.viewIndex + 1
        },
        () => {
          this.updateCurrSentence();
        }
      );
    }
  };

  addWordColumn = (chosenWordObj, ind, selectedIndex, isCustom) => {
    if (ind != this.state.latestColIndex) {
      this.setState(
        {
          recentWord: chosenWordObj.word,
          latestColIndex: this.state.viewIndex + 1,
          viewIndex: this.state.viewIndex + 1
        },
        () => {
          axios.get(ACT_URL + "words/" + this.state.recentWord).then(res => {
            let arrayNewWords = res.data;

            if (isCustom) selectedIndex = 0;
            this.setState(
              prevState => ({
                columnData: [
                  ...prevState.columnData.slice(0, this.state.viewIndex),
                  arrayNewWords
                ],
                selectedIndices: [
                  ...this.state.selectedIndices.slice(
                    0,
                    this.state.viewIndex - 1
                  ),
                  selectedIndex
                ]
              }),
              () => {
                if (isCustom) {
                  const newColumnData = this.state.columnData.slice();
                  newColumnData[this.state.viewIndex - 1].unshift(
                    chosenWordObj
                  );

                  console.log(
                    "New Col Data: " +
                      newColumnData[this.state.viewIndex - 1][1].word
                  );

                  this.setState({
                    columnData: newColumnData
                  }, () => {
                    this.updateCurrSentence();
                  });
                }
              }
            );
          });
        }
      );
    } else {
      this.setState(
        {
          recentWord: chosenWordObj.word,
          latestColIndex: this.state.latestColIndex + 1,
          viewIndex: this.state.viewIndex + 1,
          selectedIndices: [...this.state.selectedIndices, selectedIndex]
        },
        () => {
          axios.get(ACT_URL + "words/" + chosenWordObj.word).then(res => {
            let arrayNewWords = res.data;
            this.setState(
              prevState => ({
                columnData: [...prevState.columnData, arrayNewWords]
              }),
              () => {
                this.updateCurrSentence();
              }
            );
          });
        }
      );
    }
  };

  updateCurrSentence = () => {
    if (this.state.columnData.length === 0) {
      return;
    } else {
      let newSentence = "",
        selectWordInd = null;
      for (let i = 0; i < this.state.viewIndex; i++) {
        selectWordInd = this.state.selectedIndices[i];
        newSentence += " " + this.state.columnData[i][selectWordInd].word;
      }

      this.setState({
        currSentence: newSentence
      });
    }
  };

  render() {
    return (
      <React.Fragment>
        <center>
          <h1 className="fancyFont bigFont">Words Words Words</h1>
          <hr />
          <div>
            <p className="fancyFont medFont">{this.state.currSentence}</p>
          </div>
          <div>
            <table>
              <tbody>
                <tr>
                  <td>
                    <input
                      type="text"
                      onKeyDown={evt => this.handleKeyDown(evt)}
                      onChange={this.updateInputValue}
                      value={this.state.textContent}
                    />
                  </td>
                  <td>
                    <div
                      onClick={this.handleSubmitPress}
                      className="wordSubmitBtn fancyFont medFont centerText"
                    >
                      Submit
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <h3>Recommended Words</h3>
          <h3>{"Selecting Word: " + (this.state.viewIndex + 1).toString()}</h3>
          {this.renderWordColumns()}
        </center>
      </React.Fragment>
    );
  }
}

export default Recommender;

// <Recommender lastWord={this.state.lastWord} />
