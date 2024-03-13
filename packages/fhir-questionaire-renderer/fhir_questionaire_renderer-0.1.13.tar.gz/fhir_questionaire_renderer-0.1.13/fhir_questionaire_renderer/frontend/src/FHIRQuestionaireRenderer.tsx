import {
  StreamlitComponentBase,
  Streamlit,
  withStreamlitConnection,
} from "streamlit-component-lib";
import React, { ReactNode } from 'react';
import { SmartFormsRenderer, getResponse } from "@aehrc/smart-forms-renderer";

/**
 * This is a React-based component template. The `render()` function is called
 * automatically when your component should be re-rendered.
 */
class FHIRQuestionnaireRenderer extends StreamlitComponentBase<{height?:number}> {
  private rootElement = React.createRef<HTMLDivElement>();

componentDidMount() {
  setTimeout(() => this.adjustFrameHeight(), 1000);
}

componentDidUpdate() {
  setTimeout(() => this.adjustFrameHeight(), 1000);
}

adjustFrameHeight() {
  const height = this.rootElement.current?.clientHeight || 0;
  console.log('Calculated height:', height);
  this.setState({ height });
  Streamlit.setFrameHeight(height);
}
  
  public render = (): ReactNode => {
    // Arguments that are passed to the plugin in Python are accessible
    // via `this.props.args`. Here, we access the "name" arg.
    const questionnaire = this.props.args["questionaire"];

    return (
      <div
        ref={this.rootElement}
        style={{ height: "auto", overflow: "auto" }}
      >
        <SmartFormsRenderer questionnaire={questionnaire}  />
        <button
          onClick={() => {
            Streamlit.setComponentValue(getResponse());
            // Do something with the questionnaire response
          }}
        >
          Submit
        </button>
      </div>
    );
  };
}

export default withStreamlitConnection(FHIRQuestionnaireRenderer);
