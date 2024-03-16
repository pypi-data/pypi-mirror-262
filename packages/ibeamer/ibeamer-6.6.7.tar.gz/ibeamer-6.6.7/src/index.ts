import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { DOMUtils } from '@jupyterlab/apputils';
import {Widget} from '@lumino/widgets';

const ilambda_Anchor_CSS_CLASS = 'jp-ilambda-Anchor';

/**
 * Initialization data for the iBeamer extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'iBeamer:plugin',
  description: 'A simple .css Beamer/LaTeX Environment Extension for Jupyter Lab/Notebooks',
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    console.log('ibeamer is activated!');

    let node;

    // Check if the node exists before creating it
    if (!document.querySelector(".jp-ilambda-Anchor")) {
      // If the node doesn't exist, create it
      node = document.createElement("div");
      node.innerHTML = "<a href='https://www.lambda.joburg' target='_blank'><img src='https://lambda.joburg/assets/images/index/logo/lambda_logo.svg'></a>";
    }

    // Check if the node has been successfully created
    if (node) {
      const widget = new Widget({node}); // constructor for creating a widget from a DOM element
      widget.addClass(ilambda_Anchor_CSS_CLASS);
      widget.id = DOMUtils.createDomID();
      app.shell.add(widget, 'top', {rank: 1000}); // rank - move widget to right-most position in top area panel
    }

  }
};

export default plugin;
