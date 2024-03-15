import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';

import { IThemeManager } from '@jupyterlab/apputils';

/**
 * Initialization data for the theme toggle plugin.
 */
const plugin: JupyterFrontEndPlugin<void> = {
    id: 'skillsnetwork_jupyter_extension:theme',
    description: 'Theme toggle plugin for Skills Network Authoring Extension',
    autoStart: true,
    requires: [IThemeManager],
    activate: (app: JupyterFrontEnd, themeManager: IThemeManager) => {
      console.log('Activating skillsnetwork_jupyter_extension theme toggle plugin!');
  
      /* Incoming messages management */
      window.addEventListener('message', (event) => {
        if (event.data.type === 'update_theme') {
          console.log('Message received in the iframe:', event.data);
  
          if (event.data.color === 'light') {
            themeManager.setTheme('JupyterLab Light');
          } else {
            themeManager.setTheme('JupyterLab Dark');
          }
        }
      });
    },
  };
  
  export default plugin;