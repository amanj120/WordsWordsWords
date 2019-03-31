import React, { Component } from "react";

import "./style.css";
import Recommender from "./Recommender";

const wordRegex = /\w+(?:'\w+)?(?:-\w+(?:'\w+)?)*|(?:[.,:;!?–—]|-{2,})/g;

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      words: null,
      lastWord: undefined
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

  render() {
    return (
      <React.Fragment>
        <center>
          <h1 className="fancy-font">Wordswordswords</h1>
        </center>
        <hr />
        <p>Start typing a sentence</p>
        <input type="text" onChange={this.updateInputValue} />
        <Recommender lastWord={this.state.lastWord} />
      </React.Fragment>
    );
  }
}

export default App;
